import pandas as pd
from corpusaPrestatu import corpusa_prozesatu
from lemak_lortu_2 import lemak_lortu
from entitateak_lortu_2 import entitateak_lortu
from parlaMint_bateratu import merge_parlamint_folders, build_global_tsv

# Nire exekuzioan 00:26:00 iraun du gutxi gora behera
def main():
    """
    Erauzketaren funtzio nagusia.
    Dataframe batean jasoko dira espero diren datuak, eta csv batean gordeko dira.
    2. bertsio honetan, GRaL-erako gomendatu diren modeloak alde batera utziz, beste batzuk erabiliko dira. Hau horrela da, gomendatutakoak ez zutenez guztiz ondo funtzionatzen, ikusteko ea beste modelo batzuekin zer moduz doazen.
    """

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
        "Lemmas",        # Lemak
        "Lemmas_stw",    # Lemak stopwords gabe
        "Entities",      # Entitateak
        "Entities_stw"   # Entitateak stopwords gabe
    ]

    ## Nire exekuzioan 00:05:47 iraun du gutxi gora behera lehen atal honek.
    # ParlaMint fitxategiak bateratu (bi .tsv eta .txt fitxategiak)
    merge_parlamint_folders(input_dir="ParlaMint-ES-PV", output_dir="ParlaMint-ES-PV-bateratua", skip_existing=True)
    # ParlaMint-eko fitxategi guztiak taula bakarrean bildu
    build_global_tsv(input_dir="ParlaMint-ES-PV-bateratua", output_file="global-ParlaMint-ES-PV.tsv")
    print("ParlaMint TSV globala sortuta.")
    
    # Corpusaren prozesamendua (Olatz Pérez de Viñaspre-ren kodea adaptatuta) - BasqueParl
    erregistroak = corpusa_prozesatu(corpus_path="basque-parliament-corpus-transcriptions") #basque-parliament-corpus-transcriptions,ParlaMint-ES-PV
    df_bp = pd.DataFrame(erregistroak, columns=columns)
    df_bp.to_csv("global-BasqueParl.tsv", index=False, sep="\t", encoding="utf-8")
    print("BasqueParl TSV globala sortuta.")

    # Bi corpusen datuak batu
    df_basqueParl = pd.read_csv("global-BasqueParl.tsv", sep="\t", dtype=str)
    df_parlaMint = pd.read_csv("global-ParlaMint-ES-PV.tsv", sep="\t", dtype=str)
    df_all = pd.concat([df_basqueParl, df_parlaMint], ignore_index=True)
    df_all.to_csv("global-CorpusBase.tsv", sep="\t", index=False)
    print("TSV globala sortuta: global-CorpusBase.tsv")



    # # Corpus osoa kargatu
    # df = pd.read_csv("global-CorpusBase.tsv", sep="\t", dtype=str)
    # print("Corpus osoa kargatua.")

    # # Lemak gehitu
    # df = lemak_lortu(df)
    # print(df.head())
    # df.to_csv("corpus_erauzketa_2.tsv", index=False, sep="\t", encoding="utf-8")

    # # Entitateak gehitu
    # df = entitateak_lortu(df)
    # print(df.head())
    # df.to_csv("corpus_erauzketa_2.tsv", index=False, sep="\t", encoding="utf-8")

if __name__ == "__main__":
    main()
