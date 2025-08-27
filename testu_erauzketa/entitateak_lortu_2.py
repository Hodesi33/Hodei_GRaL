import spacy
import pandas as pd
from transformers import pipeline

# Modeloak kargatu
# SpaCy (es)
try:
    nlp_es = spacy.load("es_core_news_sm")
except:
    nlp_es = spacy.blank("es")

# BERTeus (NER pipeline) (eu)
try:
    ner_eu = pipeline("ner", model="ixa-ehu/berteus-base-cased", aggregation_strategy="simple")
except Exception as e:
    print("Errorea BERTeus kargatzean:", e)
    ner_eu = None

# Stopwords
STOPWORDS_ES = spacy.lang.es.stop_words.STOP_WORDS
STOPWORDS_EU = {"eta", "edo", "baita", "izan", "dut", "da", "zuen"} # Handitu daiteke



# Funtzioak
def entitateak_lortu_parrafo(testua, hizkuntza):
    """Paragrafo baten entitateak lortu hizkuntza kontuan hartuta."""

    if not testua.strip():
        return []

    ents = []
    if hizkuntza == "es":
        doc = nlp_es(testua)
        ents = [ent.text for ent in doc.ents]

    elif hizkuntza == "eu" and ner_eu is not None:
        results = ner_eu(testua)
        ents = [r["word"] for r in results]

    else:  # fallback -> tokenizazioa soilik
        doc = spacy.blank("xx")(testua)
        ents = [tok.text.lower() for tok in doc if not tok.is_punct]

    return ents



def entitateak_lortu(df):
    """
    Funtzio nagusia.
    DataFrame-ari 'Entities' eta 'Entities_stw' zutabeak gehitu.
    Zutabe bakoitza (Text eta Language) paragrafoz banatuta dago (<PARRAFO/>), eta <PARRAFO/> kontserbatuko da.
    """

    entities_guztiak = []
    entities_guztiak_stw = []

    for _, row in df.iterrows():
        testuak = row["Text"].split("<PARRAFO/>")
        hizkuntzak = row["Language"].split("<PARRAFO/>")

        parrafo_ents = []
        parrafo_ents_stw = []

        for t, h in zip(testuak, hizkuntzak):
            if not t.strip():
                parrafo_ents.append("")
                parrafo_ents_stw.append("")
                continue

            ents = entitateak_lortu_parrafo(t, h)

            if h == "es":
                ents_stw = [w for w in ents if w.lower() not in STOPWORDS_ES]
            else:
                ents_stw = [w for w in ents if w.lower() not in STOPWORDS_EU]

            parrafo_ents.append(" ".join(ents))
            parrafo_ents_stw.append(" ".join(ents_stw))

        entities_guztiak.append("<PARRAFO/>".join(parrafo_ents))
        entities_guztiak_stw.append("<PARRAFO/>".join(parrafo_ents_stw))

    df["Entities"] = entities_guztiak
    df["Entities_stw"] = entities_guztiak_stw

    return df
