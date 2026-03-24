import os, re, sys
from langdetect import detect
import pandas as pd
import csv

# |----------------------------------------------------------------------------------------------------|
# |----------------------------------- KONFIGURAZIOA ETA METADATUAK -----------------------------------|
# |----------------------------------------------------------------------------------------------------|

def norm_name(s):
    """
    Izen bat normalizatzen du konparazioetarako:
    - Hasierako eta amaierako zuriuneak kentzen ditu
    - Minuskulak erabiltzen ditu
    - Tarteko zuriune bikoitzak bakar batean bihurtzen ditu

    Helburua izenen arteko konparazioak sendoagoak izatea da
    (adibidez: maiuskulak/minuskulak edo zuriune desberdinak ez eragitea).

    Parametroak
    ----------
    s : str
        Normalizatu beharreko testua (izena)

    Return
    ------
    str
        Normalizatutako izena (minuskulaz eta zuriune garbiekin)
    """
    return " ".join(str(s).strip().lower().split())

# Sailburuen genero-hiztegia (formatua: izena:generoa) kargatzen da, fitxategia existitzen bada
sailburuak = {}
GENERO_FPATH = os.path.join(os.path.dirname(__file__), "sailburu_genero.txt")

if os.path.exists(GENERO_FPATH):
    for line in open(GENERO_FPATH, encoding="utf-8"):
        sb, g = line.strip().split(":")
        sailburuak[norm_name(sb)] = g
else:
    print("Oharra: 'sailburu_genero.txt' ez da aurkitu. Generoa 'N' izango da lehenetsita.")

# Sailburuen jaiotza-hiztegia (formatua: izena\tjaiotza) kargatzen da, fitxategia existitzen bada
sailburu_birth = {}
BIRTH_FPATH = os.path.join(os.path.dirname(__file__), "sailburu_birth.txt")

if os.path.exists(BIRTH_FPATH):
    for line in open(BIRTH_FPATH, encoding="utf-8"):
        zat = line.strip().split("\t")
        if len(zat) >= 2:
            sb, b = zat[0], zat[1]
            sailburu_birth[norm_name(sb)] = b
else:
    print("Oharra: 'sailburu_birth.txt' ez da aurkitu. Birth balioa hutsik izango da lehenetsita.")

# Sailburuen alderdi-hiztegia (formatua: izena\talderdia) kargatzen da, fitxategia existitzen bada
sailburu_party = {}
PARTY_FPATH = os.path.join(os.path.dirname(__file__), "sailburu_party.txt")

if os.path.exists(PARTY_FPATH):
    for line in open(PARTY_FPATH, encoding="utf-8"):
        zat = line.strip().split("\t")
        if len(zat) >= 2:
            sb, p = zat[0], zat[1]
            sailburu_party[norm_name(sb)] = p
else:
    print("Oharra: 'sailburu_party.txt' ez da aurkitu. Party balioa hutsik izango da lehenetsita.")





def corpusa_prozesatu(corpus_path):
    """
    corpus_path karpetako .txt fitxategi guztiak prozesatzen ditu eta
    hitzaldi-paragrafo bakoitzaren informazioa (metadata + testua) 
    itzultzen du erregistro zerrenda moduan.
    """
    erregistroak = []
    speech_id = 0

    for folder in os.listdir(corpus_path):
        folder_path = os.path.join(corpus_path, folder)
        if not os.path.isdir(folder_path):
            continue  # Ez bada karpeta, saltatu

        for fname in os.listdir(folder_path):
            if not fname.endswith(".txt"):
                continue  # Soilik .txt fitxategiak prozesatu

            file_path = os.path.join(folder_path, fname)
            print(f"Prozesatzen: {file_path}")

            i = 0
            lehena = True
            bukaera = False
            parrafo = False
            testua = ""
            hizlaria = ""
            generoa = ""
            birth = ""
            party = ""
            hizkuntza = ""
            h_id = 0

            for line in open(file_path, encoding="utf-8"):
                line = line.strip()
                sys.stdout.write(f"\r{i} ")
                sys.stdout.flush()
                i += 1

                # Bukaera edo balio gabeko lerroak
                if bukaera or "PAGE" in line or "Comienzo de la cinta" in line:
                    continue

                if lehena:
                    # Lehenengo lerrotik data ateratzen saiatu
                    lehena = False
                    zatia = " ".join(line.split(" ")[:3])
                    array = [i for i, s in enumerate(zatia) if s.isdigit()]
                    if array:
                        azkena = array.pop() + 1
                        data = zatia[:azkena]
                        h_id = 0
                    else:
                        data = fname.split(".")[0]
                        h_id = 0
                else:
                    if line:
                        # Amaierako markak
                        if parrafo and (
                            "amaiera ematen zaio" in line.lower()
                            or "se da por finalizada la sesi" in line.lower()
                            or "se levanta la sesi" in line.lower()
                            or "amaitu da bilkura" in line.lower()
                            or "amaiera ematen diot" in line.lower()
                            or "bilkurari amaiera ematen" in line.lower()
                            or "plenoa amaitzen da" in line.lower()
                            or "plenoa bukatutzat geratzen da" in line.lower()
                            or "bilkura amaitzen dugu" in line.lower()
                            or "amaituta gelditzen d" in line.lower()
                            or "amaituta geratzen d" in line.lower()
                            or "amaitutzat ematen d" in line.lower()
                            or "bukatutzat ematen d" in line.lower()
                            or "bilkura ere amaitzen d" in line.lower()
                            or "amaitzen da osoko bilkura" in line.lower()
                            or "bilkura amaitzen da" in line.lower()
                        ):
                            bukaera = True
                            erregistroak.append({
                                "Date": data,
                                "Speech_id": speech_id,
                                "Text_id": h_id,
                                "Speaker": hizlaria,
                                "Birth": birth,
                                "Gender": generoa,
                                "Party": party,
                                "Language": hizkuntza,
                                "Text": testua,
                                "Lemmas": "",
                                "Lemmas_stw": "",
                                "Entities": "",
                                "Entities_stw": ""
                            })
                            hizlaria, generoa, birth, party, testua, hizkuntza = "", "", "", "", "", ""

                        # Hizlari berria identifikatu
                        if ":" in line and parrafo:
                            zatiak = line.split(":")
                            hiz = zatiak[0]

                            berria = False
                            if hiz.startswith("LEHENDAKARI") or hiz.startswith("La PRESIDENTA") or hiz.startswith("LEGEBILTZARREKO LEHENDAKARI"):
                                if hizlaria:
                                    erregistroak.append({
                                        "Date": data,
                                        "Speech_id": speech_id,
                                        "Text_id": h_id,
                                        "Speaker": hizlaria,
                                        "Birth": birth,
                                        "Gender": generoa,
                                        "Party": party,
                                        "Language": hizkuntza,
                                        "Text": testua,
                                        "Lemmas": "",
                                        "Lemmas_stw": "",
                                        "Entities": "",
                                        "Entities_stw": ""
                                    })
                                if "(" in hiz:
                                    lehendakari_izena = hiz.split("(")[1].split(")")[0]
                                    hizlaria = lehendakari_izena + " LEHENDAKARIA"
                                    generoa = "E"
                                else:
                                    hizlaria = hiz + " LEHENDAKARIA"
                                    generoa = "E"
                                birth = sailburu_birth.get(norm_name(hizlaria), "")
                                party = sailburu_party.get(norm_name(hizlaria), "")
                                berria = True
                                h_id += 1

                            elif (hiz.split()[-1].lower() in ["andreak", "andrea", "andereak", "anderea", "adreak"] or hiz.startswith("La Sra.")) and "," not in hiz:
                                erregistroak.append({
                                    "Date": data,
                                    "Speech_id": speech_id,
                                    "Text_id": h_id,
                                    "Speaker": hizlaria,
                                    "Birth": birth,
                                    "Gender": generoa,
                                    "Party": party,
                                    "Language": hizkuntza,
                                    "Text": testua,
                                    "Lemmas": "",
                                    "Lemmas_stw": "",
                                    "Entities": "",
                                    "Entities_stw": ""
                                })
                                generoa = "E"
                                if hiz.startswith("La Sra."):
                                    hizlaria = " ".join(hiz.split()[2:])
                                else:
                                    hizlaria = " ".join(hiz.split()[:-1])
                                birth = sailburu_birth.get(norm_name(hizlaria), "")
                                party = sailburu_party.get(norm_name(hizlaria), "")
                                berria = True
                                h_id += 1

                            elif (hiz.split()[-1].lower() in ["jaunak", "jauna"] or hiz.startswith("El Sr.")) and "," not in hiz:
                                erregistroak.append({
                                    "Date": data,
                                    "Speech_id": speech_id,
                                    "Text_id": h_id,
                                    "Speaker": hizlaria,
                                    "Birth": birth,
                                    "Gender": generoa,
                                    "Party": party,
                                    "Language": hizkuntza,
                                    "Text": testua,
                                    "Lemmas": "",
                                    "Lemmas_stw": "",
                                    "Entities": "",
                                    "Entities_stw": ""
                                })
                                generoa = "G"
                                if hiz.startswith("El Sr."):
                                    hizlaria = " ".join(hiz.split()[2:])
                                else:
                                    hizlaria = " ".join(hiz.split()[:-1])
                                birth = sailburu_birth.get(norm_name(hizlaria), "")
                                party = sailburu_party.get(norm_name(hizlaria), "")
                                berria = True
                                h_id += 1

                            elif (
                                len(hiz.split(" ")[0]) > 2
                                and hiz.split(" ")[0] != "ETA"
                                and hiz.split(" ")[0].isupper()
                                and "," not in hiz
                                and "?" not in hiz
                                and len(hiz) < 120
                                and not line.startswith('"')
                            ):
                                erregistroak.append({
                                    "Date": data,
                                    "Speech_id": speech_id,
                                    "Text_id": h_id,
                                    "Speaker": hizlaria,
                                    "Birth": birth,
                                    "Gender": generoa,
                                    "Party": party,
                                    "Language": hizkuntza,
                                    "Text": testua,
                                    "Lemmas": "",
                                    "Lemmas_stw": "",
                                    "Entities": "",
                                    "Entities_stw": ""
                                })
                                hizlaria = hiz
                                generoa = sailburuak.get(norm_name(hizlaria), "N")
                                birth = sailburu_birth.get(norm_name(hizlaria), "")
                                party = sailburu_party.get(norm_name(hizlaria), "")
                                berria = True
                                h_id += 1

                            if berria:
                                testua = ":".join(zatiak[1:])
                                hizkuntza = ""
                                berria = False
                            else:
                                testua += " " + line
                        else:
                            testua += " " + line

                        parrafo = False
                    else:
                        # Parrafo hutsak -> hizkuntza detekzioa
                        parrafo = True
                        azkena = testua.split("<PARRAFO/>")[-1]
                        try:
                            azk_hiz_d = detect(azkena)
                        except:
                            azk_hiz_d = ""
                        if azk_hiz_d != "es":
                            azk_hiz_d = "eu"
                        hizkuntza += azk_hiz_d + "<PARRAFO/>"
                        testua += "<PARRAFO/>"

            speech_id += 1

    return erregistroak



# Funtzio hau gehitu da estruktura argiago bat edukitzeko.
def split_parrafoak(df, group_cols=['Speech_id'], token='<PARRAFO/>', on_mismatch='pad'):
    """
    <PARRAFO/> token bidez bereizitako paragrafoak errenkada berrietan banatzen ditu,
    eta Language eta Text zutabeak lerrokatuta mantentzen ditu.

    Parametroak
    ----------
    df : pd.DataFrame
        Jatorrizko DataFrame-a.
    group_cols : tuple/list edo None
        Zein zutaberen arabera berriro kalkulatu Text_id (cumcount erabiliz).
        None bada, Text_id globalki zenbatzen da.
    token : str
        Paragrafoen bereizlea; lehenetsia '<PARRAFO/>'.
    on_mismatch : {'pad','repeat_last','error'}
        Zer egin hizkuntzen eta paragrafoen kopurua ez badator bat:
        - 'pad': falta den hizkuntza NA-rekin bete
        - 'repeat_last': azken hizkuntza ezaguna errepikatu
        - 'error': errorea jaurti

    Return
    ------
    pd.DataFrame
        Paragrafo bakoitza errenkada batean duen DataFrame-a.
    """
    df = df.copy()

    rows_out = []
    for _, row in df.iterrows():
        text_raw = '' if pd.isna(row['Text']) else str(row['Text'])
        lang_raw = '' if pd.isna(row['Language']) else str(row['Language'])

        texts = text_raw.split(token)      
        langs = lang_raw.split(token)

        # Amaierako hutsune komunak kendu (token-a amaieran egoteagatik sortuak)
        while texts and langs and texts[-1].strip() == '' and langs[-1].strip() == '':
            texts.pop()
            langs.pop()

        # Elementu bakoitzeko zuriuneak garbitu
        texts = [t.strip() for t in texts]
        langs = [l.strip() for l in langs]

        # Testu guztia hutsik badago, errenkada saltatu
        if all(t == '' for t in texts):
            continue

        # Desorekak kudeatu (paragrafo kopurua != hizkuntza kopurua)
        n_text = len(texts)
        n_lang = len(langs)

        if n_text != n_lang:
            if on_mismatch == 'error':
                raise ValueError(
                    f"Desoreka errenkadan: #Text={n_text} #Language={n_lang} "
                    f"(jatorrizko Text_id={row.get('Text_id', None)})"
                )
            elif on_mismatch == 'repeat_last' and n_lang > 0 and n_text > n_lang:
                # Azken hizkuntza errepikatu
                langs = langs + [langs[-1]] * (n_text - n_lang)
            elif on_mismatch == 'pad' and n_text > n_lang:
                # Falta diren hizkuntzak NA-rekin bete
                langs = langs + [pd.NA] * (n_text - n_lang)
            elif n_lang > n_text:
                # Hizkuntza gehiago badira testuak baino, moztu
                langs = langs[:n_text]

        # Errenkada berriak sortu (paragrafo bakoitzeko)
        for lang, txt in zip(langs, texts):
            if txt == '':
                continue
            new_row = row.to_dict()
            new_row['Language'] = lang
            new_row['Text'] = txt
            rows_out.append(new_row)

    out = pd.DataFrame(rows_out)

    # Text_id berriro kalkulatu
    if group_cols is None:
        out['Text_id'] = range(len(out))
    else:
        out['Text_id'] = out.groupby(list(group_cols), sort=False).cumcount()

    return out



def language_normalizatu(df: pd.DataFrame, text_col: str = "Text", lang_col: str = "Language") -> pd.DataFrame:
    """
    Language zutabea normalizatzen du:
    - Balioa 'eu' edo 'es' bada, bere horretan mantentzen da.
    - Bestela, testuaren hizkuntza detektatzen da eta 'es' ez bada, 'eu' ezartzen da.

    Parametroak
    ----------
    df : pd.DataFrame
        Normalizatu beharreko DataFrame-a.
    text_col : str
        Hizkuntza detektatzeko erabiliko den testu-zutabea.
    lang_col : str
        Normalizatu beharreko hizkuntza-zutabea.

    Return
    ------
    pd.DataFrame
        Hizkuntza zutabea normalizatuta duen DataFrame-a.
    """
    def fix_lang(row) -> str:
        lang = str(row.get(lang_col, "")).strip().lower()
        if lang in ("eu", "es"):
            return lang

        text = str(row.get(text_col, "")).strip()
        if not text:
            return "" # Testurik ez badago, balio hutsa mantentzen da

        try:
            d = detect(text)
        except Exception:
            d = ""

        # 'es' ez bada, 'eu' ezartzen da
        if d != "es":
            d = "eu"
        return d

    df[lang_col] = df.apply(fix_lang, axis=1)
    return df



def merge_lemmas_entities(
    lemak_path="corpus_erauzketa_lemak.tsv",
    entities_path="corpus_erauzketa_entities.tsv",
    out_path="corpus_erauzketa_lemak_entities.tsv",
):
    """
    Lemak eta entitateak TSV bakarrean bateratzen ditu, errenkaden posizioaren arabera.

    Baldintzak:
    - Bi TSVek errenkada kopuru bera izan behar dute.
    - Entitateak df_e['Entities'] zutabetik hartzen dira.

    Parametroak
    ----------
    lemak_path : str
        Lemak dituen TSV fitxategiaren bidea.
    entities_path : str
        Entitateak dituen TSV fitxategiaren bidea.
    out_path : str
        Irteerako TSV fitxategiaren bidea.

    Return
    ------
    pd.DataFrame
        Lemak + Entities zutabeak bateratuta dituen DataFrame-a.
    """
    # TSV-ak kargatu
    df_l = pd.read_csv(
        lemak_path,
        sep="\t",
        dtype=str,
        keep_default_na=False,
        engine="python",
        quoting=csv.QUOTE_NONE
    )

    df_e = pd.read_csv(
        entities_path,
        sep="\t",
        dtype=str,
        keep_default_na=False,
        engine="python",
        quoting=csv.QUOTE_NONE
    )

    # Errenkada kopurua berdina dela egiaztatu
    if len(df_l) != len(df_e):
        raise ValueError(
            f"Errenkada kopurua ez dator bat: lemak={len(df_l)} | entities={len(df_e)}"
        )

    # Entities zutabea zuzenean itsatsi errenkaden posizioaren arabera
    df_l["Entities"] = df_e["Entities"].values

    # Emaitza gorde
    df_l.to_csv(out_path, sep="\t", index=False, encoding="utf-8", quoting=csv.QUOTE_NONE)

    print(f"TSV berria sortuta: {out_path}")
    print(f"Errenkadak: {len(df_l)}")

    return df_l