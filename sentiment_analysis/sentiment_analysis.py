import csv
import torch
import pandas as pd
import re
import time
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from huggingface_hub import login
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from prompts import *



# === MODELOA KONFIGURATZEA ===
# Modeloa aukeratu
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
IRTEERA_FITXATEGIA = "llama3.1-8B.csv"

#MODEL_NAME = "HiTZ/Latxa-Llama-3.1-8B-Instruct"
#IRTEERA_FITXATEGIA = "latxa3.1-8B.csv"

#MODEL_NAME = "BSC-LT/salamandra-7b-instruct"
#IRTEERA_FITXATEGIA = "salamandra-7B.csv"

#MODEL_NAME = "meta-llama/Llama-3.1-70B-Instruct" #HAU BUKAERAN!
#IRTEERA_FITXATEGIA = "llama3.1-70B.csv"

#MODEL_NAME = "HiTZ/Latxa-Llama-3.1-70B-Instruct" #HAU BUKAERAN!
#IRTEERA_FITXATEGIA = "latxa3.1-70B.csv"


# Modeloa kargatu
print("Modeloa kargatzen...")
try:
    # Kuantizazioa erabiltzeko
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto"
        , quantization_config=bnb_config # Ez bada nahi kuantizazioa erabili, lerro hau komentatu
        )
    print("Modeloa kargatuta.")
except Exception as e:
    print("Errorea modeloa kargatzean:", e)
    exit(1)



# === INFERENTZIAREN FUNTZIOA ===
def inferentzia(prompt: str, max_new_tokens=25) -> str: #max_new_tokens aldagaiarekin frogak egin
    """
    Inferentzia egiteko funtzioa.
    """

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokenizer.eos_token_id
    )
    #decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).strip().lower() #Emaitza eta prompt-a bidaltzeko
    decoded = tokenizer.decode(outputs[0][inputs['input_ids'].shape[-1]:], skip_special_tokens=True).strip().lower() #Bakarrik emaitza bueltatzeko
    print(f"[DEBUG] Decoded: {decoded}")
    return decoded



# === PARAGRAFO BAKOITZA AZTERTZEA ===
def paragrafoa_aztertu(text: str, froga: int, prompt_dict):
    """
    Textua aztertzeko funtzioa. Hemen etiketa esleitzen zaio.
    Baita, denbora kalkulatzen da jakiteko modeloak zenbat tardatzen duen.
    """

    prompts = prompt_dict[froga]
    emaitzak = []

    for idx, prompt_template in enumerate(prompts):
        prompt = prompt_template.format(paragrafoa=text) 

        start_time = time.time()
        decoded = inferentzia(prompt)
        elapsed_time = time.time() - start_time

        # Emaitza aztertu eta etiketa lortu
        match = re.search(r"\b(pos|neu|neg)\b", decoded)
        if match:
            label = match.group(1)
        else:
            label = "neu"

        emaitzak.append({
            "Froga": froga,
            "Prompt": idx + 1,
            "Label": label,
            "Exec_time": elapsed_time
        })

    return emaitzak



# === METRIKEN KALKULUA ===
def calculate_metrics(df_emaitzak):
    """
    Metrikak kalkulatzeko funtzioa.
    """

    metrics = []

    # (froga, prompt) bakoitzeko
    grouped = df_emaitzak.groupby(["Froga", "Prompt"])
    for (froga, prompt), group in grouped:
        y_true = group["Label_real"]
        y_pred = group["Decoded_label"]
        avg_exec_time = group["Exec_time"].mean()

        accuracy = accuracy_score(y_true, y_pred)
        precision_macro = precision_score(y_true, y_pred, average='macro', zero_division=0)
        recall_macro = recall_score(y_true, y_pred, average='macro', zero_division=0)
        f1_macro = f1_score(y_true, y_pred, average='macro', zero_division=0)

        precision_weighted = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall_weighted = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1_weighted = f1_score(y_true, y_pred, average='weighted', zero_division=0)

        metrics.append({
            "Froga": froga,
            "Prompt": prompt,
            "Accuracy": accuracy,
            "Precision_macro": precision_macro,
            "Recall_macro": recall_macro,
            "F1_macro": f1_macro,
            "Precision_weighted": precision_weighted,
            "Recall_weighted": recall_weighted,
            "F1_weighted": f1_weighted,
            "Avg_exec_time": avg_exec_time
        })

    # Froga bakoitzeko emaitza globalak
    grouped_froga = df_emaitzak.groupby("Froga")
    for froga, group in grouped_froga:
        y_true = group["Label_real"]
        y_pred = group["Decoded_label"]
        avg_exec_time = group["Exec_time"].mean()

        accuracy = accuracy_score(y_true, y_pred)
        precision_macro = precision_score(y_true, y_pred, average='macro', zero_division=0)
        recall_macro = recall_score(y_true, y_pred, average='macro', zero_division=0)
        f1_macro = f1_score(y_true, y_pred, average='macro', zero_division=0)

        precision_weighted = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall_weighted = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1_weighted = f1_score(y_true, y_pred, average='weighted', zero_division=0)

        metrics.append({
            "Froga": froga,
            "Prompt": "GLOBAL",
            "Accuracy": accuracy,
            "Precision_macro": precision_macro,
            "Recall_macro": recall_macro,
            "F1_macro": f1_macro,
            "Precision_weighted": precision_weighted,
            "Recall_weighted": recall_weighted,
            "F1_weighted": f1_weighted,
            "Avg_exec_time": avg_exec_time
        })

    df_metrics = pd.DataFrame(metrics)
    df_metrics = df_metrics.sort_values(by=["Froga", "Prompt"])
    return df_metrics



# === PROZESU NAGUSIA ===
def sentiment_analysis(input_csv, analysis_type):
    """
    Sentiment analysis egiteko funtzio nagusia.
    Behin prozesua amaituta, emaitzak/metrikak (metrics) eta pozesuaren datu gehiago (denbora, ea zein etiketa bueltatu dituen, etab.) (decoded) bi csv-tan gordeko dira.
    """

    # Rutak esleitu
    partition = input_csv.replace(".csv", "")
    irteera_fitxategia_decoded = f"emaitzak_sentiment/{analysis_type}/{partition}/decoded/{IRTEERA_FITXATEGIA}"
    irteera_fitxategia_metrics = f"emaitzak_sentiment/{analysis_type}/{partition}/metrics/{IRTEERA_FITXATEGIA}"
    emaitza_guztiak = []

    # Aztertzeko testuak jasotzeko
    try:
        df_input = pd.read_csv(input_csv, encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: ezin izan da sarrera fitxategia aurkitu: {input_csv}")
        return None

    # Prompt egokiak ezartzeko. Prompt hauek guztiak prompts.py fitxategian aurkitu daitezke.
    if analysis_type == "zero-shot":
        prompt_dict = prompt_zero_shot_dict
    elif analysis_type == "few-shot-1":
        prompt_dict = prompt_few_shot_1_dict
    elif analysis_type == "few-shot-2":
        prompt_dict = prompt_few_shot_2_dict
    else:
        raise ValueError(f"Unknown analysis type: {analysis_type}")
    
    # Testuen analisia
    for _, row in df_input.iterrows():
        text = row["Text"]
        language = row["Language"].lower()

        if language == "eu":
            frogak = [1, 3, 4]
        elif language == "es":
            frogak = [2, 3, 4]
        else:
            print(f"Hizkuntza ezezaguna {row['Text_id']} lerroan: {language}")
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
                    "Decoded_label": e["Label"],
                    "Label_real": label_real,
                    "Result": result,
                    "Exec_time": e["Exec_time"]
                })

    # Karpetak sortu
    os.makedirs(os.path.dirname(irteera_fitxategia_decoded), exist_ok=True)
    os.makedirs(os.path.dirname(irteera_fitxategia_metrics), exist_ok=True)

    # Decoded emaitzak DataFrame batean jaso eta csv batean gorde
    df_emaitzak = pd.DataFrame(emaitza_guztiak)
    df_emaitzak.to_csv(irteera_fitxategia_decoded, index=False, encoding='utf-8')
    print(f"[INFO] Emaitzak gordeta: {irteera_fitxategia_decoded}")

    # Metrics emaitzak lortu eta csv batean gorde
    df_metrics = calculate_metrics(df_emaitzak)
    df_metrics.to_csv(irteera_fitxategia_metrics, index=False, encoding='utf-8')
    print(f"[INFO] Metrikak gordeta: {irteera_fitxategia_metrics}")

    return df_emaitzak
