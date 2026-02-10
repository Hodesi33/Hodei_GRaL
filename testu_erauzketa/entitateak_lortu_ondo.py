# entitateak_lortu.py
from __future__ import annotations

from typing import Any, Dict, List, Union
import json
import os
import random
import shutil
import time

import pandas as pd
import requests

URL_NERC = "https://zerbitzuak.hitz.eus/lema/api/nerc"

HEADERS = {
    "accept": "*/*",
    "Content-Type": "application/json",
}


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

        # Ez bada amaiera, saiatu azken zuriunean mozten
        if end < n:
            cut = text.rfind(" ", start, end)
            # Zati txikiegiak ekiditeko
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
    POST sendoa: berriro saiatzen da 429 eta 5xx erroreetan, eta sare/timeout erroreetan.
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


def _format_entities_as_list(resp: Union[Dict[str, Any], List[Any], str]) -> str:
    """
    NER APIaren erantzuna zerrenda normalizatu batean bihurtzen du:
    [
      {"text": "...", "label": "PER"},
      ...
    ]
    Itzultzen du: JSON string.
    """
    if isinstance(resp, str):
        s = resp.strip()
        try:
            resp = json.loads(s)
        except Exception:
            return "[]"

    if isinstance(resp, dict) and "emaitza" in resp and isinstance(resp["emaitza"], dict):
        entities = [{"text": ent, "label": lab} for ent, lab in resp["emaitza"].items()]
        return json.dumps(entities, ensure_ascii=False)

    # Baliteke APIak beste eskema bat bidaltzea
    return "[]"


def _merge_entity_chunks(entity_json_strings: List[str]) -> str:
    """
    Chunk bakoitzeko entitate-zerrendak batu (JSON string-ak -> lista bakarra).
    """
    all_entities: List[Dict[str, Any]] = []

    for s in entity_json_strings:
        if not s:
            continue
        try:
            obj = json.loads(s)
        except Exception:
            continue

        if isinstance(obj, list):
            # Elementu bakoitza {"text":..., "label":...} dela espero dugu
            all_entities.extend(obj)

    return json.dumps(all_entities, ensure_ascii=False)


def _entities_text_chunked(text: str, max_chars: int = 3000, sleep_s: float = 0.05) -> str:
    """
    Testu bakar bat NER bidez prozesatzen du, zatika (API muga saihesteko).
    Itzultzen du: JSON string -> [{"text":...,"label":...}, ...]
    """
    chunks = _chunk_text(text, max_chars=max_chars)
    out_entity_lists: List[str] = []

    for ch in chunks:
        try:
            resp = _post_json(URL_NERC, {"text": ch})
            out_entity_lists.append(_format_entities_as_list(resp))
        except Exception as e:
            print(f"[WARN] NER chunk-ak huts egin du ({type(e).__name__}): {e}")
            out_entity_lists.append("[]")

        if sleep_s:
            time.sleep(sleep_s)

    if len(out_entity_lists) == 1:
        return out_entity_lists[0]

    return _merge_entity_chunks(out_entity_lists)


def entitateak_lortu(
    df: pd.DataFrame,
    text_col: str = "Text",
    lang_col: str = "Language",
    output_tsv: str = "corpus_erauzketa_entities.tsv",
) -> pd.DataFrame:
    """
    Entitateak (NER) lortzen ditu:
    - TSV batean pixkanaka idazten du (segurtasunez)
    - TSV badago, reanuda egiten du
    - Entities badago eta hutsik ez badago, errenkada saltatzen du
    - euskarazko (lang == 'eu') errenkadak bakarrik prozesatzen ditu
    """
    tmp_tsv = output_tsv + ".tmp"

    if os.path.exists(output_tsv):
        print("[INFO] Aurreko TSV-a aurkitu da, jarraitzen...")
        df_out = pd.read_csv(output_tsv, sep="\t", dtype=str)
        if "Entities" not in df_out.columns:
            df_out["Entities"] = ""
    else:
        df_out = df.copy()
        df_out["Entities"] = ""

    with open(tmp_tsv, "w", encoding="utf-8") as f:
        f.write("\t".join(df_out.columns) + "\n")

        for i, row in df_out.iterrows():
            entities_existing = str(row.get("Entities", "")).strip()
            if entities_existing and entities_existing.lower() != "nan":
                f.write("\t".join(row.astype(str).tolist()) + "\n")
                continue

            text = str(row[text_col]).strip()
            lang = str(row[lang_col]).strip()

            if not text or lang != "eu":
                row["Entities"] = "[]"
                f.write("\t".join(row.astype(str).tolist()) + "\n")
                continue

            entities_str = _entities_text_chunked(text, max_chars=3000, sleep_s=0.05)
            row["Entities"] = entities_str

            f.write("\t".join(row.astype(str).tolist()) + "\n")
            f.flush()

            if (i + 1) % 50 == 0:
                print(f"[INFO] {i+1}/{len(df_out)} errenkada prozesatuta")

    shutil.move(tmp_tsv, output_tsv)
    return df_out
