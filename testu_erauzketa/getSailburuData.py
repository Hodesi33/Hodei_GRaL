from pathlib import Path
from datasets import load_dataset
import pandas as pd


def update_speakers_data_files(
    parlamint_dir="ParlaMint-bateratua",
    basqueparl_name="HiTZ/basqueparl",
    birth_output="sailburu_birth.tsv",
    gender_output="sailburu_gender.tsv",
    party_output="sailburu_party.tsv"
):
    """
    Speaker bakoitzaren Birth, Gender eta Party datuak eguneratzen ditu.

    - Lehendik dauden fitxategiak badaude, oinarri gisa erabiltzen dira.
    - BasqueParl eta ParlaMint aztertzen dira.
    - Speaker berriak gehitzen dira.
    - Lehendik dagoen speaker baten daturen bat hutsik badago, osatzen saiatzen da.

    Sortzen diren fitxategiak:
    - sailburu_birth.tsv   -> Speaker, Birth
    - sailburu_gender.tsv  -> Speaker, Gender
    - sailburu_party.tsv   -> Speaker, Party
    """

    parlamint_dir = Path(parlamint_dir)
    birth_output = Path(birth_output)
    gender_output = Path(gender_output)
    party_output = Path(party_output)

    # ---------------- Garbiketa funtzioak ----------------
    def clean_text(series):
        return (
            series.astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    def clean_nullable(series):
        s = clean_text(series)
        return s.replace({
            "": pd.NA,
            "nan": pd.NA,
            "None": pd.NA,
            "<NA>": pd.NA,
            "-": pd.NA
        })

    def normalize_gender(series):
        s = clean_nullable(series).str.upper()

        # ParlaMint: F/M -> E/G
        s = s.replace({
            "F": "E",
            "M": "G"
        })

        return s

    def normalize_df(df):
        df = df.copy()

        df["Speaker"] = clean_nullable(df["Speaker"])
        df["Birth"] = clean_nullable(df["Birth"])
        df["Party"] = clean_nullable(df["Party"])
        df["Gender"] = normalize_gender(df["Gender"])

        # Speaker baliogabeak kendu
        df.loc[df["Speaker"].isin(["-"]), "Speaker"] = pd.NA

        # Konparaziorako gakoa sortu
        df["Speaker_key"] = (
            df["Speaker"]
            .astype("string")
            .str.lower()
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

        # Speaker gabeko lerroak kendu
        df = df.dropna(subset=["Speaker", "Speaker_key"])

        return df

    def choose_best_group(group):
        """
        Speaker berarentzako erregistro onena aukeratzen du:
        informazio gehien duen lerroa lehenetsiz.
        """
        group = group.copy()

        group["_completeness"] = (
            group["Birth"].notna().astype(int) +
            group["Party"].notna().astype(int) +
            group["Gender"].notna().astype(int)
        )

        best = (
            group.sort_values(
                ["_completeness", "Birth", "Party", "Gender"],
                ascending=[False, True, True, True],
                na_position="last"
            )
            .iloc[0]
            .copy()
        )

        return best.drop(labels=["_completeness"])

    def deduplicate_speakers(df):
        """
        Speaker bakoitzeko erregistro bakarra uzten du.
        """
        if df.empty:
            return df.copy()

        rows = []
        for _, group in df.groupby("Speaker_key", dropna=True):
            rows.append(choose_best_group(group))

        return pd.DataFrame(rows).reset_index(drop=True)

    def load_existing_file(path, value_col):
        """
        Lehendik dagoen fitxategi bat kargatzen du, badagoen kasuan.
        """
        if path.exists():
            df = pd.read_csv(path, sep="\t", dtype=str)

            required_cols = {"Speaker", value_col}
            if not required_cols.issubset(df.columns):
                raise ValueError(
                    f"{path} fitxategiak zutabe hauek izan behar ditu: Speaker, {value_col}"
                )

            df = df[["Speaker", value_col]].copy()
            print(f"Fitxategia kargatua: {path}")
        else:
            df = pd.DataFrame(columns=["Speaker", value_col])
            print(f"{path} ez da existitzen; berria sortuko da.")

        return df

    def merge_existing_columns(df_birth, df_gender, df_party):
        """
        Lehendik dauden hiru fitxategietako datuak Speaker arabera bateratzen ditu.
        """
        df_birth = df_birth.rename(columns={"Birth": "Birth"})
        df_gender = df_gender.rename(columns={"Gender": "Gender"})
        df_party = df_party.rename(columns={"Party": "Party"})

        df = df_birth.merge(df_gender, on="Speaker", how="outer")
        df = df.merge(df_party, on="Speaker", how="outer")

        return df

    def merge_prefer_base_and_fill(base_df, new_df):
        """
        Oinarriko datuak mantentzen ditu, baina hutsik dauden eremuak
        new_df-ko balioekin osatzen ditu speaker bera bada.
        """
        if base_df.empty:
            return deduplicate_speakers(new_df)

        base_df = base_df.copy()
        new_df = new_df.copy()

        new_map = (
            new_df[["Speaker_key", "Birth", "Party", "Gender"]]
            .drop_duplicates(subset=["Speaker_key"])
            .set_index("Speaker_key")
        )

        for idx, row in base_df.iterrows():
            key = row["Speaker_key"]
            if key in new_map.index:
                for col in ["Birth", "Party", "Gender"]:
                    if pd.isna(base_df.at[idx, col]) and pd.notna(new_map.at[key, col]):
                        base_df.at[idx, col] = new_map.at[key, col]

        existing_keys = set(base_df["Speaker_key"].dropna())
        only_new = new_df[~new_df["Speaker_key"].isin(existing_keys)].copy()

        merged = pd.concat([base_df, only_new], ignore_index=True)
        merged = deduplicate_speakers(merged)

        return merged

    # -------------------------------------------------
    # 1. Lehendik dauden fitxategiak kargatu
    # -------------------------------------------------
    df_birth_base = load_existing_file(birth_output, "Birth")
    df_gender_base = load_existing_file(gender_output, "Gender")
    df_party_base = load_existing_file(party_output, "Party")

    df_base = merge_existing_columns(df_birth_base, df_gender_base, df_party_base)

    # Falta diren zutabeak sortu
    for col in ["Birth", "Gender", "Party"]:
        if col not in df_base.columns:
            df_base[col] = pd.NA

    df_base = df_base[["Speaker", "Birth", "Party", "Gender"]]
    df_base = normalize_df(df_base)
    df_base = deduplicate_speakers(df_base)

    # -------------------------------------------------
    # 2. BasqueParl kargatu
    # -------------------------------------------------
    ds = load_dataset(basqueparl_name, split="train")
    df_bp = ds.to_pandas()[["speaker", "birth", "party", "gender"]].copy()
    df_bp = df_bp.rename(columns={
        "speaker": "Speaker",
        "birth": "Birth",
        "party": "Party",
        "gender": "Gender"
    })
    df_bp = normalize_df(df_bp)
    df_bp = deduplicate_speakers(df_bp)

    # -------------------------------------------------
    # 3. ParlaMint kargatu
    # -------------------------------------------------
    parlamint_frames = []

    for tsv_path in sorted(parlamint_dir.rglob("*.tsv")):
        df = pd.read_csv(tsv_path, sep="\t", dtype=str)

        if {"Speaker_name", "Speaker_birth", "Speaker_party", "Speaker_gender"}.issubset(df.columns):
            part = df[["Speaker_name", "Speaker_birth", "Speaker_party", "Speaker_gender"]].copy()
            part = part.rename(columns={
                "Speaker_name": "Speaker",
                "Speaker_birth": "Birth",
                "Speaker_party": "Party",
                "Speaker_gender": "Gender"
            })
            parlamint_frames.append(part)

    if parlamint_frames:
        df_pm = pd.concat(parlamint_frames, ignore_index=True)
    else:
        df_pm = pd.DataFrame(columns=["Speaker", "Birth", "Party", "Gender"])

    df_pm = normalize_df(df_pm)
    df_pm = deduplicate_speakers(df_pm)

    # -------------------------------------------------
    # 4. Oinarria eguneratu
    # -------------------------------------------------
    df_merged = merge_prefer_base_and_fill(df_base, df_bp)
    df_merged = merge_prefer_base_and_fill(df_merged, df_pm)

    # -------------------------------------------------
    # 5. Hiru irteera-fitxategiak sortu
    # -------------------------------------------------
    df_birth = (
        df_merged[["Speaker", "Birth"]]
        .dropna(subset=["Birth"])
        .sort_values("Speaker")
        .reset_index(drop=True)
    )

    df_gender = (
        df_merged[["Speaker", "Gender"]]
        .dropna(subset=["Gender"])
        .sort_values("Speaker")
        .reset_index(drop=True)
    )

    df_party = (
        df_merged[["Speaker", "Party"]]
        .dropna(subset=["Party"])
        .sort_values("Speaker")
        .reset_index(drop=True)
    )

    df_birth.to_csv(birth_output, sep="\t", index=False, encoding="utf-8")
    df_gender.to_csv(gender_output, sep="\t", index=False, encoding="utf-8")
    df_party.to_csv(party_output, sep="\t", index=False, encoding="utf-8")

    print(f"Fitxategia gordeta: {birth_output} | errenkadak: {len(df_birth)}")
    print(f"Fitxategia gordeta: {gender_output} | errenkadak: {len(df_gender)}")
    print(f"Fitxategia gordeta: {party_output} | errenkadak: {len(df_party)}")

    return df_birth, df_gender, df_party



if __name__ == "__main__":
    update_speakers_data_files()
