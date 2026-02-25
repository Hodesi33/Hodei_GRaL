import torch
import pandas as pd
import re
import time
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
#from huggingface_hub import login # Ez da beharrezkoa terminaletik login egin bada

from prompts_v1 import *





# |----------------------------------------------------------------------------------------------------|
# |--------------------------------------- EREDUA KONFIGURATZEA ---------------------------------------|
# |----------------------------------------------------------------------------------------------------|

# Modeloa aukeratu (deskomentatu erabiliko dena eta komentatu gainerakoak)
# Oharra: Zenbait modelo erabiltzeko (adib. Llama) Hugging Face-eko tokena behar da.

# MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
# IRTEERA_FITXATEGIA = "llama3.1-8B.csv"

# MODEL_NAME = "HiTZ/Latxa-Llama-3.1-8B-Instruct"
# IRTEERA_FITXATEGIA = "latxa3.1-8B.csv"

# MODEL_NAME = "BSC-LT/salamandra-7b-instruct"
# IRTEERA_FITXATEGIA = "salamandra-7B.csv"

# MODEL_NAME = "meta-llama/Llama-3.1-70B-Instruct" #HAU BUKAERAN!
# IRTEERA_FITXATEGIA = "llama3.1-70B.csv"

MODEL_NAME = "HiTZ/Latxa-Llama-3.1-70B-Instruct" #HAU BUKAERAN!
IRTEERA_FITXATEGIA = "latxa3.1-70B.csv"


# Tokenizer-a eta modeloa behar direnean kargatzen dira
tokenizer = None
model = None



def load_model():
    """
    Modeloa modu 'lazy'-n kargatzen du (behin bakarrik) eta ondoren berrerabiltzen du.

    Return
    ------
    tuple
        (tokenizer, model) bikotea.
    """
    global tokenizer, model

    if tokenizer is not None and model is not None:
        return tokenizer, model

    print("Modeloa kargatzen...")

    # 70B modeloetan, 4-bit kuantizazioa normalean beharrezkoa da VRAM arazoak ekiditeko
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        torch_dtype=torch.float16,
        quantization_config=bnb_config
    )

    # Inferentziarako modua aktibatu
    model.eval()

    print("Modeloa kargatuta.")
    return tokenizer, model





# |----------------------------------------------------------------------------------------------------|
# |------------------------------------------ SYSTEM PROMPT -------------------------------------------|
# |----------------------------------------------------------------------------------------------------|

# # PromptMotza
# SYSTEM_PROMPT = """You are a strict sentiment classifier for parliamentary texts.

# Default to NEU:
# - If there is no explicit evaluation (good/bad, success/failure, improvement/problem, benefit/harm), output neu.
# - Greetings, thanks, procedural talk, lists of facts/numbers, announcements, plans, meetings -> neu.

# pos only with explicit positive evaluation.
# neg only with explicit negative evaluation.

# Output EXACTLY one label: pos, neu, or neg
# """





# PromptLuzea
SYSTEM_PROMPT = """You are a strict sentiment classifier for parliamentary texts.

DECISION PRINCIPLE (most important):
- Choose pos/neg ONLY when the sentence contains an explicit overall evaluation.
- If the sentence is mostly factual, procedural, institutional, descriptive, or just reporting actions, default to: neu.

What counts as EXPLICIT evaluation:
- Positive evaluation: praise, success, improvement, benefit, good results, fulfillment, effective action, congratulations.
- Negative evaluation: criticism, failure, worsening, harm, problems, unacceptable situation, victims, losses, serious concern.

What does NOT count as positive or negative by itself (usually NEU unless evaluation words are present):
- Greetings and formalities: "egun on", "eskerrik asko", "lehendakari", "sailburu", etc.
- Announcements / intentions / plans / proposals: "we will", "we propose", "we intend", "we want", "it is planned".
- Procedural or institutional actions: "presented", "approved", "reported", "held a meeting", "registered", "published".
- Descriptions, lists, numbers, places, dates, counts of workers, budget figures, references to laws or programs.

Important domain rule:
- Do NOT infer sentiment from topic (e.g., "youth", "industry", "justice") or from the fact that an action is mentioned.
- Government action, measures, programs, investments, laws, agreements are NOT positive by default.
- A sentence can mention a problem factually and still be neu if there is no evaluative judgement.

If the sentence mixes facts and mild subjective language, decide the overall polarity:
- If clearly positive overall -> pos
- If clearly negative overall -> neg
- If unclear / balanced / mainly descriptive -> neu

Output rules:
- Output EXACTLY one label: pos, neu, or neg
- No punctuation, no explanations, no extra words
"""





# # PromptBerria1
# SYSTEM_PROMPT = """You are a sentiment classifier for parliamentary texts.

# GOAL:
# Classify the sentence as pos / neu / neg based on the speaker's evaluative stance.

# CORE RULE:
# - Use pos/neg only when the sentence contains a CLEAR evaluation of performance, situation, or responsibility.
# - If the sentence is mostly descriptive, procedural, contextual, or just states goals/values without judging results -> neu.

# NEGATIVE (neg) if the sentence:
# - Criticizes, blames, or signals failure/insufficiency (explicit or implicit).
# - Highlights harm, losses, victims, discrimination, fraud, corruption, crisis, unacceptable situations.
# - Uses negative judgement words (e.g., wrong, serious, unacceptable, failure, poor results) OR
#   implies inadequacy through normative contrast: "should/need/must" + current reality is not meeting it.

# POSITIVE (pos) if the sentence:

# - Expresses approval, support, defense, or endorsement of an action, policy, idea, or actor.
# - Describes something as important, appropriate, fair, necessary, valuable, beneficial, reasonable, or justified.
# - Presents an institutional achievement, status, recognition, or distinction in a favorable way.
# - Uses clearly positive evaluative language, even if it does not explicitly mention measurable success.
# - Frames a situation as desirable or correct.

# Do NOT require explicit proof of success.

# IMPORTANT RESTRICTION (avoid over-predicting pos):
# - Mere mentions of positive values/goals (justice, equality, cooperation, peace, rights, future, cohesion)
#   are NOT pos by themselves.
#   They are neu unless the speaker clearly:
#   (a) expresses approval/support/endorsement, OR
#   (b) describes something as beneficial/appropriate/fair/necessary/valuable, OR
#   (c) frames an outcome/status/recognition as positive.
# - Plans, intentions, proposals, or recommendations are neu unless they include clear praise/support (pos)
#   or clear criticism/problem framing (neg).

# NEUTRAL (neu) if the sentence:
# - Is a greeting, thanks without evaluation, formalities.
# - Reports facts, numbers, dates, lists, institutional steps, laws, meetings.
# - Describes a situation without judging it (no blame/praise, no success/failure).

# MIXED SENTENCES:
# - If both appear, choose the dominant evaluation.
# - If the main purpose is to propose improvements without judging current performance -> neu.
# - If the proposal implies current failure/insufficiency -> neg.

# Output:
# - Output EXACTLY one label: pos, neu, or neg
# - No punctuation, no explanations, no extra words
# """





# #PromptBerria2
# SYSTEM_PROMPT = """You are a sentiment classifier for parliamentary texts.

# GOAL:
# Classify each sentence as:
# - pos (positive)
# - neu (neutral)
# - neg (negative)

# CORE PRINCIPLE:
# Classify the OVERALL evaluative stance of the sentence.
# Only use pos or neg when there is a clear evaluative attitude.
# If the sentence is mainly descriptive, procedural, strategic, or organizational, classify it as neu.

# ------------------------------------------------------------
# NEGATIVE (neg)
# ------------------------------------------------------------
# Classify as neg if the sentence:

# - Criticizes, blames, or questions an action, policy, institution, or actor.
# - Signals failure, insufficiency, injustice, harm, discrimination, corruption, fraud, crisis, loss, or damage.
# - Uses clearly negative evaluative language (e.g., unacceptable, incoherent, wrong, serious problem, mistake).
# - Implies inadequacy through contrast (e.g., “should”, “must”, “need to”) when it suggests the current situation is insufficient.
# - Frames something as lacking legitimacy, lacking foundation, or being problematic.

# Implicit criticism counts as neg if the overall intention is clearly critical.

# ------------------------------------------------------------
# POSITIVE (pos)
# ------------------------------------------------------------
# Classify as pos if the sentence:

# - Expresses approval, support, endorsement, or defense of an action, policy, idea, or actor.
# - Describes something as important, appropriate, fair, necessary, valuable, reasonable, justified, beneficial, or correct.
# - Presents an institutional achievement, recognition, distinction, or status in a favorable way.
# - Clearly frames something as desirable, legitimate, or worthy of support.
# - Uses positive evaluative language directed at performance, decisions, or outcomes.

# Do NOT require explicit proof of measurable success.
# Clear positive evaluation or endorsement is sufficient.

# Do NOT classify as pos if the sentence merely states a policy goal,
# agenda item, strategic line, or general value without expressing approval
# or positive judgement about performance or results.

# Do not classify as pos if the positive wording refers only to abstract principles or rhetorical emphasis without clear endorsement.

# ------------------------------------------------------------
# NEUTRAL (neu)
# ------------------------------------------------------------
# Classify as neu if the sentence:

# - Reports facts, data, numbers, dates, procedures, meetings, laws, or institutional steps.
# - Is mainly descriptive or explanatory.
# - Contains greetings, formalities, or short procedural remarks.
# - States a proposal, request, or recommendation without clear praise or criticism.
# - Mentions positive values (justice, equality, empowerment, cooperation, rights, development, cohesion, etc.)
#   as part of an agenda or program without evaluating results.
# - States strategic lines, policy objectives, or programmatic priorities.
# - Refers to something as "important" in a procedural, structural, or organizational way
#   (e.g., “third strategic line”, “we said something important last year”).
# - Is primarily programmatic rather than evaluative.

# If there is no clear approval or criticism, default to neu.

# ------------------------------------------------------------
# MIXED SENTENCES
# ------------------------------------------------------------
# If both positive and negative elements appear:
# - Choose the dominant evaluative direction.
# - If evaluation is secondary and the sentence is mainly descriptive or programmatic → neu.

# ------------------------------------------------------------
# OUTPUT RULES
# ------------------------------------------------------------
# - Output EXACTLY one label: pos, neu, or neg
# - No punctuation
# - No explanations
# - No additional text
# """





# |----------------------------------------------------------------------------------------------------|
# |------------------------------------------- INFERENTZIA --------------------------------------------|
# |----------------------------------------------------------------------------------------------------|

def inferentzia(user_prompt: str, max_new_tokens: int = 10) -> str:
    """
    Inferentzia egiten du, system prompt-a eta chat template-a erabiliz.

    Parametroak
    ----------
    user_prompt : str
        Erabiltzailearen prompt-a (txertatutako paragrafoarekin).
    max_new_tokens : int
        Sortuko den irteeraren token kopuru maximoa.

    Return
    ------
    str
        Modeloaren dekodetutako irteera (minuskulaz eta zuriunez garbituta).
    """
    load_model()

    # System + user mezuak definitu
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    # Tokenizer-ak chat template onartzen badu, hori erabiltzen da
    if hasattr(tokenizer, "apply_chat_template"):
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    else:
        # Bestela, system prompt-a aurretik itsasten da
        prompt = SYSTEM_PROMPT + "\n" + user_prompt

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Inferentzia determinista: do_sample=False
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    # Prompt-aren ondorengo zatia bakarrik dekodetu
    decoded = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[-1]:],
        skip_special_tokens=True
    ).strip().lower()

    print(f"[DEBUG] Decoded: {decoded}")
    return decoded





# |----------------------------------------------------------------------------------------------------|
# |----------------------------------- PARAGRAFO BAKOITZA AZTERTZEA -----------------------------------|
# |----------------------------------------------------------------------------------------------------|

def paragrafoa_aztertu(text: str, froga: int, prompt_dict):
    """
    Paragrafo bati froga/prompt desberdinak aplikatzen dizkio, eta irteera-labela (pos/neu/neg) esleitzen du.

    Parametroak
    ----------
    text : str
        Aztertu beharreko paragrafoa.
    froga : int
        Aplikatu beharreko froga-zenbakia (prompt multzoa aukeratzeko).
    prompt_dict : dict
        Froga bakoitzerako prompt zerrendak dituen egitura.

    Return
    ------
    list[dict]
        Prompt bakoitzeko emaitzen zerrenda (etiketa eta exekuzio-denborarekin).
    """
    prompts = prompt_dict[froga]
    emaitzak = []

    for idx, prompt_template in enumerate(prompts):
        prompt = prompt_template.format(paragrafoa=text)

        start_time = time.time()
        decoded = inferentzia(prompt)
        elapsed_time = time.time() - start_time

        # Modeloaren irteeratik etiketa estandarra normalizatu (pos/neu/neg)
        m = re.search(r"\b(pos|neu|neg|positive|neutral|negative|positiboa|neutroa|negatiboa|positivo|neutral|negativo)\b", decoded)
        if m:
            lab = m.group(1)
            if lab.startswith("pos"):
                label = "pos"
            elif lab.startswith("neg"):
                label = "neg"
            else:
                label = "neu"
        else:
            # Match-ik ez badago, neu lehenesten da
            label = "neu"

        emaitzak.append({
            "Froga": froga,
            "Prompt": idx + 1,
            "Erabilitako_prompta": prompt,
            "Modeloaren_emaitza": decoded[:500], # CSV-a gehiegi ez handitzeko, irteera mozten da
            "Label": label,
            "Exec_time": elapsed_time
        })

    return emaitzak





# |----------------------------------------------------------------------------------------------------|
# |---------------------------------------- METRIKEN KALKULUA -----------------------------------------|
# |----------------------------------------------------------------------------------------------------|

def calculate_metrics(df_emaitzak: pd.DataFrame) -> pd.DataFrame:
    """
    (Froga, Prompt) bakoitzeko eta froga bakoitzeko (GLOBAL) metrikak kalkulatzen ditu.

    Parametroak
    ----------
    df_emaitzak : pd.DataFrame
        Emaitzen taula (Label_real eta Decoded_label zutabeekin).

    Return
    ------
    pd.DataFrame
        Metriken taula (Accuracy, Precision/Recall/F1 macro eta weighted, eta exekuzio-denboraren batez bestekoa).
    """
    metrics = []

    # (Froga, Prompt) konbinazio bakoitzerako metrikak
    grouped = df_emaitzak.groupby(["Froga", "Prompt"])
    for (froga, prompt), group in grouped:
        y_true = group["Label_real"]
        y_pred = group["Decoded_label"]

        metrics.append({
            "Froga": froga,
            "Prompt": prompt,
            "Accuracy": accuracy_score(y_true, y_pred),
            "Precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
            "Recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
            "F1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
            "Precision_weighted": precision_score(y_true, y_pred, average="weighted", zero_division=0),
            "Recall_weighted": recall_score(y_true, y_pred, average="weighted", zero_division=0),
            "F1_weighted": f1_score(y_true, y_pred, average="weighted", zero_division=0),
            "Avg_exec_time": group["Exec_time"].mean()
        })
    
    # Froga bakoitzerako metrika globalak
    grouped_froga = df_emaitzak.groupby("Froga")
    for froga, group in grouped_froga:
        y_true = group["Label_real"]
        y_pred = group["Decoded_label"]

        metrics.append({
            "Froga": froga,
            "Prompt": "GLOBAL",
            "Accuracy": accuracy_score(y_true, y_pred),
            "Precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
            "Recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
            "F1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
            "Precision_weighted": precision_score(y_true, y_pred, average="weighted", zero_division=0),
            "Recall_weighted": recall_score(y_true, y_pred, average="weighted", zero_division=0),
            "F1_weighted": f1_score(y_true, y_pred, average="weighted", zero_division=0),
            "Avg_exec_time": group["Exec_time"].mean()
        })

    return pd.DataFrame(metrics).sort_values(by=["Froga", "Prompt"])





# |----------------------------------------------------------------------------------------------------|
# |----------------------------------- CONFUSION MATRIX-AK SORTZEA ------------------------------------|
# |----------------------------------------------------------------------------------------------------|

def _plot_confusion_matrix(cm: np.ndarray, labels: list[str], title: str, out_png: str):
    """
    Confusion matrix bat marrazten du eta PNG gisa gordetzen du.

    Parametroak
    ----------
    cm : np.ndarray
        Confusion matrix-aren balioak.
    labels : list[str]
        Etiketen ordena (adib. ["pos", "neu", "neg"]).
    title : str
        Irudiaren titulua.
    out_png : str
        PNG fitxategiaren irteera-bidea.

    Return
    ------
    None
    """
    fig, ax = plt.subplots()
    im = ax.imshow(cm)

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_title(title)

    # Balioak gelaxketan idatzi
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")

    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(out_png, dpi=200)
    plt.close(fig)


def create_confusion_matrixes(
    df_emaitzak: pd.DataFrame,
    out_dir: str,
    labels: list[str],
    save_csv: bool = True
):
    """
    (Froga, Prompt) bakoitzeko eta Froga bakoitzeko (GLOBAL) confusion matrix-ak sortu eta gordetzen ditu.

    Irteerak:
    - PNG: irudi moduan
    - CSV (aukerakoa): balio-taula fitxategi gisa

    Parametroak
    ----------
    df_emaitzak : pd.DataFrame
        Emaitzen taula (Label_real eta Decoded_label zutabeekin).
    out_dir : str
        Irudiak/CSVak gordetzeko karpeta.
    labels : list[str]
        Etiketen ordena confusion_matrix funtziorako.
    save_csv : bool
        True bada, CSV fitxategiak ere sortzen dira.

    Return
    ------
    None
    """
    if labels is None:
        labels = ["pos", "neu", "neg"]

    os.makedirs(out_dir, exist_ok=True)

    # (Froga, Prompt) bakoitzeko confusion matrix-a
    grouped = df_emaitzak.groupby(["Froga", "Prompt"])
    for (froga, prompt), group in grouped:
        y_true = group["Label_real"].astype(str)
        y_pred = group["Decoded_label"].astype(str)

        cm = confusion_matrix(y_true, y_pred, labels=labels)

        title = f"Confusion Matrix - Froga {froga} - Prompt {prompt}"
        base = f"froga_{froga}_prompt_{prompt}"

        out_png = os.path.join(out_dir, base + ".png")
        _plot_confusion_matrix(cm, labels, title, out_png)

        if save_csv:
            out_csv = os.path.join(out_dir, base + ".csv")
            pd.DataFrame(cm, index=[f"true_{l}" for l in labels], columns=[f"pred_{l}" for l in labels]) \
              .to_csv(out_csv, encoding="utf-8")

    # Froga bakoitzeko GLOBAL confusion matrix-a
    grouped_froga = df_emaitzak.groupby("Froga")
    for froga, group in grouped_froga:
        y_true = group["Label_real"].astype(str)
        y_pred = group["Decoded_label"].astype(str)

        cm = confusion_matrix(y_true, y_pred, labels=labels)

        title = f"Confusion Matrix - Froga {froga} - GLOBAL"
        base = f"froga_{froga}_GLOBAL"

        out_png = os.path.join(out_dir, base + ".png")
        _plot_confusion_matrix(cm, labels, title, out_png)

        if save_csv:
            out_csv = os.path.join(out_dir, base + ".csv")
            pd.DataFrame(cm, index=[f"true_{l}" for l in labels], columns=[f"pred_{l}" for l in labels]) \
              .to_csv(out_csv, encoding="utf-8")





# |----------------------------------------------------------------------------------------------------|
# |----------------------------------------- PROZESU NAGUSIA ------------------------------------------|
# |----------------------------------------------------------------------------------------------------|

def sentiment_analysis(input_csv: str, analysis_type: str):
    """
    Sentiment analysis prozesu nagusia exekutatzen du.

    Prozesua:
    - Sarrerako CSV-a irakurri.
    - analysis_type arabera prompt multzoa aukeratu.
    - Testu bakoitzean froga multzo egokia aplikatu (hizkuntzaren arabera).
    - Emaitzak (decoded) eta metrikak CSV fitxategietan gorde.
    - Confusion matrix-ak sortu (PNG eta CSV).

    Parametroak
    ----------
    input_csv : str
        Sarrerako CSV fitxategiaren bidea.
    analysis_type : str
        Analisi mota: "zero-shot", "few-shot-1" edo "few-shot-2".

    Return
    ------
    pd.DataFrame | None
        Emaitzen DataFrame-a; sarrera fitxategia ez bada aurkitzen, None.
    """
    partition = input_csv.replace(".csv", "")
    irteera_fitxategia_decoded = f"emaitzak/emaitzak_sentiment_v1_SysPromptBerria1/{analysis_type}/{partition}/decoded/{IRTEERA_FITXATEGIA}"
    irteera_fitxategia_metrics = f"emaitzak/emaitzak_sentiment_v1_SysPromptBerria1/{analysis_type}/{partition}/metrics/{IRTEERA_FITXATEGIA}"
    irteera_fitxategia_confusion = f"emaitzak/emaitzak_sentiment_v1_SysPromptBerria1/{analysis_type}/{partition}/confusion_matrixes/{IRTEERA_FITXATEGIA.replace('.csv','')}"

    # Sarrera irakurri
    try:
        df_input = pd.read_csv(input_csv, encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: ezin izan da sarrera fitxategia aurkitu: {input_csv}")
        return None

    # Prompt multzoa aukeratu
    if analysis_type == "zero-shot":
        prompt_dict = prompt_zero_shot_dict
    elif analysis_type == "few-shot-1":
        prompt_dict = prompt_few_shot_1_dict
    elif analysis_type == "few-shot-2":
        prompt_dict = prompt_few_shot_2_dict
    else:
        raise ValueError(f"Unknown analysis type: {analysis_type}")

    emaitza_guztiak = []

    # Testu bakoitza aztertu
    for _, row in df_input.iterrows():
        text = row["Text"]
        language = str(row["Language"]).lower()

        # Hizkuntzaren arabera frogak aukeratu
        if language == "eu":
            frogak = [1, 3, 4]
        elif language == "es":
            frogak = [2, 3, 4]
        else:
            print(f"Hizkuntza ezezaguna {row.get('Text_id', '???')} lerroan: {language}")
            continue

        for froga in frogak:
            emaitzak = paragrafoa_aztertu(text, froga, prompt_dict)

            for e in emaitzak:
                label_real = row["Label"]
                result = 1 if label_real == e["Label"] else 0

                emaitza_guztiak.append({
                    "Text_id": row["Text_id"],
                    "Text": text,
                    "Language": language,
                    "Froga": e["Froga"],
                    "Prompt": e["Prompt"],
                    "Erabilitako_prompta": e["Erabilitako_prompta"], # Hau komentatu prompt-a ez baduzu gorde nahi
                    "Modeloaren_emaitza": e["Modeloaren_emaitza"], # Hau komentatu ez baduzu gorde nahi modeloak bueltatu duena
                    "Decoded_label": e["Label"],
                    "Label_real": label_real,
                    "Result": result,
                    "Exec_time": e["Exec_time"]
                })

    # Irteera-karpetak sortu
    os.makedirs(os.path.dirname(irteera_fitxategia_decoded), exist_ok=True)
    os.makedirs(os.path.dirname(irteera_fitxategia_metrics), exist_ok=True)

    # Decoded emaitzak gorde
    df_emaitzak = pd.DataFrame(emaitza_guztiak)
    df_emaitzak.to_csv(irteera_fitxategia_decoded, index=False, encoding="utf-8")
    print(f"[INFO] Emaitzak gordeta: {irteera_fitxategia_decoded}")

    # Metrikak kalkulatu eta gorde
    df_metrics = calculate_metrics(df_emaitzak)
    df_metrics.to_csv(irteera_fitxategia_metrics, index=False, encoding="utf-8")
    print(f"[INFO] Metrikak gordeta: {irteera_fitxategia_metrics}")

    # Confusion matrix-ak sortu eta gorde
    create_confusion_matrixes(df_emaitzak, irteera_fitxategia_confusion, labels=["pos", "neu", "neg"], save_csv=True)
    print(f"[INFO] Confusion matrix-ak gordeta: {irteera_fitxategia_confusion}")

    return df_emaitzak
