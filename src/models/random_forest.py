import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

FEATURES = ["grid", "last_3_avg_finish", "season_points_before_race", "constructor_points_before_race"]
TARGET = "position"


def load_model_ready_data():
    df = pd.read_csv("data/processed/training_dataset.csv")
    df = df[df["did_not_finish"] == False].copy()
    df = df.dropna(subset=FEATURES)
    return df


def chronological_split(df, train_seasons, test_seasons):
    train = df[df["season"].isin(train_seasons)]
    test = df[df["season"].isin(test_seasons)]
    return train, test


if __name__ == "__main__":
    df = load_model_ready_data()

    train_seasons = [2018, 2019, 2020, 2021, 2022]
    test_seasons = [2023, 2024]
    train, test = chronological_split(df, train_seasons, test_seasons)

    X_train, y_train = train[FEATURES], train[TARGET]
    X_test, y_test = test[FEATURES], test[TARGET]

    model = RandomForestRegressor(n_estimators=200, max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print("Train rows:", len(train), "| Test rows:", len(test))
    print("Random Forest MAE:", round(mae, 3))
    importances = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)
    print()
    print("Feature importances:")
    print(importances)
    print("(Baseline MAE was: 3.009)")