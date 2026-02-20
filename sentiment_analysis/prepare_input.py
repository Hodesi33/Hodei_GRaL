import pandas as pd
from sklearn.model_selection import train_test_split
from langdetect import detect

def prepare_data(input_path, dev_path, test_path):
    """
    Sarrerako datuak prestatzen ditu sentiment analysis esperimentuetarako.

    Prozesua:
    - Sarrerako CSV-a irakurri.
    - Language zutabea sortu edo normalizatu (eu/es).
    - Derrigorrezko zutabeak daudela egiaztatu.
    - Etiketak formatu estandar batera mapatu (pos/neu/neg).
    - Datuak dev eta test multzoetan banatu.
    - Multzo bakoitzean Text_id berria esleitu.
    - Dev eta test CSV fitxategiak sortu.

    Parametroak
    ----------
    input_path : str
        Sarrerako CSV fitxategiaren bidea.
    dev_path : str
        Development multzoaren irteera-fitxategia.
    test_path : str
        Test multzoaren irteera-fitxategia.

    Return
    ------
    None
    """

    # Test multzoaren proportzioa (gainerakoa dev-era doa)
    test_size = 2/3

    # Sarrerako CSV-a irakurri
    df = pd.read_csv(input_path)



    # |----------------------------------------------------------------------------------------------------|
    # |----------------------------------- LANGUAGE SORTU ETA NORMALIZATU ---------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # Language zutabea ez badago, sortu egiten da
    if "Language" not in df.columns:
        df["Language"] = ""

    def _fix_lang(row) -> str:
        """
        Language balioa normalizatzen du:
        - 'eu' edo 'es' bada, bere horretan mantentzen da.
        - Bestela, testuaren hizkuntza detektatzen da eta 'es' ez bada, 'eu' ezartzen da.

        Return
        ------
        str
            Hizkuntza etiketa normalizatua ('eu', 'es' edo '').
        """
        lang = str(row.get("Language", "")).strip().lower()
        if lang in ("eu", "es"):
            return lang

        text = str(row.get("Text", "")).strip()
        if not text:
            return "" # Testurik ez badago, balio hutsa mantentzen da

        try:
            d = detect(text)
        except Exception:
            d = ""

        # 'es' bada, 'es'; bestela, 'eu'
        return "es" if d == "es" else "eu"

    df["Language"] = df.apply(_fix_lang, axis=1)



    # |----------------------------------------------------------------------------------------------------|
    # |----------------------------------- ZUTABEEN EGIAZTAPENA ETA MAPA ----------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # Derrigorrezko zutabeak existitzen direla ziurtatu
    required_columns = ['Text', 'Label'] # Beste zutabe izen batzuk badaude, hemen egokitu
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"'{col}' zutabea falta da sarrerako CSV-an.")
    
    # Etiketak mapatu: "Positiboa" -> "pos", "Neutroa" -> "neu", "Negatiboa" -> "neg"
    etiketa_map = {
        "Positiboa": "pos",
        "Neutroa": "neu",
        "Negatiboa": "neg"
    }
    df['Label'] = df['Label'].map(etiketa_map).fillna(df['Label'])

    # Beharrezko zutabeekin bakarrik geratu
    new_df = df[['Text', 'Language', 'Label']]



    # --- Banaketa (dev/test) ---
    # test_size proportzioa test-era, gainerakoa dev-era
    dev_df, test_df = train_test_split(
        new_df, test_size=test_size, random_state=33, shuffle=True
    )



    # --- Text_id esleitu ---
    # Multzo bakoitzean Text_id berria sortu (1etik hasita)
    dev_df = dev_df.reset_index(drop=True)
    dev_df.insert(0, 'Text_id', range(1, len(dev_df) + 1))

    test_df = test_df.reset_index(drop=True)
    test_df.insert(0, 'Text_id', range(1, len(test_df) + 1))



    # --- Irteera gorde ---
    # Dev eta test CSV fitxategietan gorde
    dev_df.to_csv(dev_path, index=False)
    test_df.to_csv(test_path, index=False)
