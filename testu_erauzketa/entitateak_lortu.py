from __future__ import annotations

from typing import Any, Dict, List, Union, Optional, Tuple
import json
import os
import random
import shutil
import time

import pandas as pd
import requests

# --- EU: hitz.eus NER API ---
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
    last_exc: Exception | None = None

    for attempt in range(max_retries):
        try:
            r = requests.post(url, headers=HEADERS, json=payload, timeout=timeout)

            if 200 <= r.status_code < 300:
                try:
                    return r.json()
                except Exception:
                    return r.text

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

    raise RuntimeError(f"APIak huts egin du {max_retries} saiakeren ondoren. Azken errorea: {last_exc}")



# EU formatting (API response)
def _format_entities_as_list_eu(resp: Union[Dict[str, Any], List[Any], str]) -> str:
    """
    EU NER APIaren erantzuna -> JSON string:
    [
      {"text": "...", "label": "PER"},
      ...
    ]
    """
    if isinstance(resp, str):
        s = resp.strip()
        try:
            resp = json.loads(s)
        except Exception:
            return "[]"

    # Zure aurreko logikaren arabera: {"emaitza": { "Entitatea": "LABEL", ...}}
    if isinstance(resp, dict) and "emaitza" in resp and isinstance(resp["emaitza"], dict):
        entities = [{"text": ent, "label": lab} for ent, lab in resp["emaitza"].items()]
        return json.dumps(entities, ensure_ascii=False)

    return "[]"



def _merge_entity_lists(entity_lists: List[List[Dict[str, Any]]], dedup: bool = False) -> List[Dict[str, Any]]:
    """
    Chunk bakoitzeko zerrendak batu.
    dedup=True bada, (text,label) bidez deduplikatzen du (ordena mantenduta).
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



# ES formatting (Flair)
def _load_flair_es_ner(model_name: str = "flair/ner-spanish-large", device: str = "cpu"):
    """
    Flair NER modeloa kargatu (behin bakarrik).
    model_name: 'flair/ner-spanish-large' (gomendatua)
    device: 'cpu' edo 'cuda'
    """
    if device == "cuda" and torch.cuda.is_available():
        flair_device = torch.device("cuda")
    else:
        flair_device = torch.device("cpu")

    # Flair-ek barnean erabiltzen du device globala kasu batzuetan; seguruena:
    try:
        import flair
        flair.device = flair_device
    except Exception:
        pass

    tagger = Classifier.load(model_name)
    return tagger



def _entities_es_flair(text: str, tagger) -> List[Dict[str, Any]]:
    """
    Testu batetik Flair bidez NER: [{"text":..., "label":...}, ...]
    Flair-eko span tag-ak normalean: PER/LOC/ORG/MISC (modelaren arabera).
    """
    if not text:
        return []

    sent = Sentence(text)
    tagger.predict(sent)

    ents: List[Dict[str, Any]] = []
    for span in sent.get_spans("ner"):
        # span.text: entity surface form
        # span.tag: entity label
        ents.append({"text": span.text, "label": span.tag})
    return ents



def _entities_es_text_chunked(text: str, tagger, max_chars: int = 3000) -> str:
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
    TSV-n lerroak ez apurtzeko (tab/newline).
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
    Entitateak (NER) lortzen ditu:
    - TSV batean pixkanaka idazten du (segurtasunez)
    - TSV badago, reanuda egiten du
    - Entities badago eta hutsik ez badago, errenkada saltatzen du
    - eu -> hitz.eus API
    - es -> Flair
    """
    tmp_tsv = output_tsv + ".tmp"

    df_out = df.copy()
    if "Entities" not in df_out.columns:
        df_out["Entities"] = ""



    # Flair (ES) modeloa kargatu behin
    try:
        tagger_es = _load_flair_es_ner(flair_es_model, device=flair_device)
    except Exception as e:
        raise RuntimeError(
            f"Ezin izan da Flair ES NER modeloa kargatu: {flair_es_model}. "
            f"Probatu: pip install flair torch"
        ) from e
    


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
