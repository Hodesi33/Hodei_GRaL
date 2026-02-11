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

from prompts import *


# === SYSTEM PROMPT (PORTAERA KONTROLA) ===
SYSTEM_PROMPT = """You are a strict sentiment classifier for parliamentary texts.

Classification criterion:
- Do NOT infer the speaker's intent, stance, or subjective tone.
- Classify the sentence based on its overall polarity as a whole.

Label definitions:
- pos: the sentence expresses an overall positive evaluation (benefits, improvements, praise, positive outcomes).
- neg: the sentence expresses an overall negative evaluation (problems, criticism, failures, harmful outcomes).
- neu: the sentence is descriptive, factual, or procedural, with no overall positive or negative evaluation.

Output rules:
- Output EXACTLY one label: pos, neu, or neg
- No punctuation, no explanations, no extra words
"""


# =========================================================
# === MODELOA (CACHE + ALDAKETA AUTOMATIKOA)
# =========================================================

tokenizer = None
model = None
_current_model_name = None


def load_model(model_name: str, use_4bit: bool = True):
    """
    Modeloa kargatzen du. Modeloa aldatzen bada, berriro kargatzen du.
    Cache moduan funtzionatzen du: model_name bera bada, berrerabili.
    """
    global tokenizer, model, _current_model_name

    if tokenizer is not None and model is not None and _current_model_name == model_name:
        return tokenizer, model

    print(f"[INFO] Modeloa kargatzen: {model_name}")

    # Aurreko modeloa askatu (memoria)
    tokenizer = None
    model = None
    torch.cuda.empty_cache()

    bnb_config = None
    if use_4bit:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16
        )

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        quantization_config=bnb_config
    )
    model.eval()

    _current_model_name = model_name
    print("[INFO] Modeloa kargatuta.")
    return tokenizer, model


# =========================================================
# === INFERENTZIA
# =========================================================

def inferentzia(user_prompt: str, model_name: str, max_new_tokens: int = 10, use_4bit: bool = True) -> str:
    """
    Inferentzia egiteko funtzioa.
    System prompt-a eta chat template-a erabiltzen ditu.
    """
    load_model(model_name, use_4bit=use_4bit)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    if hasattr(tokenizer, "apply_chat_template"):
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    else:
        prompt = SYSTEM_PROMPT + "\n" + user_prompt

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[-1]:],
        skip_special_tokens=True
    ).strip().lower()

    # print(f"[DEBUG] Decoded: {decoded}")
    return decoded


# =========================================================
# === PARAGRAFO BAKOITZA AZTERTZEA
# =========================================================

def paragrafoa_aztertu(text: str, froga: int, prompt_dict, model_name: str, use_4bit: bool = True):
    """
    Testuari froga/prompt desberdinak aplikatzen dizkio eta etiketa (pos/neu/neg) esleitzen du.
    """
    prompts = prompt_dict[froga]
    emaitzak = []

    for idx, prompt_template in enumerate(prompts):
        prompt = prompt_template.format(paragrafoa=text)

        start_time = time.time()
        decoded = inferentzia(prompt, model_name=model_name, use_4bit=use_4bit)
        elapsed_time = time.time() - start_time

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
            label = "neu"

        emaitzak.append({
            "Froga": froga,
            "Prompt": idx + 1,
            "Erabilitako_prompta": prompt,
            "Modeloaren_emaitza": decoded[:500],
            "Label": label,
            "Exec_time": elapsed_time
        })

    return emaitzak


# =========================================================
# === METRIKEN KALKULUA
# =========================================================

def calculate_metrics(df_emaitzak: pd.DataFrame) -> pd.DataFrame:
    metrics = []

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


# =========================================================
# === CONFUSION MATRIX-AK
# =========================================================

def _plot_confusion_matrix(cm: np.ndarray, labels: list[str], title: str, out_png: str):
    fig, ax = plt.subplots()
    im = ax.imshow(cm)

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_title(title)

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
    labels: list[str] = None,
    save_csv: bool = True
):
    if labels is None:
        labels = ["pos", "neu", "neg"]

    os.makedirs(out_dir, exist_ok=True)

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
            pd.DataFrame(
                cm,
                index=[f"true_{l}" for l in labels],
                columns=[f"pred_{l}" for l in labels]
            ).to_csv(out_csv, encoding="utf-8")

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
            pd.DataFrame(
                cm,
                index=[f"true_{l}" for l in labels],
                columns=[f"pred_{l}" for l in labels]
            ).to_csv(out_csv, encoding="utf-8")


# =========================================================
# === PROZESU NAGUSIA
# =========================================================

def sentiment_analysis(
    input_csv: str,
    analysis_type: str,
    model_name: str,
    irteera_fitxategia: str,
    use_4bit: bool = True
):
    """
    Orain model_name + output name jasotzen ditu, modelo desberdinak iteratzeko.
    """
    partition = input_csv.replace(".csv", "")

    decoded_path = f"emaitzak_sentiment/{analysis_type}/{partition}/decoded/{irteera_fitxategia}"
    metrics_path = f"emaitzak_sentiment/{analysis_type}/{partition}/metrics/{irteera_fitxategia}"

    # ✅ confusions: direktorioa (ez fitxategia)
    confusion_dir = f"emaitzak_sentiment/{analysis_type}/{partition}/confusion_matrixes/{irteera_fitxategia.replace('.csv','')}/"

    try:
        df_input = pd.read_csv(input_csv, encoding="utf-8")
    except FileNotFoundError:
        print(f"[ERROR] ezin izan da sarrera fitxategia aurkitu: {input_csv}")
        return None

    if analysis_type == "zero-shot":
        prompt_dict = prompt_zero_shot_dict
    elif analysis_type == "few-shot-1":
        prompt_dict = prompt_few_shot_1_dict
    elif analysis_type == "few-shot-2":
        prompt_dict = prompt_few_shot_2_dict
    else:
        raise ValueError(f"Unknown analysis type: {analysis_type}")

    emaitza_guztiak = []

    for _, row in df_input.iterrows():
        text = row["Text"]
        language = str(row["Language"]).lower()

        if language == "eu":
            frogak = [1, 3, 4]
        elif language == "es":
            frogak = [2, 3, 4]
        else:
            print(f"[WARN] Hizkuntza ezezaguna {row.get('Text_id','???')} lerroan: {language}")
            continue

        for froga in frogak:
            emaitzak = paragrafoa_aztertu(text, froga, prompt_dict, model_name=model_name, use_4bit=use_4bit)

            for e in emaitzak:
                label_real = row["Label"]
                result = 1 if label_real == e["Label"] else 0

                emaitza_guztiak.append({
                    "Model": model_name,
                    "Text_id": row["Text_id"],
                    "Text": text,
                    "Language": language,
                    "Froga": e["Froga"],
                    "Prompt": e["Prompt"],
                    "Erabilitako_prompta": e["Erabilitako_prompta"],
                    "Modeloaren_emaitza": e["Modeloaren_emaitza"],
                    "Decoded_label": e["Label"],
                    "Label_real": label_real,
                    "Result": result,
                    "Exec_time": e["Exec_time"]
                })

    os.makedirs(os.path.dirname(decoded_path), exist_ok=True)
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)

    df_emaitzak = pd.DataFrame(emaitza_guztiak)
    df_emaitzak.to_csv(decoded_path, index=False, encoding="utf-8")
    print(f"[INFO] Emaitzak gordeta: {decoded_path}")

    df_metrics = calculate_metrics(df_emaitzak)
    df_metrics.to_csv(metrics_path, index=False, encoding="utf-8")
    print(f"[INFO] Metrikak gordeta: {metrics_path}")

    create_confusion_matrixes(df_emaitzak, confusion_dir, labels=["pos", "neu", "neg"], save_csv=True)
    print(f"[INFO] Confusion matrix-ak gordeta: {confusion_dir}")

    return df_emaitzak
