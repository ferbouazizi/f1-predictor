import pandas as pd
import os

def load_raw_results(path="data/raw/race_results_2018_2024.csv"):
    df = pd.read_csv(path)
    return df

FINISHED_STATUSES = {"Finished", "Lapped"}


def clean_results(df):
    """
    Cleans the raw race results DataFrame:
    - adds a did_not_finish flag derived from the 'status' column
    - keeps only the columns we currently need
    """
    df = df.copy()

    # A driver is considered "finished" if status is Finished/Lapped,
    # or starts with "+" (e.g. "+1 Lap", "+2 Laps") - meaning they were
    # still running, just behind the leader. Everything else is a DNF.
    is_finished = df["status"].isin(FINISHED_STATUSES) | df["status"].str.startswith("+")
    df["did_not_finish"] = ~is_finished

    columns_to_keep = [
        "season", "round",
        "driverId", "driverCode", "givenName", "familyName",
        "constructorId", "constructorName",
        "grid", "position", "points", "laps",
        "status", "did_not_finish",
    ]
    df = df[columns_to_keep]

    return df

if __name__ == "__main__":
    raw_df = load_raw_results()
    clean_df = clean_results(raw_df)

    print("Cleaned shape:", clean_df.shape)
    print()
    print("did_not_finish counts:")
    print(clean_df["did_not_finish"].value_counts())
    print()
    print(clean_df.head())

    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/race_results_clean.csv"
    clean_df.to_csv(output_path, index=False)
    print()
    print("Saved to", output_path)