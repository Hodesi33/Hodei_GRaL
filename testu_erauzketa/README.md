# Testu Erauzketa - Erabilera Gida

## Beharrezko karpeten egitura

Kode hau erabiltzeko, ondorengo karpeta-egitura behar da:

### 1. BasqueParl

`BasqueParl` izeneko karpeta bat, eta barruan urteka antolatutako azpikarpetak:
- "2012"
- "2013"
- ...

Urteko karpeta bakoitzaren barruan:
- Transkripzioak `.txt` formatuan egon behar dira.
- Beste fitxategi batzuk badaude, ez dira kontuan hartuko.

### 2. ParlaMint

`ParlaMint` izeneko karpeta bat, eta barruan urteka antolatutako azpikarpetak:
- "2015"
- "2016"
- ...

Urteko karpeta bakoitzaren barruan, transkripzio bakoitzeko 3 fitxategi egongo dira:
- Bi `.tsv` fitxategi (testuari buruzko metadatuak, baina ez testua bera):
  - Batek titulua euskaraz izango du.
  - Besteak titulua ingelesez.
- Hirugarren fitxategia `.txt` bat izango da, eta bertan transkripzioaren testua egongo da, identifikatzaile batekin.

---

## Exekuzio pausuak

1. Kode nagusia `main_erauzketa.py` da. Beraz, fitxategi hori exekutatu behar da.

2. Datuen karpeten bideak (`path`) `main_erauzketa.py` barruan zehaztu behar dira:
   - `path_parlaMint`
   - `path_basqueParl`

3. Kontuan izan:
   - Defektuz dauden izenak erabiltzen ez badira, ziurtatu irteerako karpetek/fitxategiek ez dutela talka egiten existitzen direnekin.

---

## Sortzen diren fitxategiak

Kodea behar bezala exekutatzen bada, honako fitxategiak sortuko dira:

- `global-BasqueParl.tsv`
- `global-ParlaMint-ES-PV.tsv`
- `global-CorpusBase.tsv`

Lehenengo bietan corpus bakoitzeko datuak jasoko dira.
`global-CorpusBase.tsv` fitxategian bi corpusak elkartuta agertuko dira:
- Lehenik BasqueParl
- Ondoren ParlaMint

TSV horietan transkripzioetatik erauzitako datuak jasoko dira.

---

### Lemak eta entitateak

`main_erauzketa.py` exekutatzean:

- `corpus_erauzketa.tsv` sortuko da:
  - `global-CorpusBase.tsv`-ko informazioa
  - Lortutako lemak
  - Lortutako entitateak

Prozesuan zehar, honako fitxategiak ere sortzen dira:
- `corpus_erauzketa_lemak.tsv`
- `corpus_erauzketa_entities.tsv`

Hauek exekuzioaren jarraipena egiteko dira.  
`corpus_erauzketa.tsv` ondo sortu bada, aurreko bi fitxategiak ezabatu daitezke.

---

## Gehigarriak

`corpusen_analisia.ipynb` notebook-aren barruan, bi corpusen azterketa bat egiten da, corpusetan aurki daitezkeen datuen analisia egiteko.
