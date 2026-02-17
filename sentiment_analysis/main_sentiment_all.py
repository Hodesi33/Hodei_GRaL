from prepare_input import prepare_data
from sentiment_pipeline_all import sentiment_analysis

def main():
    input_csv = "data.csv"
    dev_csv = "dev.csv"
    test_csv = "test.csv"

    prepare_data(input_csv, dev_csv, test_csv)

    models = [
        ("meta-llama/Meta-Llama-3-8B-Instruct", "llama3.1-8B.csv"),
        ("HiTZ/Latxa-Llama-3.1-8B-Instruct", "latxa3.1-8B.csv"),
        ("BSC-LT/salamandra-7b-instruct", "salamandra-7B.csv"),
        ("meta-llama/Llama-3.1-70B-Instruct", "llama3.1-70B.csv"),
        ("HiTZ/Latxa-Llama-3.1-70B-Instruct", "latxa3.1-70B.csv"),
    ]

    analysis_types = ["zero-shot", "few-shot-1", "few-shot-2"]

    for model_name, out_file in models:
        for analysis_type in analysis_types:
            print("\n" + "="*80)
            print(f"[RUN] model={model_name} | exp={analysis_type} | split=dev")
            print("="*80)
            sentiment_analysis(dev_csv, analysis_type, model_name, out_file, use_4bit=True)

            print("\n" + "="*80)
            print(f"[RUN] model={model_name} | exp={analysis_type} | split=test")
            print("="*80)
            sentiment_analysis(test_csv, analysis_type, model_name, out_file, use_4bit=True)

if __name__ == "__main__":
    main()
