from __future__ import annotations

from typing import Any, Dict, List, Tuple, Union
import json
import random
import shutil
import time

import pandas as pd
import requests

# |----------------------------------------------------------------------------------------------------|
# |------------------------------------------ KONFIGURAZIOA -------------------------------------------|
# |----------------------------------------------------------------------------------------------------|

# --- Euskara: hitz.eus NER APIa ---
URL_NERC_EU = "https://zerbitzuak.hitz.eus/lema/api/nerc"

HEADERS = {
    "accept": "*/*",
    "Content-Type": "application/json",
}

# --- ES: Flair NER ---
from flair.nn import Classifier
from flair.data import Sentence
import torch



def _chunk_text(text: str, max_chars: int = 3000) -> List[str]:
    """
    Testu luze bat zatitzen du max_chars muga errespetatuz, ahal den neurrian zuriuneetan moztuta.

    Return:
    - Zati-zerrenda (List[str]). Testua hutsik bada, zerrenda hutsa.
    """
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    chunks: List[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(n, start + max_chars)

        # Zatiaren amaiera hurrengo hitzaren erdian gera ez dadin, zuriunean mozten saiatzen da
        if end < n:
            cut = text.rfind(" ", start, end)
            if cut != -1 and cut > start + 200:
                end = cut

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end

    return chunks



def _post_json(
    url: str,
    payload: Dict[str, Any],
    timeout: int = 60,
    max_retries: int = 6,
    backoff_base: float = 1.6,
    backoff_max: float = 25.0,
) -> Union[Dict[str, Any], List[Any], str]:
    """
    JSON POST eskaera sendoa egiten du, eta 429/5xx kasuetan berriro saiatzen da atzerapen progresiboarekin.

    Return:
    - APIaren erantzuna (dict/list/str), formatuaren arabera.
    """
    last_exc: Exception | None = None

    for attempt in range(max_retries):
        try:
            r = requests.post(url, headers=HEADERS, json=payload, timeout=timeout)

            if 200 <= r.status_code < 300:
                try:
                    return r.json()
                except Exception:
                    return r.text
            
            # Muga edo aldi baterako erroreak: itxaron eta berriro saiatu
            if r.status_code in (429, 500, 502, 503, 504):
                wait = min(backoff_max, (backoff_base ** attempt)) + random.random() * 0.3
                ra = r.headers.get("Retry-After")
                if ra and ra.isdigit():
                    wait = max(wait, float(ra))
                time.sleep(wait)
                continue

            r.raise_for_status()

        except (requests.Timeout, requests.ConnectionError) as e:
            last_exc = e
            wait = min(backoff_max, (backoff_base ** attempt)) + random.random() * 0.3
            time.sleep(wait)
            continue
        except requests.HTTPError as e:
            last_exc = e
            wait = min(backoff_max, (backoff_base ** attempt)) + random.random() * 0.3
            time.sleep(wait)
            continue

    raise RuntimeError(
        f"APIak huts egin du {max_retries} saiakeren ondoren. Azken errorea: {last_exc}"
    )



def _format_entities_as_list_eu(resp: Union[Dict[str, Any], List[Any], str]) -> str:
    """
    EU NER APIaren erantzuna JSON kate estandar batera bihurtzen du.

    Formatu-helburua:
    [
      {"text": "...", "label": "PER"},
      ...
    ]

    Return:
    - Entitate-zerrenda JSON kate gisa (str). Ezin bada interpretatu, "[]".
    """
    if isinstance(resp, str):
        s = resp.strip()
        try:
            resp = json.loads(s)
        except Exception:
            return "[]"

    # Espero den egitura: {"emaitza": {"Entitatea": "LABEL", ...}}
    if isinstance(resp, dict) and "emaitza" in resp and isinstance(resp["emaitza"], dict):
        entities = [{"text": ent, "label": lab} for ent, lab in resp["emaitza"].items()]
        return json.dumps(entities, ensure_ascii=False)

    return "[]"



def _merge_entity_lists(entity_lists: List[List[Dict[str, Any]]], dedup: bool = False) -> List[Dict[str, Any]]:
    """
    Chunk bakoitzeko entitate-zerrendak bateratzen ditu.

    Aukerak:
    - dedup=True bada, (text, label) bikotearen arabera deduplikatzen du (ordena mantenduta).

    Return:
    - Entitateen zerrenda bateratua (List[Dict[str, Any]]).
    """
    if not dedup:
        out: List[Dict[str, Any]] = []
        for lst in entity_lists:
            out.extend(lst)
        return out

    seen: set[Tuple[str, str]] = set()
    out2: List[Dict[str, Any]] = []
    for lst in entity_lists:
        for e in lst:
            t = str(e.get("text", ""))
            l = str(e.get("label", ""))
            key = (t, l)
            if key in seen:
                continue
            seen.add(key)
            out2.append({"text": t, "label": l})
    return out2



def _entities_eu_text_chunked(text: str, max_chars: int = 3000, sleep_s: float = 0.05) -> str:
    """
    Euskarazko testua zatitu eta NER API bidez entitateak erauzten ditu, ondoren zatien emaitzak bateratuz.

    Return:
    - Entitate-zerrenda JSON kate gisa (str).
    """
    chunks = _chunk_text(text, max_chars=max_chars)
    all_lists: List[List[Dict[str, Any]]] = []

    for ch in chunks:
        try:
            resp = _post_json(URL_NERC_EU, {"text": ch})
            s = _format_entities_as_list_eu(resp)
            all_lists.append(json.loads(s))
        except Exception as e:
            print(f"[WARN] EU NER chunk-ak huts egin du ({type(e).__name__}): {e}")
            all_lists.append([])

        if sleep_s:
            time.sleep(sleep_s)

    merged = _merge_entity_lists(all_lists, dedup=False)
    return json.dumps(merged, ensure_ascii=False)



def _load_flair_es_ner(model_name: str = "flair/ner-spanish-large", device: str = "cpu"):
    """
    Gaztelania: Flair NER modeloa kargatzen du (behin bakarrik erabiltzeko pentsatua).

    Parametroak:
    - model_name: modeloa (adib. "flair/ner-spanish-large")
    - device: "cpu" edo "cuda"

    Return:
    - Flair tagger objektua.
    """
    if device == "cuda" and torch.cuda.is_available():
        flair_device = torch.device("cuda")
    else:
        flair_device = torch.device("cpu")

    # Flair-ek zenbait kasutan device globala erabiltzen du; lehenetsi ezarpena
    try:
        import flair
        flair.device = flair_device
    except Exception:
        pass

    tagger = Classifier.load(model_name)
    return tagger



def _entities_es_flair(text: str, tagger) -> List[Dict[str, Any]]:
    """
    Gaztelaniazko testutik, Flair bidez NER kalkulatu eta zerrenda egituratuan ematen du.

    Return:
    - [{"text": ..., "label": ...}, ...]
    """
    if not text:
        return []

    sent = Sentence(text)
    tagger.predict(sent)

    ents: List[Dict[str, Any]] = []
    for span in sent.get_spans("ner"):
        ents.append({"text": span.text, "label": span.tag})
    return ents



def _entities_es_text_chunked(text: str, tagger, max_chars: int = 3000) -> str:
    """
    Gaztelaniazko testua zatitu eta chunk bakoitzean Flair bidez entitateak erauzten ditu.

    Return:
    - Entitate-zerrenda JSON kate gisa (str).
    """
    chunks = _chunk_text(text, max_chars=max_chars)
    all_lists: List[List[Dict[str, Any]]] = []

    for ch in chunks:
        try:
            all_lists.append(_entities_es_flair(ch, tagger))
        except Exception as e:
            print(f"[WARN] ES Flair NER chunk-ak huts egin du ({type(e).__name__}): {e}")
            all_lists.append([])

    merged = _merge_entity_lists(all_lists, dedup=False)
    return json.dumps(merged, ensure_ascii=False)



def _tsv_safe(x: Any) -> str:
    """
    TSV-n lerroak ez apurtzeko, tabulazioak eta lerro-jauziak ordezkatzen ditu.

    Return:
    - TSV-rako segurua den kate bat (str).
    """
    s = "" if x is None else str(x)
    return s.replace("\t", " ").replace("\n", " ").replace("\r", " ")



# Funtzio nagusia
def entitateak_lortu(
    df: pd.DataFrame,
    text_col: str = "Text",
    lang_col: str = "Language",
    output_tsv: str = "corpus_erauzketa_entities.tsv",
    flair_es_model: str = "flair/ner-spanish-large",
    flair_device: str = "cuda",  # "cpu" edo "cuda"
) -> pd.DataFrame:
    """
    Entitateak (NER) erauzten ditu eta TSV batean pixkanaka idazten ditu.

    Jokabidea:
    - "Entities" zutabea existitzen ez bada, sortu egiten da.
    - Errenkadak "Entities" beteta badu, ez da berriro prozesatzen.
    - eu -> hitz.eus NER APIa
    - es -> Flair

    Return:
    - Entitateak gehituta dituen DataFrame-a (pd.DataFrame).
    """
    tmp_tsv = output_tsv + ".tmp"

    df_out = df.copy()
    if "Entities" not in df_out.columns:
        df_out["Entities"] = ""



    # --- Flair (ES) modeloa kargatu behin ---
    try:
        tagger_es = _load_flair_es_ner(flair_es_model, device=flair_device)
    except Exception as e:
        raise RuntimeError(
            f"Ezin izan da Flair ES NER modeloa kargatu: {flair_es_model}. "
            f"Probatu: pip install flair torch"
        ) from e
    


    # |----------------------------------------------------------------------------------------------------|
    # |-------------------------------------- PROZESAMENDUA ETA IDAZKETA ----------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    with open(tmp_tsv, "w", encoding="utf-8") as f:
        f.write("\t".join(df_out.columns) + "\n")

        for i, row in df_out.iterrows():
            entities_existing = str(row.get("Entities", "")).strip()
            if entities_existing and entities_existing.lower() != "nan":
                f.write("\t".join(_tsv_safe(v) for v in row.tolist()) + "\n")
                continue

            text = str(row.get(text_col, "")).strip()
            lang = str(row.get(lang_col, "")).strip()

            if not text:
                row["Entities"] = "[]"
                f.write("\t".join(_tsv_safe(v) for v in row.tolist()) + "\n")
                continue

            if lang == "eu":
                entities_str = _entities_eu_text_chunked(text, max_chars=3000, sleep_s=0.05)
            elif lang == "es":
                entities_str = _entities_es_text_chunked(text, tagger_es, max_chars=3000)
            else:
                print(
                    f"[WARN] Hizkuntza ezezaguna: {lang!r} (onartzen direnak: 'eu', 'es'). "
                    "Ez da NER kalkulatuko; 'Entities' = []"
                )
                entities_str = "[]"

            row["Entities"] = entities_str
            f.write("\t".join(_tsv_safe(v) for v in row.tolist()) + "\n")
            f.flush()

            if (i + 1) % 50 == 0:
                print(f"[INFO] {i+1}/{len(df_out)} errenkada prozesatuta")

    shutil.move(tmp_tsv, output_tsv)
    return df_out
