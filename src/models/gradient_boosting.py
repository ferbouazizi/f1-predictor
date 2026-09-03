import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

from src.models.random_forest import load_model_ready_data, chronological_split, FEATURES, TARGET


if __name__ == "__main__":
    df = load_model_ready_data()

    train_seasons = [2018, 2019, 2020, 2021, 2022]
    test_seasons = [2023, 2024]
    train, test = chronological_split(df, train_seasons, test_seasons)

    X_train, y_train = train[FEATURES], train[TARGET]
    X_test, y_test = test[FEATURES], test[TARGET]

    model = GradientBoostingRegressor(n_estimators=200, max_depth=3, learning_rate=0.05, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print("Train rows:", len(train), "| Test rows:", len(test))
    print("Gradient Boosting MAE:", round(mae, 3))
    print("(Random Forest MAE was: 2.253, Baseline MAE was: 3.009)")

    importances = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)
    print()
    print("Feature importances:")
    print(importances)