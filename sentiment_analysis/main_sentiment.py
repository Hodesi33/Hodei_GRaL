from prepare_input import prepare_data
from sentiment_pipeline import sentiment_analysis

def main():
    """
    Sentiment analysis prozesuan parte hartzen duten urrats nagusiak koordinatzen ditu.

    Prozesua:
    - Sarrerako datuak prestatu (dev/test CSV-ak sortuz).
    - Esperimentu mota desberdinak exekutatu (zero-shot eta few-shot konfigurazioak).
    - Aukeratutako partizioetan (dev/test) sentiment analysis aplikatu.
    """

    # |----------------------------------------------------------------------------------------------------|
    # |------------------------------------------ KONFIGURAZIOA -------------------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # Dev edo test multzoa exekutatu behar den adierazten du
    RUN_DEV = True
    RUN_TEST = True

    # Fitxategien bideak definitu
    input_csv = "data.csv"
    dev_csv = "dev.csv"
    test_csv = "test.csv"

    # Input-a prestatu: dev eta test CSV-ak sortu
    # Behin sortuta badaude, deialdi hau komentatu daiteke
    prepare_data(input_csv, dev_csv, test_csv)



    # |----------------------------------------------------------------------------------------------------|
    # |-------------------------------------------- EXEKUZIOAK --------------------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # Exekutatu beharreko esperimentuak definitu: ["zero-shot", "few-shot-1", "few-shot-2"]
    analysis_types = ["zero-shot", "few-shot-1", "few-shot-2"]

    # Esperimentu bakoitza exekutatu (dev + test)
    for analysis_type in analysis_types:
        print("\n" + "=" * 70)
        print(f"[INFO] Esperimentua hasten: {analysis_type}")
        print("=" * 70)

        # Development datuekin sentiment analysis exekutatu
        if RUN_DEV:
            print("Development datuekin sentiment analysis egiten...")
            _ = sentiment_analysis(dev_csv, analysis_type)

        # Test datuekin sentiment analysis exekutat
        if RUN_TEST:
            print("Test datuekin sentiment analysis egiten...")
            _ = sentiment_analysis(test_csv, analysis_type)
    

if __name__ == "__main__":
    main()
