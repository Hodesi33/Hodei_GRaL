import spacy
import stanza

# Modeloak kargatu
# SpaCy (es)
try:
    nlp_es = spacy.load("es_core_news_sm")
except:
    nlp_es = spacy.blank("es")

# Stanza (eu)
try:
    stanza.download("eu")  # Lehenengo exekuzioan bakarrik behar da
except:
    pass

nlp_eu = stanza.Pipeline("eu", processors="tokenize,lemma", tokenize_no_ssplit=True)

# Stopwords
STOPWORDS_ES = spacy.lang.es.stop_words.STOP_WORDS
STOPWORDS_EU = {"eta", "edo", "baita", "izan", "dut", "da", "zuen"} # Handitu daiteke



# Funtzioak
def lematizatu(testua, hizkuntza):
    """Paragrafo baten lematizazioa hizkuntza kontuan hartuta."""

    if not testua.strip():
        return []

    if hizkuntza == "es":
        doc = nlp_es(testua)
        return [tok.lemma_ for tok in doc if not tok.is_punct]
    else:  # hizkuntza == "eu"
        doc = nlp_eu(testua)
        # Filtratu None diren lemak, bestela errorea ematen du!
        return [word.lemma for sent in doc.sentences for word in sent.words if word.lemma is not None and word.text.strip()]



def lemak_lortu(df):
    """
    Funtzio nagusia.
    DataFrame-ari 'Lemmas' eta 'Lemmas_stw' zutabeak gehitu.
    Zutabe bakoitza (Text eta Language) paragrafoz banatuta dago (<PARRAFO/>), eta <PARRAFO/> kontserbatuko da.
    """

    lemma_guztiak = []
    lemma_guztiak_stw = []

    for _, row in df.iterrows():
        testuak = row["Text"].split("<PARRAFO/>")
        hizkuntzak = row["Language"].split("<PARRAFO/>")

        parrafo_lemak = []
        parrafo_lemak_stw = []

        for t, h in zip(testuak, hizkuntzak):
            if not t.strip():
                parrafo_lemak.append("")
                parrafo_lemak_stw.append("")
                continue

            lemak = lematizatu(t, h)

            if h == "es":
                lemak_stw = [w for w in lemak if w not in STOPWORDS_ES]
            else:
                lemak_stw = [w for w in lemak if w not in STOPWORDS_EU]

            parrafo_lemak.append(" ".join(lemak))
            parrafo_lemak_stw.append(" ".join(lemak_stw))

        lemma_guztiak.append("<PARRAFO/>".join(parrafo_lemak))
        lemma_guztiak_stw.append("<PARRAFO/>".join(parrafo_lemak_stw))

    df["Lemmas"] = lemma_guztiak
    df["Lemmas_stw"] = lemma_guztiak_stw

    return df
