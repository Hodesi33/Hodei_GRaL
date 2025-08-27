import subprocess
import pandas as pd
import os
import tempfile

# Entitateak lortzeko script-ak
SH_SCRIPT_EU = "ses-lemma-main/basque/ses-udpipe/training-scripts/ood-xlm-roberta-large_eu_bdt_ses_udpipe_batch16_lr0.00005_decay0.01_epoc20.sh"
SH_SCRIPT_ES = "ses-lemma-main/spanish/ses-udpipe/training-scripts/ood-xlm-roberta-large_es_gsd_ses_batch8_lr0.00002_decay0.1_epoc20.sh"

def entitateak_lortu(df: pd.DataFrame) -> pd.DataFrame:
    """
    DataFrame batean dauden testuetako entitateak lortzen ditu, hizkuntza kontuan hartuta (eu edo es).
    """

    entitateak_total = []

    # Lerro bakoitzeko
    for idx, row in df.iterrows():
        text = row["Text"]
        language_blocks = row["Language"].split("<PARRAFO/>")
        text_blocks = text.split("<PARRAFO/>")

        assert len(language_blocks) == len(text_blocks), "Paragrafo kopurua ez dator bat"

        entitateak_parrafoak = []

        # Paragrafo bakoitzeko
        for lang, paragraph in zip(language_blocks, text_blocks):
            paragraph = paragraph.strip()
            if not paragraph:
                entitateak_parrafoak.append("")
                continue

            # Testua fitxategi tenporalean gorde
            with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
                tmp_file.write(paragraph + "\n")
                tmp_path = tmp_file.name

            # Hizkuntza arabera script-a aukeratu
            if lang == "eu":
                sh_script = SH_SCRIPT_EU
            else:
                sh_script = SH_SCRIPT_ES

            # NER modeloa exekutatu bash bidez
            # Entitateak stdout bidez lortuko dira
            result = subprocess.run(
                ["bash", sh_script, tmp_path],
                capture_output=True,
                text=True,
                check=True
            )

            # Lerro bakoitza hutsunearekin batu (edo beste formatu egokia)
            entitateak_parrafoak.append(result.stdout.strip())

            # Fitxategi tenporala ezabatu
            os.remove(tmp_path)

        # Paragrafo guztiak berriro batu
        entitateak_total.append("<PARRAFO/>".join(entitateak_parrafoak))

    # DataFrame-a eguneratu
    df["Entities"] = entitateak_total
    return df
