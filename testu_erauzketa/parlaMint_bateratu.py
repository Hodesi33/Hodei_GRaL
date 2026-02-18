import os
from pathlib import Path

import pandas as pd



def merge_parlamint_folders(
    input_dir="ParlaMint",
    output_dir="ParlaMint-bateratua",
    skip_existing=True,
):
    """
    ParlaMint-eko fitxategiak bateratzen ditu (-meta.tsv, -meta-en.tsv eta .txt),
    dokumentu bakoitzeko TSV bakarrean, karpeten egitura mantenduz.

    Parametroak
    ----------
    input_dir : str edo Path
        Sarrerako karpeta nagusia.
    output_dir : str edo Path
        Irteerako karpeta nagusia.
    skip_existing : bool
        True bada, lehendik dauden TSVak ez dira berriro sortuko.
    """

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    def get_base_name(filename: Path) -> str | None:
        """
        Fitxategiaren oinarrizko izena itzultzen du, atzizki estandarrak kenduta:
        - -meta.tsv
        - -meta-en.tsv
        - .txt

        Return:
        - Oinarrizko izena (str), edo None formatua bateragarria ez bada.
        """
        name = filename.name
        if name.endswith("-meta-en.tsv"):
            return name.replace("-meta-en.tsv", "")
        elif name.endswith("-meta.tsv"):
            return name.replace("-meta.tsv", "")
        elif name.endswith(".txt"):
            return name.replace(".txt", "")
        return None



    # |----------------------------------------------------------------------------------------------------|
    # |------------------------------------ KARPETAK ZEHAKATU ETA TALDEKATU --------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # Azpikarpeta guztiak zeharkatu, egitura erlatiboa mantenduz
    for root, _, files in os.walk(input_dir):
        root_path = Path(root)

        # Sarrerako egitura mantentzeko bide erlatiboa
        relative_path = root_path.relative_to(input_dir)
        output_root = output_dir / relative_path
        output_root.mkdir(parents=True, exist_ok=True)

        # Fitxategiak izen oinarrien arabera taldekatu (dokumentu bereko osagaiak batera)
        groups: dict[str, list[Path]] = {}

        for f in files:
            base = get_base_name(Path(f))
            if base:
                groups.setdefault(base, []).append(root_path / f)



        # |------------------------------------------------------------------------------------------------|
        # |----------------------------------------- TALDEAK PROZESATU --------------------------------------|
        # |------------------------------------------------------------------------------------------------|

        for base, paths in groups.items():
            output_file = output_root / f"{base}.tsv"

            # Lehendik badago eta hala adierazi bada, ez da berriro sortzen
            if skip_existing and output_file.exists():
                continue

            df_meta = None
            df_meta_en = None
            df_text = None

            # Taldeko fitxategi bakoitza irakurri
            for path in paths:
                if path.name.endswith("-meta.tsv"):
                    df_meta = pd.read_csv(path, sep="\t", index_col=False, dtype=str)
                elif path.name.endswith("-meta-en.tsv"):
                    df_meta_en = pd.read_csv(path, sep="\t", index_col=False, dtype=str)
                elif path.name.endswith(".txt"):
                    df_text = pd.read_csv(
                        path,
                        sep="\t",
                        header=None,
                        names=["ID", "Text"]
                    )

            # Meta-fitxategirik gabe ezin da bateraketa egin
            if df_meta is None:
                continue

            # Testu-zutabea gehitu (ID bidez), baldin eta .txt badago
            if df_text is not None:
                df = df_meta.merge(df_text, on="ID", how="left")
            else:
                df = df_meta.copy()

            # Ingelesezko titulua gehitu (aukerakoa)
            if df_meta_en is not None:
                df_meta_en = df_meta_en[["ID", "Title"]].rename(
                    columns={"Title": "Title_en"}
                )
                df = df.merge(df_meta_en, on="ID", how="left")
            
            # Zutabeen ordena egokitu: Title eta Title_en ondoz ondokoak izan daitezen
            if "Title" in df.columns and "Title_en" in df.columns:
                cols = list(df.columns)
                cols.remove("Title_en")

                title_idx = cols.index("Title")
                cols.insert(title_idx + 1, "Title_en")
                df = df[cols]

            # Azken TSV fitxategia sortu
            df.to_csv(output_file, sep="\t", index=False)

            print(f"Sortuta: {output_file}")



def build_global_tsv(input_dir="ParlaMint-bateratua") -> pd.DataFrame:
    """
    Bateratutako ParlaMint-eko TSV guztiak irakurri, eta taula global bakarrean biltzen ditu.

    Prozesua:
    - TSV guztiak irakurri eta ordenatu.
    - Text_ID bakoitzari Speech_id bakarra esleitu.
    - Hitzaldi bakoitzean Text_id berriro 0tik hasi.
    - Generoa eta hizkuntza etiketak normalizatu.
    - Azken irteera-eskema bateratua itzuli.
    """

    input_dir = Path(input_dir)

    all_rows = []
    speech_id_map = {}   # Text_ID -> Speech_id
    next_speech_id = 0



    # |----------------------------------------------------------------------------------------------------|
    # |-------------------------------------- TSV GUZTIAK IRAKURRI -----------------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    for tsv_path in sorted(input_dir.rglob("*.tsv")):
        df = pd.read_csv(tsv_path, sep="\t", dtype=str)

        # Textuaren ordena egonkorra mantentzeko (Text_ID eta ID)
        df = df.sort_values(["Text_ID", "ID"])

        # Text_ID bakoitza hitzaldi gisa tratatu
        for text_id, group in df.groupby("Text_ID"):
            if text_id not in speech_id_map:
                speech_id_map[text_id] = next_speech_id
                next_speech_id += 1

            speech_id = speech_id_map[text_id]

            # Hitzaldiaren barruan Text_id 0tik berrabiarazi
            group = group.copy()
            group["Speech_id"] = speech_id
            group["Text_id"] = range(len(group))

            all_rows.append(group)

    df_all = pd.concat(all_rows, ignore_index=True)



    # |----------------------------------------------------------------------------------------------------|
    # |-------------------------------------- NORMALIZAZIOAK ETA IRTEERA -----------------------------------|
    # |----------------------------------------------------------------------------------------------------|

    # Generoa normalizatu (F/M -> E/G)
    gender_map = {
        "F": "E",
        "M": "G"
    }
    df_all["Gender"] = df_all["Speaker_gender"].map(gender_map)

    # Hizkuntza normalizatu (etiketa testualak -> eu/es/...)
    lang_map = {
        "Euskara": "eu",
        "Gaztelania": "es",
        "Multilingual": "multilingual"
    }
    df_all["Language"] = df_all["Lang"].map(lang_map)

    # Azken eskema bateratua eraiki
    df_final = pd.DataFrame({
        "Date": df_all["Date"],
        "Speech_id": df_all["Speech_id"],
        "Text_id": df_all["Text_id"],
        "Speaker": df_all["Speaker_ID"],
        "Birth": df_all["Speaker_birth"],
        "Gender": df_all["Gender"],
        "Party": df_all["Speaker_party_name"],
        "Language": df_all["Language"],
        "Text": df_all["Text"]
    })

    return df_final
