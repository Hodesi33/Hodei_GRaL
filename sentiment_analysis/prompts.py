# === PROMPTEN DEFINIZIOA ===
# Hemen nire 12 prompt-ak (few-shot eta zero-shot-enak), {paragrafoa} barruan paragrafoa sartzeko

# == ZERO-SHOT-EN PROMPT_AK ==
prompt_zero_shot_1_1 = """Aztertu testu bakoitzaren jarrera eta sailkatu ondorengo kategorietako batean:
- pos (positiboa)
- neu (neutroa)
- neg (negatiboa)

Erantzuna **bakarrik** etiketa hauetako bat izan behar da: "pos", "neu" edo "neg". Ez eman azalpenik.

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_zero_shot_1_2 = """Ondorengo esaldiaren jarrera aztertu eta sailkatu: "pos" (positiboa), "neu" (neutroa) edo "neg" (negatiboa).
**Ez erantzun beste ezer, bakarrik etiketa.**

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_zero_shot_1_3 = """Parlamentuko testu baten jarrera zehaztu behar duzu.
Aukeratu hiru etiketetako bat:
- "pos" (positiboa)
- "neu" (neutroa)
- "neg" (negatiboa)

**Erantzuna soilik etiketa bat izan behar da, azalpenik gabe.**

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""



prompt_zero_shot_2_1 = """Analiza el sentimiento del siguiente texto y clasifícalo en una de estas categorías:
- pos (positivo)
- neu (neutral)
- neg (negativo)

La respuesta debe ser **únicamente** una de estas etiquetas: "pos", "neu" o "neg". No des explicaciones.

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_zero_shot_2_2 = """Indica si el siguiente texto es positivo (pos), neutral (neu) o negativo (neg).
**Responde solo con la etiqueta.**

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_zero_shot_2_3 = """Clasifica el sentimiento del siguiente párrafo parlamentario.
Elige solo una de estas etiquetas:
- "pos" (positivo)
- "neu" (neutral)
- "neg" (negativo)

**La respuesta debe ser solo la etiqueta, sin explicaciones.**

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_zero_shot_3_1 = """Classify the sentiment of the following text into one of these categories:
- pos (positive)
- neu (neutral)
- neg (negative)

The answer must be **only** one of these labels: "pos", "neu" or "neg". Do not provide explanations.

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""

prompt_zero_shot_3_2 = """Decide if the sentiment of the text is positive (pos), neutral (neu), or negative (neg).
**Respond with only the label.**

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""

prompt_zero_shot_3_3 = """You are analyzing the sentiment of parliamentary speeches.
Choose only one of the following labels:
- "pos" (positive)
- "neu" (neutral)
- "neg" (negative)

The response must be **only the label**.

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""



prompt_zero_shot_4_1 = """Ondorengo testuaren jarrera sailkatu honako kategoria hauetako batean:
- pos (positiboa)
- neu (neutroa)
- neg (negatiboa)

Erantzuna izan behar da **etiketa bakarra**: "pos", "neu" edo "neg". Ez eman azalpenik.

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_zero_shot_4_2 = """Esaldiaren jarrera identifikatu eta sailkatu: "pos", "neu" edo "neg".
**Ez idatzi beste ezer.**

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_zero_shot_4_3 = """Parlamentuko esaldi edo pasarte baten jarrera aztertu eta sailkatu:
- "pos" (positiboa)
- "neu" (neutroa)
- "neg" (negatiboa)

**Erantzuna izan behar da soilik etiketa bat, azalpenik gabe.**

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

# Prompt guztiak egituratuta. 1, 2, 3 eta 4 froga bakoitzeko 3 prompt.
prompt_zero_shot_dict = {
    1: [prompt_zero_shot_1_1, prompt_zero_shot_1_2, prompt_zero_shot_1_3],
    2: [prompt_zero_shot_2_1, prompt_zero_shot_2_2, prompt_zero_shot_2_3],
    3: [prompt_zero_shot_3_1, prompt_zero_shot_3_2, prompt_zero_shot_3_3],
    4: [prompt_zero_shot_4_1, prompt_zero_shot_4_2, prompt_zero_shot_4_3],
}





# == FEW-SHOT-EN PROMPT_AK ==
# == FEW-SHOT - ADIBIDE BATEKIN ==
prompt_few_shot_1__1_1 = """Aztertu testu bakoitzaren jarrera eta sailkatu ondorengo kategorietako batean:
- pos (positiboa)
- neu (neutroa)
- neg (negatiboa)

Erantzuna **bakarrik** etiketa hauetako bat izan behar da: "pos", "neu" edo "neg". Ez eman azalpenik.

Adibideak:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_1__1_2 = """Ondorengo esaldiaren jarrera aztertu eta sailkatu: "pos" (positiboa), "neu" (neutroa) edo "neg" (negatiboa).
**Ez erantzun beste ezer, bakarrik etiketa.**

Adibideak:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_1__1_3 = """Parlamentuko testu baten jarrera zehaztu behar duzu.
Aukeratu hiru etiketetako bat:
- "pos" (positiboa)
- "neu" (neutroa)
- "neg" (negatiboa)

**Erantzuna soilik etiketa bat izan behar da, azalpenik gabe.**

Adibideak:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""



prompt_few_shot_1__2_1 = """Analiza el sentimiento del siguiente texto y clasifícalo en una de estas categorías:
- pos (positivo)
- neu (neutral)
- neg (negativo)

La respuesta debe ser **únicamente** una de estas etiquetas: "pos", "neu" o "neg". No des explicaciones.

Ejemplos:
Ejemplo:
Párrafo: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiqueta: pos

Ejemplo:
Párrafo: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiqueta: neu

Ejemplo:
Párrafo: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiqueta: neg

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_few_shot_1__2_2 = """Indica si el siguiente texto es positivo (pos), neutral (neu) o negativo (neg).
**Responde solo con la etiqueta.**

Ejemplos:
Ejemplo:
Párrafo: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiqueta: pos

Ejemplo:
Párrafo: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiqueta: neu

Ejemplo:
Párrafo: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiqueta: neg

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_few_shot_1__2_3 = """Clasifica el sentimiento del siguiente párrafo parlamentario.
Elige solo una de estas etiquetas:
- "pos" (positivo)
- "neu" (neutral)
- "neg" (negativo)

**La respuesta debe ser solo la etiqueta, sin explicaciones.**

Ejemplos:
Ejemplo:
Párrafo: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiqueta: pos

Ejemplo:
Párrafo: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiqueta: neu

Ejemplo:
Párrafo: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiqueta: neg

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_few_shot_1__3_1 = """Classify the sentiment of the following text into one of these categories:
- pos (positive)
- neu (neutral)
- neg (negative)

The answer must be **only** one of these labels: "pos", "neu" or "neg". Do not provide explanations.

Examples in Vasque:
Example:
Paragraph: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Label: pos

Example:
Paragraph: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Label: neu

Example:
Paragraph: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Label: neg

Examples in Spanish:
Example:
Paragraph: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Label: pos

Example:
Paragraph: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Label: neu

Example:
Paragraph: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Label: neg

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""

prompt_few_shot_1__3_2 = """Decide if the sentiment of the text is positive (pos), neutral (neu), or negative (neg).
**Respond with only the label.**

Examples in Vasque:
Example:
Paragraph: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Label: pos

Example:
Paragraph: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Label: neu

Example:
Paragraph: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Label: neg

Examples in Spanish:
Example:
Paragraph: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Label: pos

Example:
Paragraph: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Label: neu

Example:
Paragraph: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Label: neg

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""

prompt_few_shot_1__3_3 = """You are analyzing the sentiment of parliamentary speeches.
Choose only one of the following labels:
- "pos" (positive)
- "neu" (neutral)
- "neg" (negative)

The response must be **only the label**.

Examples in Vasque:
Example:
Paragraph: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Label: pos

Example:
Paragraph: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Label: neu

Example:
Paragraph: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Label: neg

Examples in Spanish:
Example:
Paragraph: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Label: pos

Example:
Paragraph: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Label: neu

Example:
Paragraph: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Label: neg

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""



prompt_few_shot_1__4_1 = """Ondorengo testuaren jarrera sailkatu honako kategoria hauetako batean:
- pos (positiboa)
- neu (neutroa)
- neg (negatiboa)

Erantzuna izan behar da **etiketa bakarra**: "pos", "neu" edo "neg". Ez eman azalpenik.

Adibideak euskaraz:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiketa: pos

Adibidea:
Paragrafoa: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiketa: neu

Adibidea:
Paragrafoa: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_1__4_2 = """Esaldiaren jarrera identifikatu eta sailkatu: "pos", "neu" edo "neg".
**Ez idatzi beste ezer.**

Adibideak euskaraz:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiketa: pos

Adibidea:
Paragrafoa: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiketa: neu

Adibidea:
Paragrafoa: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_1__4_3 = """Parlamentuko esaldi edo pasarte baten jarrera aztertu eta sailkatu:
- "pos" (positiboa)
- "neu" (neutroa)
- "neg" (negatiboa)

**Erantzuna izan behar da soilik etiketa bat, azalpenik gabe.**

Adibideak euskaraz:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiketa: pos

Adibidea:
Paragrafoa: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiketa: neu

Adibidea:
Paragrafoa: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

# Prompt guztiak egituratuta. 1, 2, 3 eta 4 froga bakoitzeko 3 prompt.
prompt_few_shot_1_dict = {
    1: [prompt_few_shot_1__1_1, prompt_few_shot_1__1_2, prompt_few_shot_1__1_3],
    2: [prompt_few_shot_1__2_1, prompt_few_shot_1__2_2, prompt_few_shot_1__2_3],
    3: [prompt_few_shot_1__3_1, prompt_few_shot_1__3_2, prompt_few_shot_1__3_3],
    4: [prompt_few_shot_1__4_1, prompt_few_shot_1__4_2, prompt_few_shot_1__4_3],
}





# == FEW-SHOT - BI ADIBIDEREKIN ==
prompt_few_shot_2__1_1 = """Aztertu testu bakoitzaren jarrera eta sailkatu ondorengo kategorietako batean:
- pos (positiboa)
- neu (neutroa)
- neg (negatiboa)

Erantzuna **bakarrik** etiketa hauetako bat izan behar da: "pos", "neu" edo "neg". Ez eman azalpenik.

Adibideak:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Pausuz pausu, modu dialektiko batean, elkarrizketa lanabesa izango da, komunean daukagunetik abiatu eta gehiago urruntzen gaituen punturaino heltzeko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera aztertu egin dugu eta hauxe izango litzateke guk egin dugun egoeraren azterketaren laburpen bat.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Adibidea:
Paragrafoa: Beraz, biktimak aintzat hartu behar dire eta egokitu behar da presondegiko legea eta erbestean daudenak itzuli behar dira, eta tortura erradikatu eta zigortu behar da, eta bortizkeria instituzionala ez da debalde atera behar, eta nola ez, jarduera politikoa ez da zigortuko.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_2__1_2 = """Ondorengo esaldiaren jarrera aztertu eta sailkatu: "pos" (positiboa), "neu" (neutroa) edo "neg" (negatiboa).
**Ez erantzun beste ezer, bakarrik etiketa.**

Adibideak:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Pausuz pausu, modu dialektiko batean, elkarrizketa lanabesa izango da, komunean daukagunetik abiatu eta gehiago urruntzen gaituen punturaino heltzeko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera aztertu egin dugu eta hauxe izango litzateke guk egin dugun egoeraren azterketaren laburpen bat.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Adibidea:
Paragrafoa: Beraz, biktimak aintzat hartu behar dire eta egokitu behar da presondegiko legea eta erbestean daudenak itzuli behar dira, eta tortura erradikatu eta zigortu behar da, eta bortizkeria instituzionala ez da debalde atera behar, eta nola ez, jarduera politikoa ez da zigortuko.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_2__1_3 = """Parlamentuko testu baten jarrera zehaztu behar duzu.
Aukeratu hiru etiketetako bat:
- "pos" (positiboa)
- "neu" (neutroa)
- "neg" (negatiboa)

**Erantzuna soilik etiketa bat izan behar da, azalpenik gabe.**

Adibideak:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Pausuz pausu, modu dialektiko batean, elkarrizketa lanabesa izango da, komunean daukagunetik abiatu eta gehiago urruntzen gaituen punturaino heltzeko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera aztertu egin dugu eta hauxe izango litzateke guk egin dugun egoeraren azterketaren laburpen bat.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Adibidea:
Paragrafoa: Beraz, biktimak aintzat hartu behar dire eta egokitu behar da presondegiko legea eta erbestean daudenak itzuli behar dira, eta tortura erradikatu eta zigortu behar da, eta bortizkeria instituzionala ez da debalde atera behar, eta nola ez, jarduera politikoa ez da zigortuko.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""



prompt_few_shot_2__2_1 = """Analiza el sentimiento del siguiente texto y clasifícalo en una de estas categorías:
- pos (positivo)
- neu (neutral)
- neg (negativo)

La respuesta debe ser **únicamente** una de estas etiquetas: "pos", "neu" o "neg". No des explicaciones.

Ejemplos:
Ejemplo:
Párrafo: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiqueta: pos

Ejemplo:
Párrafo: Queremos aportar nuestra firme voluntad, nuestra disposición al diálogo y nuestro proyecto político y económico en aras de una Euskal Herria mejor, más libre, más justa, más solidaria y más igualitaria.
Etiqueta: pos

Ejemplo:
Párrafo: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiqueta: neu

Ejemplo:
Párrafo: Para hacernos una idea, la presión social en esta Comunidad es de un 28,8 % del PIB que está bastante por debajo de la de España, que es un 30,4 % y está diez puntos por debajo de la presión fiscal europea, que está en un 38,4 %.
Etiqueta: neu

Ejemplo:
Párrafo: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiqueta: neg

Ejemplo:
Párrafo: Ante esta situación, no vemos otra salida que un cambio de paradigma.
Etiqueta: neg

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_few_shot_2__2_2 = """Indica si el siguiente texto es positivo (pos), neutral (neu) o negativo (neg).
**Responde solo con la etiqueta.**

Ejemplos:
Ejemplo:
Párrafo: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiqueta: pos

Ejemplo:
Párrafo: Queremos aportar nuestra firme voluntad, nuestra disposición al diálogo y nuestro proyecto político y económico en aras de una Euskal Herria mejor, más libre, más justa, más solidaria y más igualitaria.
Etiqueta: pos

Ejemplo:
Párrafo: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiqueta: neu

Ejemplo:
Párrafo: Para hacernos una idea, la presión social en esta Comunidad es de un 28,8 % del PIB que está bastante por debajo de la de España, que es un 30,4 % y está diez puntos por debajo de la presión fiscal europea, que está en un 38,4 %.
Etiqueta: neu

Ejemplo:
Párrafo: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiqueta: neg

Ejemplo:
Párrafo: Ante esta situación, no vemos otra salida que un cambio de paradigma.
Etiqueta: neg

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_few_shot_2__2_3 = """Clasifica el sentimiento del siguiente párrafo parlamentario.
Elige solo una de estas etiquetas:
- "pos" (positivo)
- "neu" (neutral)
- "neg" (negativo)

**La respuesta debe ser solo la etiqueta, sin explicaciones.**

Ejemplos:
Ejemplo:
Párrafo: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiqueta: pos

Ejemplo:
Párrafo: Queremos aportar nuestra firme voluntad, nuestra disposición al diálogo y nuestro proyecto político y económico en aras de una Euskal Herria mejor, más libre, más justa, más solidaria y más igualitaria.
Etiqueta: pos

Ejemplo:
Párrafo: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiqueta: neu

Ejemplo:
Párrafo: Para hacernos una idea, la presión social en esta Comunidad es de un 28,8 % del PIB que está bastante por debajo de la de España, que es un 30,4 % y está diez puntos por debajo de la presión fiscal europea, que está en un 38,4 %.
Etiqueta: neu

Ejemplo:
Párrafo: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiqueta: neg

Ejemplo:
Párrafo: Ante esta situación, no vemos otra salida que un cambio de paradigma.
Etiqueta: neg

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_few_shot_2__3_1 = """Classify the sentiment of the following text into one of these categories:
- pos (positive)
- neu (neutral)
- neg (negative)

The answer must be **only** one of these labels: "pos", "neu" or "neg". Do not provide explanations.

Examples in Vasque:
Example:
Paragraph: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Label: pos

Example:
Paragraph: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Label: neu

Example:
Paragraph: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Label: neg

Examples in Spanish:
Example:
Paragraph: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Label: pos

Example:
Paragraph: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Label: neu

Example:
Paragraph: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Label: neg

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""

prompt_few_shot_2__3_2 = """Decide if the sentiment of the text is positive (pos), neutral (neu), or negative (neg).
**Respond with only the label.**

Examples in Vasque:
Example:
Paragraph: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Label: pos

Example:
Paragraph: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Label: neu

Example:
Paragraph: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Label: neg

Examples in Spanish:
Example:
Paragraph: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Label: pos

Example:
Paragraph: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Label: neu

Example:
Paragraph: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Label: neg

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""

prompt_few_shot_2__3_3 = """You are analyzing the sentiment of parliamentary speeches.
Choose only one of the following labels:
- "pos" (positive)
- "neu" (neutral)
- "neg" (negative)

The response must be **only the label**.

Examples in Vasque:
Example:
Paragraph: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Label: pos

Example:
Paragraph: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Label: neu

Example:
Paragraph: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Label: neg

Examples in Spanish:
Example:
Paragraph: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Label: pos

Example:
Paragraph: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Label: neu

Example:
Paragraph: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Label: neg

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""



prompt_few_shot_2__4_1 = """Ondorengo testuaren jarrera sailkatu honako kategoria hauetako batean:
- pos (positiboa)
- neu (neutroa)
- neg (negatiboa)

Erantzuna izan behar da **etiketa bakarra**: "pos", "neu" edo "neg". Ez eman azalpenik.

Adibideak euskaraz:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Pausuz pausu, modu dialektiko batean, elkarrizketa lanabesa izango da, komunean daukagunetik abiatu eta gehiago urruntzen gaituen punturaino heltzeko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera aztertu egin dugu eta hauxe izango litzateke guk egin dugun egoeraren azterketaren laburpen bat.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Adibidea:
Paragrafoa: Beraz, biktimak aintzat hartu behar dire eta egokitu behar da presondegiko legea eta erbestean daudenak itzuli behar dira, eta tortura erradikatu eta zigortu behar da, eta bortizkeria instituzionala ez da debalde atera behar, eta nola ez, jarduera politikoa ez da zigortuko.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiketa: pos

Adibidea:
Paragrafoa: Queremos aportar nuestra firme voluntad, nuestra disposición al diálogo y nuestro proyecto político y económico en aras de una Euskal Herria mejor, más libre, más justa, más solidaria y más igualitaria.
Etiketa: pos

Adibidea:
Paragrafoa: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiketa: neu

Adibidea:
Paragrafoa: Para hacernos una idea, la presión social en esta Comunidad es de un 28,8 % del PIB que está bastante por debajo de la de España, que es un 30,4 % y está diez puntos por debajo de la presión fiscal europea, que está en un 38,4 %.
Etiketa: neu

Adibidea:
Paragrafoa: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiketa: neg

Adibidea:
Paragrafoa: Ante esta situación, no vemos otra salida que un cambio de paradigma.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_2__4_2 = """Esaldiaren jarrera identifikatu eta sailkatu: "pos", "neu" edo "neg".
**Ez idatzi beste ezer.**

Adibideak euskaraz:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Pausuz pausu, modu dialektiko batean, elkarrizketa lanabesa izango da, komunean daukagunetik abiatu eta gehiago urruntzen gaituen punturaino heltzeko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera aztertu egin dugu eta hauxe izango litzateke guk egin dugun egoeraren azterketaren laburpen bat.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Adibidea:
Paragrafoa: Beraz, biktimak aintzat hartu behar dire eta egokitu behar da presondegiko legea eta erbestean daudenak itzuli behar dira, eta tortura erradikatu eta zigortu behar da, eta bortizkeria instituzionala ez da debalde atera behar, eta nola ez, jarduera politikoa ez da zigortuko.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiketa: pos

Adibidea:
Paragrafoa: Queremos aportar nuestra firme voluntad, nuestra disposición al diálogo y nuestro proyecto político y económico en aras de una Euskal Herria mejor, más libre, más justa, más solidaria y más igualitaria.
Etiketa: pos

Adibidea:
Paragrafoa: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiketa: neu

Adibidea:
Paragrafoa: Para hacernos una idea, la presión social en esta Comunidad es de un 28,8 % del PIB que está bastante por debajo de la de España, que es un 30,4 % y está diez puntos por debajo de la presión fiscal europea, que está en un 38,4 %.
Etiketa: neu

Adibidea:
Paragrafoa: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiketa: neg

Adibidea:
Paragrafoa: Ante esta situación, no vemos otra salida que un cambio de paradigma.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_2__4_3 = """Parlamentuko esaldi edo pasarte baten jarrera aztertu eta sailkatu:
- "pos" (positiboa)
- "neu" (neutroa)
- "neg" (negatiboa)

**Erantzuna izan behar da soilik etiketa bat, azalpenik gabe.**

Adibideak euskaraz:
Adibidea:
Paragrafoa: Agerian jarri nahi dugu posiblea dela politika beste modu batera egitea. Badagoela posibilitatea baldin eta borondatea badago beste politika bat egiteko eta politika hori beste modu batera egiteko.
Etiketa: pos

Adibidea:
Paragrafoa: Pausuz pausu, modu dialektiko batean, elkarrizketa lanabesa izango da, komunean daukagunetik abiatu eta gehiago urruntzen gaituen punturaino heltzeko.
Etiketa: pos

Adibidea:
Paragrafoa: Alderdi guztien artean mintzatu beharko dugu adosteko nola eramango dugun aurrera eskubide hau. Helburu politikoak ezarri beharko ditugu aurretik, azken muga definitu beharko dugu, eta gero ikusiko dugu nolako baliabideak erabiliko ditugu horretarako.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera aztertu egin dugu eta hauxe izango litzateke guk egin dugun egoeraren azterketaren laburpen bat.
Etiketa: neu

Adibidea:
Paragrafoa: Ez dut esango burujabetzak arazo guztiak konponduko dituenik.
Etiketa: neg

Adibidea:
Paragrafoa: Beraz, biktimak aintzat hartu behar dire eta egokitu behar da presondegiko legea eta erbestean daudenak itzuli behar dira, eta tortura erradikatu eta zigortu behar da, eta bortizkeria instituzionala ez da debalde atera behar, eta nola ez, jarduera politikoa ez da zigortuko.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Por eso hemos venido aquí. Porque amamos este país profundamente. Porque amamos a sus gentes. Porque nos duelen sus dolores, nos entristecen sus penas y nos alegran sus alegrías. Y queremos darles respuestas a los problemas que les agobian.
Etiketa: pos

Adibidea:
Paragrafoa: Queremos aportar nuestra firme voluntad, nuestra disposición al diálogo y nuestro proyecto político y económico en aras de una Euskal Herria mejor, más libre, más justa, más solidaria y más igualitaria.
Etiketa: pos

Adibidea:
Paragrafoa: Y por eso, precisamente por eso, de lo primero que voy a hablar es de de soberanía, por que es el quid de la cuestión. Es el eje de todos los puntos que trataré en estos noventa minutos, y en los siguientes meses y años.
Etiketa: neu

Adibidea:
Paragrafoa: Para hacernos una idea, la presión social en esta Comunidad es de un 28,8 % del PIB que está bastante por debajo de la de España, que es un 30,4 % y está diez puntos por debajo de la presión fiscal europea, que está en un 38,4 %.
Etiketa: neu

Adibidea:
Paragrafoa: Porque nuestro objetivo no es hacer un texto que se guarde en un cajón siete años bajo siete llaves y que se olvide para siempre.
Etiketa: neg

Adibidea:
Paragrafoa: Ante esta situación, no vemos otra salida que un cambio de paradigma.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

# Prompt guztiak egituratuta. 1, 2, 3 eta 4 froga bakoitzeko 3 prompt.
prompt_few_shot_2_dict = {
    1: [prompt_few_shot_2__1_1, prompt_few_shot_2__1_2, prompt_few_shot_2__1_3],
    2: [prompt_few_shot_2__2_1, prompt_few_shot_2__2_2, prompt_few_shot_2__2_3],
    3: [prompt_few_shot_2__3_1, prompt_few_shot_2__3_2, prompt_few_shot_2__3_3],
    4: [prompt_few_shot_2__4_1, prompt_few_shot_2__4_2, prompt_few_shot_2__4_3],
}