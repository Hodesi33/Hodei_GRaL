import os, re, sys
from langdetect import detect
import pandas as pd
import csv
from pathlib import Path


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


# Sailburuen genero-hiztegia kargatu
sailburuak = {}
GENERO_FPATH = os.path.join(os.path.dirname(__file__), "sailburu_gender.tsv")

if os.path.exists(GENERO_FPATH):
    for i, line in enumerate(open(GENERO_FPATH, encoding="utf-8")):
        zat = line.strip().split("\t")
        if len(zat) >= 2:
            sb, g = zat[0].strip(), zat[1].strip().upper()

            # Goiburua saltatu
            if i == 0 and sb.lower() == "speaker" and g.lower() == "gender":
                continue

            # Segurtasunagatik normalizatu
            if g == "F":
                g = "E"
            elif g == "M":
                g = "G"

            sailburuak[norm_name(sb)] = g
else:
    print("Oharra: 'sailburu_gender.tsv' ez da aurkitu. Generoa 'N' izango da lehenetsita.")


# Sailburuen jaiotza-hiztegia kargatu
sailburu_birth = {}
BIRTH_FPATH = os.path.join(os.path.dirname(__file__), "sailburu_birth.tsv")

if os.path.exists(BIRTH_FPATH):
    for i, line in enumerate(open(BIRTH_FPATH, encoding="utf-8")):
        zat = line.strip().split("\t")
        if len(zat) >= 2:
            sb, b = zat[0].strip(), zat[1].strip()

            # Goiburua saltatu
            if i == 0 and sb.lower() == "speaker" and b.lower() == "birth":
                continue

            sailburu_birth[norm_name(sb)] = b
else:
    print("Oharra: 'sailburu_birth.tsv' ez da aurkitu. Birth balioa hutsik izango da lehenetsita.")


# Sailburuen alderdi-hiztegia kargatu
sailburu_party = {}
PARTY_FPATH = os.path.join(os.path.dirname(__file__), "sailburu_party.tsv")

if os.path.exists(PARTY_FPATH):
    for i, line in enumerate(open(PARTY_FPATH, encoding="utf-8")):
        zat = line.strip().split("\t")
        if len(zat) >= 2:
            sb, p = zat[0].strip(), zat[1].strip()

            # Goiburua saltatu
            if i == 0 and sb.lower() == "speaker" and p.lower() == "party":
                continue

            sailburu_party[norm_name(sb)] = p
else:
    print("Oharra: 'sailburu_party.tsv' ez da aurkitu. Party balioa hutsik izango da lehenetsita.")


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
            continue

        for fname in os.listdir(folder_path):
            if not fname.endswith(".txt"):
                continue

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

            # Fitxategi barruan azken lehendakari ezaguna gordetzeko
            azken_lehendakaria = ""

            for line in open(file_path, encoding="utf-8"):
                line = line.strip()
                sys.stdout.write(f"\r{i} ")
                sys.stdout.flush()
                i += 1

                # Bukaera edo balio gabeko lerroak
                if bukaera or "PAGE" in line or "Comienzo de la cinta" in line:
                    continue

                if lehena:
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
                            hiz = zatiak[0].strip()

                            berria = False

                            # Lehendakari/presidenta kasuak
                            if (
                                hiz.startswith("LEHENDAKARI")
                                or hiz.startswith("La PRESIDENTA")
                                or hiz.startswith("LEGEBILTZARREKO LEHENDAKARI")
                            ):
                                speaker_tmp = ""

                                # Uneko hizlaria itxi, berria sortu aurretik
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

                                # Izena parentesi artean badator, hori hartu
                                if "(" in hiz and ")" in hiz:
                                    speaker_tmp = hiz.split("(", 1)[1].split(")", 1)[0].strip()
                                    azken_lehendakaria = speaker_tmp

                                # Bestela, azken lehendakari ezaguna berrerabili
                                elif azken_lehendakaria:
                                    speaker_tmp = azken_lehendakaria

                                # Speaker balioduna badago, osatu
                                if speaker_tmp:
                                    hizlaria = speaker_tmp + " LEHENDAKARIA"
                                else:
                                    # Ez da speaker artifizial okerrik sortzen
                                    hizlaria = "LEHENDAKARIA"

                                generoa = sailburuak.get(norm_name(hizlaria), "E")
                                birth = sailburu_birth.get(norm_name(hizlaria), "")
                                party = sailburu_party.get(norm_name(hizlaria), "")
                                berria = True
                                h_id += 1

                            elif (
                                hiz.split()[-1].lower() in ["andreak", "andrea", "andereak", "anderea", "adreak"]
                                or hiz.startswith("La Sra.")
                            ) and "," not in hiz:
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
                                generoa = "E"
                                if hiz.startswith("La Sra."):
                                    hizlaria = " ".join(hiz.split()[2:])
                                else:
                                    hizlaria = " ".join(hiz.split()[:-1])
                                birth = sailburu_birth.get(norm_name(hizlaria), "")
                                party = sailburu_party.get(norm_name(hizlaria), "")
                                berria = True
                                h_id += 1

                            elif (
                                hiz.split()[-1].lower() in ["jaunak", "jauna"]
                                or hiz.startswith("El Sr.")
                            ) and "," not in hiz:
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
                        # Paragrafo hutsak -> hizkuntza detekzioa
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

            # Fitxategi amaieran azken hizlaria ere gorde
            if hizlaria and testua.strip():
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

            speech_id += 1

    return erregistroak


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

        while texts and langs and texts[-1].strip() == '' and langs[-1].strip() == '':
            texts.pop()
            langs.pop()

        texts = [t.strip() for t in texts]
        langs = [l.strip() for l in langs]

        if all(t == '' for t in texts):
            continue

        n_text = len(texts)
        n_lang = len(langs)

        if n_text != n_lang:
            if on_mismatch == 'error':
                raise ValueError(
                    f"Desoreka errenkadan: #Text={n_text} #Language={n_lang} "
                    f"(jatorrizko Text_id={row.get('Text_id', None)})"
                )
            elif on_mismatch == 'repeat_last' and n_lang > 0 and n_text > n_lang:
                langs = langs + [langs[-1]] * (n_text - n_lang)
            elif on_mismatch == 'pad' and n_text > n_lang:
                langs = langs + [pd.NA] * (n_text - n_lang)
            elif n_lang > n_text:
                langs = langs[:n_text]

        for lang, txt in zip(langs, texts):
            if txt == '':
                continue
            new_row = row.to_dict()
            new_row['Language'] = lang
            new_row['Text'] = txt
            rows_out.append(new_row)

    out = pd.DataFrame(rows_out)

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
            return ""

        try:
            d = detect(text)
        except Exception:
            d = ""

        if d != "es":
            d = "eu"
        return d

    df[lang_col] = df.apply(fix_lang, axis=1)
    return df



def date_normalizatu(df: pd.DataFrame, date_col: str = "Date", valid_years=None) -> pd.DataFrame:
    """
    Date zutabeko balioak YYYY-MM-DD formatura bihurtzen saiatzen da.

    - Jatorrizko balioa mantentzen da ezin bada bihurtu.
    - valid_years ematen bada, urteak filtratzen dira.
    - valid_years=None bada → EZ dago mugarik.

    Parametroak
    ----------
    df : pd.DataFrame
    date_col : str
    valid_years : set edo None

    Return
    ------
    pd.DataFrame
    """

    df = df.copy()

    month_map = {
        "enero": "01", "urtarrila": "01",
        "febrero": "02", "otsaila": "02",
        "marzo": "03", "martxoa": "03",
        "abril": "04", "apirila": "04",
        "mayo": "05", "maiatza": "05",
        "junio": "06", "ekaina": "06",
        "julio": "07", "uztaila": "07",
        "agosto": "08", "abuztua": "08",
        "septiembre": "09", "setiembre": "09", "iraila": "09",
        "octubre": "10", "urria": "10",
        "noviembre": "11", "azaroa": "11",
        "diciembre": "12", "abendua": "12",
    }

    def year_valid(y):
        if valid_years is None:
            return True
        return y in valid_years

    def normalizatu(x):
        if pd.isna(x):
            return x

        s = str(x).strip()
        if not s:
            return s

        s_low = s.lower()

        # 1) YYYY-MM-DD / YYYY/MM/DD / YYYY_MM_DD
        m = re.search(r"\b(\d{4})[-/_](\d{1,2})[-/_](\d{1,2})\b", s_low)
        if m:
            y, mo, d = map(int, m.groups())
            if year_valid(y):
                return f"{y:04d}-{mo:02d}-{d:02d}"

        # 2) DD-MM-YYYY / DD/MM/YYYY
        m = re.search(r"\b(\d{1,2})[-/_](\d{1,2})[-/_](\d{4})\b", s_low)
        if m:
            d, mo, y = map(int, m.groups())
            if year_valid(y):
                return f"{y:04d}-{mo:02d}-{d:02d}"

        # 3) YYYYMMDD
        m = re.search(r"\b(\d{4})(\d{2})(\d{2})\b", s_low)
        if m:
            y, mo, d = map(int, m.groups())
            if year_valid(y):
                return f"{y:04d}-{mo:02d}-{d:02d}"

        # 4) P231014 edo 231014 -> DDMMYY
        m = re.search(r"(?:^|[^0-9])[pP]?(\d{2})(\d{2})(\d{2})(?:[^0-9]|$)", s)
        if m:
            d, mo, yy = map(int, m.groups())
            y = 2000 + yy if yy <= 30 else 1900 + yy
            if year_valid(y):
                return f"{y:04d}-{mo:02d}-{d:02d}"

        # 5) "23 octubre 2014"
        m = re.search(
            r"\b(\d{1,2})\D+(" + "|".join(month_map.keys()) + r")\D+(\d{4})\b",
            s_low
        )
        if m:
            d = int(m.group(1))
            mo = int(month_map[m.group(2)])
            y = int(m.group(3))
            if year_valid(y):
                return f"{y:04d}-{mo:02d}-{d:02d}"

        # 6) "2014 octubre 23"
        m = re.search(
            r"\b(\d{4})\D+(" + "|".join(month_map.keys()) + r")\D+(\d{1,2})\b",
            s_low
        )
        if m:
            y = int(m.group(1))
            mo = int(month_map[m.group(2)])
            d = int(m.group(3))
            if year_valid(y):
                return f"{y:04d}-{mo:02d}-{d:02d}"

        return s

    df[date_col] = df[date_col].apply(normalizatu)

    mask_ok = df[date_col].astype(str).str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)

    print(f"Date normalizatuta: {mask_ok.sum()}")
    print(f"Date konpondu gabe: {(~mask_ok).sum()}")

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

    if len(df_l) != len(df_e):
        raise ValueError(
            f"Errenkada kopurua ez dator bat: lemak={len(df_l)} | entities={len(df_e)}"
        )

    df_l["Entities"] = df_e["Entities"].values
    df_l.to_csv(out_path, sep="\t", index=False, encoding="utf-8", quoting=csv.QUOTE_NONE)

    print(f"TSV berria sortuta: {out_path}")
    print(f"Errenkadak: {len(df_l)}")

    return df_l


def osatu_speaker_datuak(df, birth_path=None, gender_path=None, party_path=None):
    """
    DataFrame bateko Birth, Gender eta Party zutabeetako hutsuneak osatzen ditu,
    Speaker izena gako gisa erabilita.

    Parametroak
    ----------
    df : pd.DataFrame
        Speaker, Birth, Gender eta Party zutabeak dituen DataFrame-a.
    birth_path : str edo None
        Speaker\tBirth fitxategiaren bidea.
    gender_path : str edo None
        Speaker\tGender fitxategiaren bidea.
    party_path : str edo None
        Speaker\tParty fitxategiaren bidea.

    Return
    ------
    pd.DataFrame
        Datuak osatuta dituen DataFrame-a.
    """
    df = df.copy()

    for col in ["Birth", "Gender", "Party"]:
        if col not in df.columns:
            df[col] = ""

    if "Speaker" not in df.columns:
        raise ValueError("DataFrame-ak 'Speaker' zutabea izan behar du")

    def balio_hutsa(x):
        if pd.isna(x):
            return True
        x = str(x).strip()
        return x == "" or x.lower() in {"nan", "none", "<na>"} or x == "-"

    df["_speaker_key"] = df["Speaker"].apply(norm_name)

    # Birth
    birth_dict = {}
    if birth_path is not None:
        if Path(birth_path).exists():
            for i, line in enumerate(open(birth_path, encoding="utf-8")):
                zat = line.rstrip("\n").split("\t")
                if len(zat) >= 2:
                    speaker, birth = zat[0].strip(), zat[1].strip()
                    if i == 0 and speaker.lower() == "speaker":
                        continue
                    if speaker and birth and speaker != "-":
                        birth_dict[norm_name(speaker)] = birth
        else:
            print(f"Oharra: '{birth_path}' ez da aurkitu.")

    # Gender
    gender_dict = {}
    if gender_path is not None:
        if Path(gender_path).exists():
            for i, line in enumerate(open(gender_path, encoding="utf-8")):
                zat = line.rstrip("\n").split("\t")
                if len(zat) >= 2:
                    speaker, gender = zat[0].strip(), zat[1].strip().upper()
                    if i == 0 and speaker.lower() == "speaker":
                        continue
                    if gender == "F":
                        gender = "E"
                    elif gender == "M":
                        gender = "G"
                    if speaker and gender and speaker != "-":
                        gender_dict[norm_name(speaker)] = gender
        else:
            print(f"Oharra: '{gender_path}' ez da aurkitu.")

    # Party
    party_dict = {}
    if party_path is not None:
        if Path(party_path).exists():
            for i, line in enumerate(open(party_path, encoding="utf-8")):
                zat = line.rstrip("\n").split("\t")
                if len(zat) >= 2:
                    speaker, party = zat[0].strip(), zat[1].strip()
                    if i == 0 and speaker.lower() == "speaker":
                        continue
                    if speaker and party and speaker != "-":
                        party_dict[norm_name(speaker)] = party
        else:
            print(f"Oharra: '{party_path}' ez da aurkitu.")

    birth_beteak = gender_beteak = party_beteak = 0

    for idx, row in df.iterrows():
        key = row["_speaker_key"]

        if birth_dict and balio_hutsa(row["Birth"]) and key in birth_dict:
            df.at[idx, "Birth"] = birth_dict[key]
            birth_beteak += 1

        if gender_dict and balio_hutsa(row["Gender"]) and key in gender_dict:
            df.at[idx, "Gender"] = gender_dict[key]
            gender_beteak += 1

        if party_dict and balio_hutsa(row["Party"]) and key in party_dict:
            df.at[idx, "Party"] = party_dict[key]
            party_beteak += 1

    print(f"Birth osatuak: {birth_beteak}")
    print(f"Gender osatuak: {gender_beteak}")
    print(f"Party osatuak: {party_beteak}")

    df = df.drop(columns=["_speaker_key"])
    return df
