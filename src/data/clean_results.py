import pandas as pd


def load_raw_results(path="data/raw/race_results_2018_2024.csv"):
    df = pd.read_csv(path)
    return df


if __name__ == "__main__":
    df = load_raw_results()

    print("Shape:", df.shape)
    print()
    print("Columns:")
    print(df.columns.tolist())
    print()
    print("Data types:")
    print(df.dtypes)
    print()
    print("Unique 'position' values:")
    print(df["position"].unique())
    print()
    print("Missing values per column:")
    print(df.isnull().sum()[df.isnull().sum() > 0])