import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data(input_path, dev_path, test_path):
    """
    Datuak prestatzeko funtzioa. Hemen sarrerako datuak prozesatu eta txukun jartzen dira, sentimenduen analisia ondo egin ahal izateko gero.
    Behar diren zutabeekin bakarrik geratzen da.
    """

    # Sarrerako CSV-a irakurri
    df = pd.read_csv(input_path)

    # Hizkuntzaren zutabea detektatu edo sortu
    language_column_found = False
    for col in ['Hizkuntza', 'Idioma', 'Language']:
        if col in df.columns:
            df['Language'] = df[col]
            language_column_found = True
            break
    if not language_column_found:
        # Ez badago, guztiei 'eu' esleitu
        df['Language'] = 'eu'
    
    # Derrigorrezko zutabeak existitzen direla ziurtatu
    required_columns = ['Text', 'Label'] # Beste zutabe izen batzuk baditu, hemen aldatu!
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

    # Beharrezko zutabeak hartu eta izenak egokitu
    # 'Esaldia' -> 'paragraph', 'Etiketa' -> 'label'
    new_df = df[['Text', 'Language', 'Label']]

    # Datuak zatitu: 33,33% dev (150), 66,66% test (300), random_state=33
    dev_df, test_df = train_test_split(
        new_df, test_size=2/3, random_state=33, shuffle=True
    )

    # 'Text_id' berria sortu 1-X arteko balioekin bakoitzean
    dev_df = dev_df.reset_index(drop=True)
    dev_df.insert(0, 'Text_id', range(1, len(dev_df) + 1))

    test_df = test_df.reset_index(drop=True)
    test_df.insert(0, 'Text_id', range(1, len(test_df) + 1))

    # CSV fitxategietan gorde
    dev_df.to_csv(dev_path, index=False)
    test_df.to_csv(test_path, index=False)
