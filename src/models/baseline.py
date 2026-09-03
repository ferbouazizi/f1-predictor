import pandas as pd


def evaluate_baseline(df):
    """
    Baseline model: predicted finishing position = grid position.
    Evaluated only on drivers who actually finished the race
    (excludes DNFs, since their 'position' doesn't reflect real
    finishing order - see Phase 4 EDA).
    """
    finished = df[df["did_not_finish"] == False].copy()

    finished["predicted_position"] = finished["grid"]
    finished["abs_error"] = (finished["predicted_position"] - finished["position"]).abs()

    mae = finished["abs_error"].mean()

    return mae, finished


if __name__ == "__main__":
    df = pd.read_csv("data/processed/training_dataset.csv")

    mae, finished = evaluate_baseline(df)

    print("Rows evaluated (finished races only):", len(finished))
    print("Baseline MAE (predicted = grid position):", round(mae, 3))