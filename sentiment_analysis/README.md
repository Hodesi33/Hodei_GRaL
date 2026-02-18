# Sentiment Analysis - Erabilera Gida

## Beharrezko fitxategiak

Kode hau erabiltzeko, `data.csv` izeneko fitxategi bat behar da.

> Beste izen bat erabili nahi bada, `main_sentiment.py` fitxategian `input_csv` aldagaia aldatu, eta fitxategiaren izen berria jarri.

`data.csv` fitxategiak gutxienez zutabe hauek eduki behar ditu:
- `Text`
- `Label`

Aukeran, `Language` zutabea ere eduki daiteke:
- `eu` = euskara
- `es` = gaztelania

`Language` zutaberik ez badago, hizkuntza automatikoki detektatuko da `langdetect` erabiliz.

---

## Exekuzio pausuak

1. Kode nagusia `main_sentiment.py` da; beraz, fitxategi hori exekutatu behar da.

2. `data.csv` fitxategia `main_sentiment.py` dagoen karpeta berean egon behar da.

3. Exekuzioan zehar, `prepare_input.py` exekutatuko da automatikoki eta bi fitxategi sortuko ditu:
   - `dev.csv`
   - `test.csv`

   Banaketa honela egiten da:
   - datuen 1/3 `dev`-erako
   - datuen 2/3 `test`-erako

   Proportzioa aldatu nahi bada, `prepare_input.py`-ko `test_size` aldagaia egokitu daiteke.

4. `dev.csv` eta `test.csv` sortu ondoren, `sentiment_pipeline.py`-ri bi aldiz deituko zaio:
   - behin `dev.csv`-rako
   - behin `test.csv`-rako

   Honek `emaitzak_sentiment` karpetaren barruan karpetak sortuko ditu, emaitzak gordetzeko.

---

## Emaitzen egitura

`emaitzak_sentiment` karpetaren barruan honako azpikarpetak sortuko dira:

- `metrics/`  
  Emaitzen metrikak bertan aurkituko dira.

- `decoded/`  
  Prozesuan erabilitako informazioa gordetzen da: besteak beste, ereduak bueltatutako iragarpenak eta benetako etiketak.

- `confusion_matrixes/`  
  Confusion matrix-ak aurkituko dira, ereduak zein etiketatan huts egiten duen ikusteko.

---

## Eredua aldatzea

Eredua aldatzeko, `sentiment_pipeline.py` fitxategian, **"EREDUA KONFIGURATZEA"** atalean:

- erabili nahi den eredua **deskomentatu**
- gainerakoak **komentatu**

Bestela, deskomentatuta dagoen **azken eredua** erabiliko da.

Exekuzioan, emaitzak, erabilitako ereduaren izenarekin gordeko dira aurretik aipatutako karpetetan.

---

## Analisi mota aukeratzea (zero-shot / few-shot)

Analisi mota `main_sentiment.py` fitxategiko `analysis_type` aldagaian aukeratzen da.

Aukerak:
- `"zero-shot"`
- `"few-shot-1"` (few-shot adibide 1 erabiliz)
- `"few-shot-2"` (few-shot 2 adibide erabiliz)

Defektuz, hirurak exekutatuko dira segidan, baina `analysis_type` aldatuz hau mugatu daiteke.

Emaitzak analisi mota bakoitzaren karpetaren barruan gordeko dira.
