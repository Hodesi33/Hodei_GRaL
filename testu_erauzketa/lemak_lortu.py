from __future__ import annotations

from typing import Any, Dict, List, Union, Optional
import os
import random
import shutil
import time

import pandas as pd
import requests

# --- Euskara lematizatzeko APIa ---
URL_LEMMA = "https://zerbitzuak.hitz.eus/lema/api/lemma"

HEADERS = {
    "accept": "*/*",
    "Content-Type": "application/json",
}

# --- Gaztelaniarako spaCy ---
# Instalazioa:
#   pip install spacy
#   python -m spacy download es_core_news_md
import spacy



def _chunk_text(text: str, max_chars: int = 3000) -> List[str]:
    """
    Testu luze bat zatitzen du max_chars baino txikiagoak diren zatitan,
    ahal bada zuriuneetan moztuz.
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
    POST sendoa: berriro saiatzen da 429 eta 5xx erroreetan.
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



def _format_lemma_response(resp: Union[Dict[str, Any], List[Any], str]) -> str:
    """
    APIaren erantzuna lemen string batera bihurtzen du.
    """
    if isinstance(resp, str):
        return resp.strip()

    if isinstance(resp, list):
        return " ".join(
            str(it.get("lemma", it)) if isinstance(it, dict) else str(it)
            for it in resp
        ).strip()

    if isinstance(resp, dict):
        if "emaitza" in resp and isinstance(resp["emaitza"], list):
            return " ".join(
                str(it["lemma"]) for it in resp["emaitza"]
                if isinstance(it, dict) and "lemma" in it
            ).strip()

        for key in ("lemmas", "lemma", "result", "data", "tokens"):
            if key in resp:
                val = resp[key]
                if isinstance(val, str):
                    return val.strip()
                if isinstance(val, list):
                    return _format_lemma_response(val)
                return str(val).strip()

        return str(resp).strip()

    return str(resp).strip()



def _lemmatize_eu_text_chunked(text: str, max_chars: int = 3000, sleep_s: float = 0.05) -> str:
    chunks = _chunk_text(text, max_chars=max_chars)
    out_parts: List[str] = []

    for ch in chunks:
        try:
            resp = _post_json(URL_LEMMA, {"text": ch})

            if isinstance(resp, dict) and isinstance(resp.get("emaitza"), dict):
                out_parts.append(" ".join(resp["emaitza"].values()))
            else:
                # fallback por si cambia el formato
                out_parts.append(_format_lemma_response(resp))

        except Exception as e:
            print(f"[WARN] EU lemmatizazioak huts egin du ({type(e).__name__}): {e}")
            out_parts.append("")

        if sleep_s:
            time.sleep(sleep_s)

    return " ".join(p for p in out_parts if p).strip()



def _load_spacy_es(model: str = "es_core_news_md"):
    """
    spaCy pipeline kargatzen du (behin bakarrik).
    Lemmatizaziorako beharrezkoa: tagger/morph.
    Parser/NER desgaituta, azkartzeko.
    """
    return spacy.load(model, disable=["ner", "parser"])



def _lemmatize_es_spacy(text: str, nlp) -> str:
    """
    Gaztelania: spaCy bidez lematizatzen du, eta emaitza EU APIaren antzeko formatuan uzten du:
    - dena minuskulaz
    - puntuazioa eta hutsune tokenak kanpo
    - zuriunez banatutako lema-sekuentzia
    """
    if not text:
        return ""

    doc = nlp(text)
    lemmas: List[str] = []

    for t in doc:
        # EU adibideetan bezala: ez sartu puntuazioa/espazioak
        if t.is_space or t.is_punct:
            continue
        lemma = (t.lemma_ or t.text).strip()
        if not lemma:
            continue
        lemmas.append(lemma.lower())

    return " ".join(lemmas).strip()



# Funtzio nagusia
def lemak_lortu(
    df: pd.DataFrame,
    text_col: str = "Text",
    lang_col: str = "Language",
    output_tsv: str = "corpus_erauzketa_lemak.tsv",
    spacy_es_model: str = "es_core_news_md", # "es_core_news_lg" jarri daiteke, modelo handiagoa hartzeko (instalatu behar da aparte)
) -> pd.DataFrame:
    """
    Corpus osoa lematizatzen du:
    - TSV batean pixkanaka idazten du
    - Lemmas badago eta hutsik ez badago, errenkada saltatzen du
    - eu -> API (hitz.eus)
    - es -> spaCy (EU APIaren antzeko formatuan)
    """
    tmp_tsv = output_tsv + ".tmp"

    df_out = df.copy()
    if "Lemmas" not in df_out.columns:
        df_out["Lemmas"] = ""


    # spaCy (ES) pipelinea kargatu
    try:
        nlp_es = _load_spacy_es(spacy_es_model)
    except Exception as e:
        raise RuntimeError(
            f"Ezin izan da spaCy ES modeloa kargatu: {spacy_es_model}. "
            f"Instalatu hau: python -m spacy download {spacy_es_model}"
        ) from e
    

    with open(tmp_tsv, "w", encoding="utf-8") as f:
        f.write("\t".join(df_out.columns) + "\n")

        for i, row in df_out.iterrows():
            lemmas_existing = str(row.get("Lemmas", "")).strip()
            if lemmas_existing and lemmas_existing.lower() != "nan":
                f.write("\t".join(row.astype(str).tolist()) + "\n")
                continue

            text = str(row[text_col]).strip()
            lang = str(row[lang_col]).strip()

            if not text:
                row["Lemmas"] = ""
                f.write("\t".join(row.astype(str).tolist()) + "\n")
                continue

            if lang == "eu":
                lemma_str = _lemmatize_eu_text_chunked(text, max_chars=3000, sleep_s=0.05)
            elif lang == "es":
                lemma_str = _lemmatize_es_spacy(text, nlp_es)
            else:
                print(
                    f"[WARN] Hizkuntza ezezaguna: {lang!r} (onartzen direnak: 'eu', 'es'). "
                    "Ez da lematizaziorik egingo; 'Lemmas' hutsik."
                )
                lemma_str = ""

            row["Lemmas"] = lemma_str
            f.write("\t".join(row.astype(str).tolist()) + "\n")
            f.flush()

            if (i + 1) % 50 == 0:
                print(f"[INFO] {i+1}/{len(df_out)} errenkada prozesatuta")

    shutil.move(tmp_tsv, output_tsv)
    return df_out
