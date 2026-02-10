import pandas as pd
from corpusaPrestatu import corpusa_prozesatu, split_parrafoak
from lemak_lortu import lemak_lortu
from entitateak_lortu_ondo import entitateak_lortu
from parlaMint_bateratu import merge_parlamint_folders, build_global_tsv

# Nire exekuzioan 04:30:00 iraun du gutxi gora behera
def main():
    """
    Erauzketaren funtzio nagusia.
    Dataframe batean jasoko dira espero diren datuak, eta csv batean gordeko dira.
    1. bertsio honetan, GRaL-erako gomendatu diren modeloak erabiliko dira.
    """

    # |----------------------------------------------------------------------------------------------------|
    # |-------------------------------------- CORPUSEN PROZESAMENDUA --------------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # # Nire exekuzioan 00:05:23 iraun du lehen atal honek.
    # # Behin 3 .tsv-ak lortuta, eginda = True jarri daiteke, hurrengo zarian datuak berriro kargatzen direlako, horrela denbora aurreztuz.
    eginda = True

    if eginda == False:
        # Zutabeak definitu
        columns = [
            "Date",          # Hitzaldiaren data (formatua: YYYY-MM-DD)
            "Speech_id",     # Hitzaldi bakoitzaren identifikagailu bakarra
            "Text_id",       # Hitzaldiaren barruko testu-zatiaren identifikagailua
            "Speaker",       # Testu-zatia esaten duen hizlariaren izena
            "Birth",         # Hizlariaren jaiotze-data (formatua: YYYY-MM-DD) # Hau gehitu behar da, hizlari bakoitzaren jaiotze dataren .txt bat eginez
            "Gender",        # Hizlariaren generoa (Emakumea: F - Gizonezkoa: M)
            "Party",         # Hizlariaren partidu politikoa # Hau gehitu behar da, hizlari bakoitzaren partiduaren .txt bat eginez
            "Language",      # Testuaren hizkuntza (eu/es)
            "Text",          # Hitzaldiaren testu-zatiaren edukia
            # "Lemmas",        # Lemak
            # "Lemmas_stw",    # Lemak stopwords gabe
            # "Entities",      # Entitateak
            # "Entities_stw"   # Entitateak stopwords gabe
        ]

        path_parlaMint = "ParlaMint-ES-PV"
        path_basqueParl = "basque-parliament-corpus-transcriptions"



        # ParlaMint fitxategiak bateratu (bi .tsv eta .txt fitxategiak)
        merge_parlamint_folders(input_dir=path_parlaMint, output_dir="ParlaMint-ES-PV-bateratua", skip_existing=True)
        # ParlaMint-eko fitxategi guztiak taula bakarrean bildu
        df_pm = build_global_tsv(input_dir="ParlaMint-ES-PV-bateratua")
            # Tabulazioak etab. garbitu, bestela gero errorea emango du!
        df_pm["Text"] = (
            df_pm["Text"]
            .astype(str)
            .str.replace("\t", " ", regex=False)
            .str.replace("\r", " ", regex=False)
            .str.replace("\n", " ", regex=False)
        )
        df_pm.to_csv("global-ParlaMint-ES-PV.tsv", sep="\t", index=False, encoding="utf-8")
        print("ParlaMint TSV globala sortuta.")
        


        # BasqueParl corpusaren prozesamendua (Olatz Pérez de Viñaspre-ren kodea adaptatuta)
        erregistroak = corpusa_prozesatu(corpus_path=path_basqueParl)
        df_bp = pd.DataFrame(erregistroak, columns=columns)
            # Tabulazioak etab. garbitu, bestela gero errorea emango du!
        df_bp["Text"] = (
            df_bp["Text"]
            .astype(str)
            .str.replace("\t", " ", regex=False)
            .str.replace("\r", " ", regex=False)
            .str.replace("\n", " ", regex=False)
        )
            # Parrafozka banatu
        df_bp = split_parrafoak(df_bp)
        df_bp.to_csv("global-BasqueParl.tsv", index=False, sep="\t", encoding="utf-8")
        print("BasqueParl TSV globala sortuta.")



        # Bi corpusen datuak batu
        df_basqueParl = pd.read_csv("global-BasqueParl.tsv", sep="\t", dtype=str)
        df_parlaMint = pd.read_csv("global-ParlaMint-ES-PV.tsv", sep="\t", dtype=str)
            # Indizea 0-tik berriro ez hasteko
        max_id = df_basqueParl['Speech_id'].astype(int).max() + 1
        df_parlaMint['Speech_id'] = (df_parlaMint['Speech_id'].astype(int) + max_id).astype(str)
        df_all = pd.concat([df_basqueParl, df_parlaMint], ignore_index=True)
        df_all.to_csv("global-CorpusBase.tsv", sep="\t", index=False)
        print("TSV globala sortuta: global-CorpusBase.tsv")





    # |----------------------------------------------------------------------------------------------------|
    # |------------------------------------ LEMAK ETA ENTITATEAK LORTU ------------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # Corpus osoa kargatu
    df = pd.read_csv("global-CorpusBase.tsv", sep="\t", dtype=str)
    print("Corpus osoa kargatua.")

    # Lemak gehitu
    df = lemak_lortu(df)
    print(df.head())
    df.to_csv("corpus_erauzketa_lemak_final.tsv", index=False, sep="\t", encoding="utf-8")

    # # Entitateak gehitu
    # df = entitateak_lortu(df)
    # print(df.head())
    # df.to_csv("corpus_erauzketa.tsv", index=False, sep="\t", encoding="utf-8")

if __name__ == "__main__":
    main()
