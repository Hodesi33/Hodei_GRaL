# Hemen nire 12 prompt-ak (few-shot eta zero-shot-enak) definitzen dira, {paragrafoa} barruan paragrafoa sartzeko

# |----------------------------------------------------------------------------------------------------|
# |------------------------------------------- ZERO-SHOT ----------------------------------------------|
# |----------------------------------------------------------------------------------------------------|

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





# |----------------------------------------------------------------------------------------------------|
# |----------------------------------- FEW-SHOT - ADIBIDE BATEKIN -------------------------------------|
# |----------------------------------------------------------------------------------------------------|

prompt_few_shot_1__1_1 = """Aztertu testu bakoitzaren jarrera eta sailkatu ondorengo kategorietako batean:
- pos (positiboa)
- neu (neutroa)
- neg (negatiboa)

Erantzuna **bakarrik** etiketa hauetako bat izan behar da: "pos", "neu" edo "neg". Ez eman azalpenik.

Adibideak:
Adibidea:
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_1__1_2 = """Ondorengo esaldiaren jarrera aztertu eta sailkatu: "pos" (positiboa), "neu" (neutroa) edo "neg" (negatiboa).
**Ez erantzun beste ezer, bakarrik etiketa.**

Adibideak:
Adibidea:
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
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
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
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
Párrafo: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiqueta: pos

Ejemplo:
Párrafo: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiqueta: neu

Ejemplo:
Párrafo: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Etiqueta: neg

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_few_shot_1__2_2 = """Indica si el siguiente texto es positivo (pos), neutral (neu) o negativo (neg).
**Responde solo con la etiqueta.**

Ejemplos:
Ejemplo:
Párrafo: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiqueta: pos

Ejemplo:
Párrafo: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiqueta: neu

Ejemplo:
Párrafo: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
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
Párrafo: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiqueta: pos

Ejemplo:
Párrafo: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiqueta: neu

Ejemplo:
Párrafo: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
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
Paragraph: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Label: pos

Example:
Paragraph: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Label: neu

Example:
Paragraph: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Label: neg

Examples in Spanish:
Example:
Paragraph: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Label: pos

Example:
Paragraph: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Label: neu

Example:
Paragraph: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Label: neg

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""

prompt_few_shot_1__3_2 = """Decide if the sentiment of the text is positive (pos), neutral (neu), or negative (neg).
**Respond with only the label.**

Examples in Vasque:
Example:
Paragraph: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Label: pos

Example:
Paragraph: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Label: neu

Example:
Paragraph: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Label: neg

Examples in Spanish:
Example:
Paragraph: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Label: pos

Example:
Paragraph: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Label: neu

Example:
Paragraph: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
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
Paragraph: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Label: pos

Example:
Paragraph: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Label: neu

Example:
Paragraph: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Label: neg

Examples in Spanish:
Example:
Paragraph: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Label: pos

Example:
Paragraph: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Label: neu

Example:
Paragraph: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
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
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiketa: pos

Adibidea:
Paragrafoa: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiketa: neu

Adibidea:
Paragrafoa: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_1__4_2 = """Esaldiaren jarrera identifikatu eta sailkatu: "pos", "neu" edo "neg".
**Ez idatzi beste ezer.**

Adibideak euskaraz:
Adibidea:
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiketa: pos

Adibidea:
Paragrafoa: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiketa: neu

Adibidea:
Paragrafoa: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
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
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiketa: pos

Adibidea:
Paragrafoa: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiketa: neu

Adibidea:
Paragrafoa: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
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





# |----------------------------------------------------------------------------------------------------|
# |----------------------------------- FEW-SHOT - BI ADIBIDEREKIN -------------------------------------|
# |----------------------------------------------------------------------------------------------------|

prompt_few_shot_2__1_1 = """Aztertu testu bakoitzaren jarrera eta sailkatu ondorengo kategorietako batean:
- pos (positiboa)
- neu (neutroa)
- neg (negatiboa)

Erantzuna **bakarrik** etiketa hauetako bat izan behar da: "pos", "neu" edo "neg". Ez eman azalpenik.

Adibideak:
Adibidea:
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Aurrerapen nabarmena izan da eta herritarren ongizatea handitu da.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Aurrekontua eta egutegia azaldu dira, eta hurrengo urratsak zehaztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Adibidea:
Paragrafoa: Politika honek porrota ekarri du eta arazoa okertu egin da azken hilabeteetan.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_2__1_2 = """Ondorengo esaldiaren jarrera aztertu eta sailkatu: "pos" (positiboa), "neu" (neutroa) edo "neg" (negatiboa).
**Ez erantzun beste ezer, bakarrik etiketa.**

Adibideak:
Adibidea:
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Aurrerapen nabarmena izan da eta herritarren ongizatea handitu da.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Aurrekontua eta egutegia azaldu dira, eta hurrengo urratsak zehaztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Adibidea:
Paragrafoa: Politika honek porrota ekarri du eta arazoa okertu egin da azken hilabeteetan.
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
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Aurrerapen nabarmena izan da eta herritarren ongizatea handitu da.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Aurrekontua eta egutegia azaldu dira, eta hurrengo urratsak zehaztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Adibidea:
Paragrafoa: Politika honek porrota ekarri du eta arazoa okertu egin da azken hilabeteetan.
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
Párrafo: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiqueta: pos

Ejemplo:
Párrafo: Ha habido un avance claro y el bienestar de la ciudadanía ha aumentado.
Etiqueta: pos

Ejemplo:
Párrafo: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiqueta: neu

Ejemplo:
Párrafo: Se han explicado el presupuesto y el calendario, y se han definido los siguientes pasos.
Etiqueta: neu

Ejemplo:
Párrafo: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Etiqueta: neg

Ejemplo:
Párrafo: Esta política ha fracasado y el problema ha empeorado en los últimos meses.
Etiqueta: neg

Párrafo a analizar:
Párrafo: {paragrafoa}
Etiqueta: 
"""

prompt_few_shot_2__2_2 = """Indica si el siguiente texto es positivo (pos), neutral (neu) o negativo (neg).
**Responde solo con la etiqueta.**

Ejemplos:
Ejemplo:
Párrafo: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiqueta: pos

Ejemplo:
Párrafo: Ha habido un avance claro y el bienestar de la ciudadanía ha aumentado.
Etiqueta: pos

Ejemplo:
Párrafo: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiqueta: neu

Ejemplo:
Párrafo: Se han explicado el presupuesto y el calendario, y se han definido los siguientes pasos.
Etiqueta: neu

Ejemplo:
Párrafo: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Etiqueta: neg

Ejemplo:
Párrafo: Esta política ha fracasado y el problema ha empeorado en los últimos meses.
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
Párrafo: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiqueta: pos

Ejemplo:
Párrafo: Ha habido un avance claro y el bienestar de la ciudadanía ha aumentado.
Etiqueta: pos

Ejemplo:
Párrafo: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiqueta: neu

Ejemplo:
Párrafo: Se han explicado el presupuesto y el calendario, y se han definido los siguientes pasos.
Etiqueta: neu

Ejemplo:
Párrafo: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Etiqueta: neg

Ejemplo:
Párrafo: Esta política ha fracasado y el problema ha empeorado en los últimos meses.
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
Paragraph: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Label: pos

Example:
Paragraph: Aurrerapen nabarmena izan da eta herritarren ongizatea handitu da.
Label: pos

Example:
Paragraph: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Label: neu

Example:
Paragraph: Aurrekontua eta egutegia azaldu dira, eta hurrengo urratsak zehaztu dira.
Label: neu

Example:
Paragraph: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Label: neg

Example:
Paragraph: Politika honek porrota ekarri du eta arazoa okertu egin da azken hilabeteetan.
Label: neg

Examples in Spanish:
Example:
Paragraph: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Label: pos

Example:
Paragraph: Ha habido un avance claro y el bienestar de la ciudadanía ha aumentado.
Label: pos

Example:
Paragraph: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Label: neu

Example:
Paragraph: Se han explicado el presupuesto y el calendario, y se han definido los siguientes pasos.
Label: neu

Example:
Paragraph: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Label: neg

Example:
Paragraph: Esta política ha fracasado y el problema ha empeorado en los últimos meses.
Label: neg

Paragraph to analyze:
Paragraph: {paragrafoa}
Label: 
"""

prompt_few_shot_2__3_2 = """Decide if the sentiment of the text is positive (pos), neutral (neu), or negative (neg).
**Respond with only the label.**

Examples in Vasque:
Example:
Paragraph: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Label: pos

Example:
Paragraph: Aurrerapen nabarmena izan da eta herritarren ongizatea handitu da.
Label: pos

Example:
Paragraph: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Label: neu

Example:
Paragraph: Aurrekontua eta egutegia azaldu dira, eta hurrengo urratsak zehaztu dira.
Label: neu

Example:
Paragraph: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Label: neg

Example:
Paragraph: Politika honek porrota ekarri du eta arazoa okertu egin da azken hilabeteetan.
Label: neg

Examples in Spanish:
Example:
Paragraph: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Label: pos

Example:
Paragraph: Ha habido un avance claro y el bienestar de la ciudadanía ha aumentado.
Label: pos

Example:
Paragraph: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Label: neu

Example:
Paragraph: Se han explicado el presupuesto y el calendario, y se han definido los siguientes pasos.
Label: neu

Example:
Paragraph: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Label: neg

Example:
Paragraph: Esta política ha fracasado y el problema ha empeorado en los últimos meses.
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
Paragraph: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Label: pos

Example:
Paragraph: Aurrerapen nabarmena izan da eta herritarren ongizatea handitu da.
Label: pos

Example:
Paragraph: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Label: neu

Example:
Paragraph: Aurrekontua eta egutegia azaldu dira, eta hurrengo urratsak zehaztu dira.
Label: neu

Example:
Paragraph: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Label: neg

Example:
Paragraph: Politika honek porrota ekarri du eta arazoa okertu egin da azken hilabeteetan.
Label: neg

Examples in Spanish:
Example:
Paragraph: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Label: pos

Example:
Paragraph: Ha habido un avance claro y el bienestar de la ciudadanía ha aumentado.
Label: pos

Example:
Paragraph: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Label: neu

Example:
Paragraph: Se han explicado el presupuesto y el calendario, y se han definido los siguientes pasos.
Label: neu

Example:
Paragraph: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Label: neg

Example:
Paragraph: Esta política ha fracasado y el problema ha empeorado en los últimos meses.
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
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Aurrerapen nabarmena izan da eta herritarren ongizatea handitu da.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Aurrekontua eta egutegia azaldu dira, eta hurrengo urratsak zehaztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Adibidea:
Paragrafoa: Politika honek porrota ekarri du eta arazoa okertu egin da azken hilabeteetan.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiketa: pos

Adibidea:
Paragrafoa: Ha habido un avance claro y el bienestar de la ciudadanía ha aumentado.
Etiketa: pos

Adibidea:
Paragrafoa: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiketa: neu

Adibidea:
Paragrafoa: Se han explicado el presupuesto y el calendario, y se han definido los siguientes pasos.
Etiketa: neu

Adibidea:
Paragrafoa: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Etiketa: neg

Adibidea:
Paragrafoa: Esta política ha fracasado y el problema ha empeorado en los últimos meses.
Etiketa: neg

Aztertzeko esaldia:
Paragrafoa: {paragrafoa}
Etiketa: 
"""

prompt_few_shot_2__4_2 = """Esaldiaren jarrera identifikatu eta sailkatu: "pos", "neu" edo "neg".
**Ez idatzi beste ezer.**

Adibideak euskaraz:
Adibidea:
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Aurrerapen nabarmena izan da eta herritarren ongizatea handitu da.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Aurrekontua eta egutegia azaldu dira, eta hurrengo urratsak zehaztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Adibidea:
Paragrafoa: Politika honek porrota ekarri du eta arazoa okertu egin da azken hilabeteetan.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiketa: pos

Adibidea:
Paragrafoa: Ha habido un avance claro y el bienestar de la ciudadanía ha aumentado.
Etiketa: pos

Adibidea:
Paragrafoa: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiketa: neu

Adibidea:
Paragrafoa: Se han explicado el presupuesto y el calendario, y se han definido los siguientes pasos.
Etiketa: neu

Adibidea:
Paragrafoa: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Etiketa: neg

Adibidea:
Paragrafoa: Esta política ha fracasado y el problema ha empeorado en los últimos meses.
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
Paragrafoa: Neurri hauei esker, zerbitzua hobetu da eta emaitzak positiboak izan dira.
Etiketa: pos

Adibidea:
Paragrafoa: Aurrerapen nabarmena izan da eta herritarren ongizatea handitu da.
Etiketa: pos

Adibidea:
Paragrafoa: Gaurko bilkuran bi puntu eztabaidatu dira eta txostenaren datuak aurkeztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Aurrekontua eta egutegia azaldu dira, eta hurrengo urratsak zehaztu dira.
Etiketa: neu

Adibidea:
Paragrafoa: Egoera larria da eta hartutako neurriak ez dira nahikoak; ondorioak kaltegarriak dira.
Etiketa: neg

Adibidea:
Paragrafoa: Politika honek porrota ekarri du eta arazoa okertu egin da azken hilabeteetan.
Etiketa: neg

Adibideak gaztelaniaz:
Adibidea:
Paragrafoa: Gracias a estas medidas, el servicio ha mejorado y los resultados han sido positivos.
Etiketa: pos

Adibidea:
Paragrafoa: Ha habido un avance claro y el bienestar de la ciudadanía ha aumentado.
Etiketa: pos

Adibidea:
Paragrafoa: En la sesión de hoy se han tratado dos puntos y se han presentado los datos del informe.
Etiketa: neu

Adibidea:
Paragrafoa: Se han explicado el presupuesto y el calendario, y se han definido los siguientes pasos.
Etiketa: neu

Adibidea:
Paragrafoa: La situación es grave y las medidas tomadas no son suficientes; las consecuencias son perjudiciales.
Etiketa: neg

Adibidea:
Paragrafoa: Esta política ha fracasado y el problema ha empeorado en los últimos meses.
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