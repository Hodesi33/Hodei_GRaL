import os, re, sys
from langdetect import detect

# Sailburuen hiztegia baldin badago (izena:generoa)
sailburuak = {}
GENERO_FPATH = os.path.join(os.path.dirname(__file__), "sailburu_genero.txt")

if os.path.exists(GENERO_FPATH):
    for line in open(GENERO_FPATH, encoding="utf-8"):
        sb, g = line.strip().split(":")
        sailburuak[sb] = g
else:
    print("Oharra: 'sailburu_genero.txt' ez da aurkitu. Generoa 'N' izango da lehenetsita.")


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
                                "Birth": "",
                                "Gender": generoa,
                                "Party": "",
                                "Language": hizkuntza,
                                "Text": testua,
                                "Lemmas": "",
                                "Lemmas_stw": "",
                                "Entities": "",
                                "Entities_stw": ""
                            })
                            hizlaria, generoa, testua, hizkuntza = "", "", "", ""

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
                                        "Birth": "",
                                        "Gender": generoa,
                                        "Party": "",
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
                                berria = True
                                h_id += 1

                            elif (hiz.split()[-1].lower() in ["andreak", "andrea", "andereak", "anderea", "adreak"] or hiz.startswith("La Sra.")) and "," not in hiz:
                                erregistroak.append({
                                    "Date": data,
                                    "Speech_id": speech_id,
                                    "Text_id": h_id,
                                    "Speaker": hizlaria,
                                    "Birth": "",
                                    "Gender": generoa,
                                    "Party": "",
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
                                berria = True
                                h_id += 1

                            elif (hiz.split()[-1].lower() in ["jaunak", "jauna"] or hiz.startswith("El Sr.")) and "," not in hiz:
                                erregistroak.append({
                                    "Date": data,
                                    "Speech_id": speech_id,
                                    "Text_id": h_id,
                                    "Speaker": hizlaria,
                                    "Birth": "",
                                    "Gender": generoa,
                                    "Party": "",
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
                                    "Birth": "",
                                    "Gender": generoa,
                                    "Party": "",
                                    "Language": hizkuntza,
                                    "Text": testua,
                                    "Lemmas": "",
                                    "Lemmas_stw": "",
                                    "Entities": "",
                                    "Entities_stw": ""
                                })
                                hizlaria = hiz
                                generoa = sailburuak.get(hizlaria, "N")
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
