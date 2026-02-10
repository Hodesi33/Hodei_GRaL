Kode hau erabiltzeko ondorengoak behar dira:
(BasqueParl) Karpeta bat, non barruan beste karpeta batzuk egongo diren urteen izenekin, adibidez, "2012", "2013", ... izeneko karpetak. Horien barruan, .txt-ak sartu beharko dira transkripzioekin. Beste fitxategi batzuk badaude, hauek ez dira kontutan hartuko.
(ParlaMint) Karpeta bat, non barruan beste karpeta batzuk egongo diren urteen izenekin, adibidez, "2015", "2016", ... izeneko karpetak. Horien barruan, 3 fitxategi aurkituko dira transkripzio bakoitzerako. Lehenengo biah .tsv-ak izango dira, testuaren inguruko datuak eskainiz (testua ez), bat titulua euskaraz eta bestea gaztelaniaz. Hirugarren fitxategian (.txt), testua aurkituko da identifikatzaile batekin.

Behin hori edukita, ondorengo pausuak jarraitzen dira:
Kode nagusiak, main_erauzketa.py eta main_erauzketa_2.py dira, beraz hauetako bat exekutatu behar da. Datuen karpeten helbideak (path-ak), main_erauzketa.py eta main_erauzketa_2.py barruan adierazi beharko dira, path_parlaMint eta path_basqueParl aldagaietan. Kontutan eduki, defektuz dauden izenak ez badiera erabiltzen, irteerako karpeta/fitxategiekin talka ez dutela egiten.
Behin kodea exekutatzerakoan, datuak ondo jarri badira, global-ParlaMint-ES-PV.tsv, global-BasqueParl.tsv eta global-CorpusBase.tsv sortuko dira, lehenengo bietan corpus bakoitzeko datuak jasoz, eta CorpusBase-ren barruan biak elkartuta, lehenik BasqueParl eta gero ParlaMint. TSV horietan, transkripzioetatik erauzitako datuak jasoko dira.
Lemak eta entitateak lortutakoan, corpus_erauzketa.tsv sortuko da main_erauzketa.py exekutatu bada, eta corpus_erauzketa_2.tsv, main_erauzketa_2.py exekutatu bada, bertan jasoz global-CorpusBase.tsv barruko informazioa eta lortutako lemak eta entitateak.

Gehigarriak:
corpusen_analisia.ipynb notabook-aren barruan, bi corpusen azterketa bat egin da jakiteko nolako datuak aurki daitezken corpusetan.
