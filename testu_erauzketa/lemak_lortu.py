import subprocess
import pandas as pd
import os
import tempfile

# Lematizatzailea erabiltzeko script-ak
SH_SCRIPT_EU = "ses-lemma-main/basque/ses-udpipe/training-scripts/ood-xlm-roberta-large_eu_bdt_ses_udpipe_batch16_lr0.00005_decay0.01_epoc20.sh"
GET_LEMMAS_EU = "ses-lemma-main/basque/ses-udpipe/training-scripts/get_lemmas__.py"

SH_SCRIPT_ES = "ses-lemma-main/spanish/ses-udpipe/training-scripts/ood-xlm-roberta-large_es_gsd_ses_batch8_lr0.00002_decay0.1_epoc20.sh"
GET_LEMMAS_ES = "ses-lemma-main/spanish/ses-udpipe/training-scripts/get_lemmas__.py"



# Lemak lortzeko funtzioa
def lemak_lortu(df: pd.DataFrame) -> pd.DataFrame:
    """
    DataFrame batean dauden testuetako lemak lortzen ditu, hizkuntza kontuan hartuta (eu edo es).
    """

    lemak_total = []

    # Lerro bakoitzeko
    for idx, row in df.iterrows():
        text = row["Text"]
        language_blocks = row["Language"].split("<PARRAFO/>")
        text_blocks = text.split("<PARRAFO/>")

        assert len(language_blocks) == len(text_blocks), "Paragrafo kopurua ez dator bat"

        lemmas_parrafoak = []

        # Paragrafo bakoitzeko
        for lang, paragraph in zip(language_blocks, text_blocks):
            paragraph = paragraph.strip()
            if not paragraph:
                lemmas_parrafoak.append("")
                continue

            # Testua fitxategi tenporalean gorde
            with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
                for word in paragraph.split():
                    # SES "ez egin ezer" formatua
                    tmp_file.write(f"{word}\t↓0;d¦\n")
                tmp_path = tmp_file.name

            # Hizkuntza arabera script-a aukeratu
            if lang == "eu":
                sh_script = SH_SCRIPT_EU
                get_lemmas_script = GET_LEMMAS_EU
            else: # lang == "es"
                sh_script = SH_SCRIPT_ES
                get_lemmas_script = GET_LEMMAS_ES

            # SES modeloa exekutatu bash bidez
            subprocess.run(["bash", sh_script], check=True)

            # Lemmak lortu
            lemmas_output = subprocess.run(
                ["python3", get_lemmas_script, tmp_path],
                capture_output=True,
                text=True,
                check=True
            )

            # Lerro bakoitza hutsunearekin batu
            lemmas_parrafoak.append(" ".join(lemmas_output.stdout.strip().split("\n")))

            # Fitxategi tenporala ezabatu
            os.remove(tmp_path)

        # Paragrafo guztiak berriro batu
        lemak_total.append("<PARRAFO/>".join(lemmas_parrafoak))

    # DataFrame-a eguneratu
    df["Lemmas"] = lemak_total
    return df
