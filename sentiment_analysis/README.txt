Kode hau erabiltzeko ondorengoak behar dira:
data.csv izeneko (beste izen bat jarriz, main_sentiment.py fitxategian, input_csv aldatu honen izena jarriz) fitxategi bat behar da:
Bertan "Text" eta "Label" zutabeak dituenak gutxienez. "Language" zutabea badu, "eu" = euskara eta "es" = gaztelania hizkuntzetarako jarri.

Behin hori edukita, ondorengo pausuak jarraitzen dira:
Kode nagusia, main_sentiment.py da, beraz hau exekutatu behar da. data.csv fitxategia, main_sentiment.py dagoen karpeta berdinean eduki behar da.
Hau edukita, prepare_input-ek dev.csv eta test.csv fitxategiak sortuko ditu ondorengo banaketarekin: datuen 1/3 dev-entzat eta 2/3 test-entzat. Hau test_size aldatuz alda daiteke nahi den proportzioa jartzeko. 
Behin dev.csv eta test.csv sortu direla eta main_sentiment.py berriro exekutatu behar bada, prepare_data-ren lerroa komentatu daiteke, azkarrago exekutatzeko.
Ondoren, sentiment_analysis.py-ri bi aldiz deituko zaio, behin dev.csv datuei aplikatzeko, eta beste behin test.csv-rentzat. Hauek, emaitzak_sentiment karpetaren barruan karpetak sortuko dituzte bertan emaitzak jasotzeko. Bertan, metrics eta decoded karpetak aurkituko dira. Metrics barruan, emaitzak aurkitzen dira, eta decoded barruan, prozesuan erabiltzen diren datu batzuk, modeloak bueltatzen duena eta benetazko etiketa aurkituko dira, beste batzuen artean.
Ereduak aldatzeko, sentiment_analysis.py barruan # === MODELOA KONFIGURATZEA === atalean barruan, horko eredu bat aukeratu behar da eta besteak komentatu, bestela deskomentatu den azkenekoa aukeratuko da. Exekutatzerakoan, modeloaren izenarekin jasoko dira emaitzak, aipatu diren karpetetan.
Baita, zero-shot, few-shot adibide batekin etiketako edo few-shot bi adibiderekin etiketako aukeratu behar da. Hau main_sentiment.py barruan analysis_type aldagaian aukeratu behar da. Lerro horretan agertzen den bezala, ondorengo hauetako bat aukeratu behar da: "zero-shot", "few-shot-1" edo "few-shot-2". Emaitzak, bakoitzaren karpeta barruan jasoko dira.
