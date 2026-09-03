import pandas as pd


def add_driver_form_features(df):
    """
    Adds recent-form and season-standing features for each driver,
    using only information available BEFORE each race (no data leakage).
    """
    df = df.sort_values(["season", "round"]).reset_index(drop=True)

    # Average finishing position over the driver's last 3 races,
    # NOT including the current race (shift(1) moves values down by 1 row).
    df["last_3_avg_finish"] = (
        df.groupby("driverId")["position"]
        .transform(lambda x: x.shift(1).rolling(window=3, min_periods=1).mean())
    )

    # Total championship points the driver had BEFORE this race,
    # within the same season.
    df["season_points_before_race"] = (
        df.groupby(["season", "driverId"])["points"]
        .transform(lambda x: x.shift(1).cumsum())
    )
    df["season_points_before_race"] = df["season_points_before_race"].fillna(0)

    return df


if __name__ == "__main__":
    df = pd.read_csv("data/processed/race_results_clean.csv")
    df = add_driver_form_features(df)

    # Look at one driver across a season to sanity-check the logic
    check = df[(df["driverId"] == "max_verstappen") & (df["season"] == 2023)]
    print(check[["round", "position", "points", "last_3_avg_finish", "season_points_before_race"]].to_string(index=False))