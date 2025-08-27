from prepare_input import prepare_data
from sentiment_analysis import sentiment_analysis

def main():
    """
    Sentiment analysis egiteko behar diren funtzioak koordinatzen dituen funtzio nagusia.
    """

    # Fitxategien path-ak definitu.
    input_csv = "data.csv"
    dev_csv = "dev.csv"
    test_csv = "test.csv"

    # Input-a prestatu: dev eta test CSV-ak sortu.
    #prepare_data(input_csv, dev_csv, test_csv) # Eginda badago ez da zertan berriro egin behar, eta lerro hau komentatu daiteke.


    # Analisia zein formatutan egin nahi duzun.
    analysis_type = "few-shot-2" #zero-shot; few-shot-1; few-shot-2

    # Bakarrik dev edo test egin nahi bada, ahal dira komentatu azkarrago egiteko nahi dena!
    # Sentiment analysis egin development datuekin. Modeloa sentiment_analysis.py barruan aukeratu!
    #print("Development datuekin sentiment analysis egiten...")
    #dev_result = sentiment_analysis(dev_csv, analysis_type)
    
    # Sentiment analysis egin test datuekin. Modeloa sentiment_analysis.py barruan aukeratu!
    print("Test datuekin sentiment analysis egiten...")
    test_result = sentiment_analysis(test_csv, analysis_type)



if __name__ == "__main__":
    main()
