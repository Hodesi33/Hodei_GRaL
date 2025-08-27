import pandas as pd
from corpusaPrestatu import corpusa_prozesatu
from lemak_lortu import lemak_lortu
from entitateak_lortu import entitateak_lortu

# Nire exekuzioan 04:30:00 iraun du gutxi gora behera
def main():
    """
    Erauzketaren funtzio nagusia.
    Dataframe batean jasoko dira espero diren datuak, eta csv batean gordeko dira.
    1. bertsio honetan, GRaL-erako gomendatu diren modeloak erabiliko dira.
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

    # Korpusaren prozesamendua (Olatz Pérez de Viñaspre-ren kodea adaptatuta)
    erregistroak = corpusa_prozesatu(corpus_path="basque-parliament-corpus-transcriptions")
    df = pd.DataFrame(erregistroak, columns=columns)
    print(df.head())
    df.to_csv("corpus_erauzketa.csv", index=False, sep="\t", encoding="utf-8")

    # Lemak gehitu
    df = lemak_lortu(df)
    print(df.head())
    df.to_csv("corpus_erauzketa.csv", index=False, sep="\t", encoding="utf-8")

    # Entitateak gehitu
    df = entitateak_lortu(df)
    print(df.head())
    df.to_csv("corpus_erauzketa.csv", index=False, sep="\t", encoding="utf-8")

if __name__ == "__main__":
    main()
