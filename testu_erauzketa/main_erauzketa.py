import pandas as pd

from corpusaPrestatu import (
    corpusa_prozesatu,
    split_parrafoak,
    language_normalizatu,
    merge_lemmas_entities,
)
from lemak_lortu import lemak_lortu
from entitateak_lortu import entitateak_lortu
from parlaMint_bateratu import merge_parlamint_folders, build_global_tsv



def main():
    """
    Erauzketa-prozesuaren funtzio nagusia.

    Helburuak:
    - ParlaMint eta BasqueParl corpusak prestatzea eta bateratzea.
    - Lemak eta entitateak erauztea.
    - Emaitzak TSV fitxategietan gordetzea.
    """

    # |----------------------------------------------------------------------------------------------------|
    # |-------------------------------------- CORPUSEN PROZESAMENDUA --------------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # --- Sarrerako karpeten bideak ---
    path_parlaMint = "ParlaMint"
    path_basqueParl = "BasqueParl"

    # True -> TSV berriak ez dira sortuko
    # False -> Corpusak berriro prozesatuko dira
    eginda = False

    if eginda is False:

        # BasqueParl-erako taularen zutabe-egitura
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



        # --- ParlaMint corpusaren prozesamendua ---
        # ParlaMint fitxategiak bateratu (TSV eta TXT)
        merged_path_parlaMint = "ParlaMint-bateratua"
        merge_parlamint_folders(input_dir=path_parlaMint, output_dir=merged_path_parlaMint, skip_existing=True)
        
        # ParlaMint-eko fitxategi guztiak taula bakarrean bildu
        df_pm = build_global_tsv(input_dir=merged_path_parlaMint)

        # Testuko kontrol-karaktereak garbitu
        df_pm["Text"] = (
            df_pm["Text"]
            .astype(str)
            .str.replace("\t", " ", regex=False)
            .str.replace("\r", " ", regex=False)
            .str.replace("\n", " ", regex=False)
        )

        df_pm.to_csv("global-ParlaMint.tsv", sep="\t", index=False, encoding="utf-8")
        print("ParlaMint TSV globala sortuta.")
        


        # --- BasqueParl corpusaren prozesamendua --- 
        # Olatz Pérez de Viñaspre-ren kodea adaptatuta
        erregistroak = corpusa_prozesatu(corpus_path=path_basqueParl)
        df_bp = pd.DataFrame(erregistroak, columns=columns)

        # Testuko kontrol-karaktereak garbitu
        df_bp["Text"] = (
            df_bp["Text"]
            .astype(str)
            .str.replace("\t", " ", regex=False)
            .str.replace("\r", " ", regex=False)
            .str.replace("\n", " ", regex=False)
        )

        # Testua paragrafoetan banatu
        df_bp = split_parrafoak(df_bp)

        df_bp.to_csv("global-BasqueParl.tsv", index=False, sep="\t", encoding="utf-8")
        print("BasqueParl TSV globala sortuta.")



        # Bi corpusen datuak batu
        df_basqueParl = pd.read_csv("global-BasqueParl.tsv", sep="\t", dtype=str)
        df_parlaMint  = pd.read_csv("global-ParlaMint.tsv", sep="\t", dtype=str)

        # Hizkuntza-etiketak normalizatu (eu/es)
        df_basqueParl = language_normalizatu(df_basqueParl)
        df_parlaMint  = language_normalizatu(df_parlaMint)

        # Speech_id balioen arteko talka saihestu
        max_id = df_basqueParl['Speech_id'].astype(int).max() + 1
        df_parlaMint['Speech_id'] = (df_parlaMint['Speech_id'].astype(int) + max_id).astype(str)
        
        # DataFrame bakarrean bateratu
        df_all = pd.concat([df_basqueParl, df_parlaMint], ignore_index=True)
        df_all.to_csv("global-CorpusBase.tsv", sep="\t", index=False)

        print("TSV globala sortuta: global-CorpusBase.tsv")





    # |----------------------------------------------------------------------------------------------------|
    # |------------------------------------ LEMAK ETA ENTITATEAK LORTU ------------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # Corpus bateratua kargatu
    df = pd.read_csv("global-CorpusBase.tsv", sep="\t", dtype=str)
    print("Corpus osoa kargatua.")

    # Lemak erauzi
    df = lemak_lortu(df)
    print(df.head())

    # Entitateak erauzi
    df = entitateak_lortu(df)
    print(df.head())

    # Lemak eta entitateak fitxategi bakarrean bateratu
    merge_lemmas_entities(
        lemak_path="corpus_erauzketa_lemak.tsv",
        entities_path="corpus_erauzketa_entities.tsv",
        out_path="corpus_erauzketa.tsv"
    )



if __name__ == "__main__":
    main()
