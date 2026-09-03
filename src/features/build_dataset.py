import pandas as pd

from src.features.driver_features import add_driver_form_features
from src.features.constructor_features import add_constructor_features


def build_training_dataset():
    df = pd.read_csv("data/processed/race_results_clean.csv")

    df = add_driver_form_features(df)
    df = add_constructor_features(df)

    return df


if __name__ == "__main__":
    df = build_training_dataset()

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print()
    print("Missing values per column:")
    print(df.isnull().sum()[df.isnull().sum() > 0])

    output_path = "data/processed/training_dataset.csv"
    df.to_csv(output_path, index=False)
    print()
    print("Saved to", output_path)