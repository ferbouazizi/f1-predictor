import pandas as pd


def add_constructor_features(df):
    """
    Adds constructor (team) championship standing before each race,
    using only information available before the race.
    """
    df = df.sort_values(["season", "round"]).reset_index(drop=True)

    # Step 1: collapse to one row per team per round (sum both drivers' points)
    round_totals = (
        df.groupby(["season", "constructorId", "round"])["points"]
        .sum()
        .reset_index()
        .sort_values(["season", "constructorId", "round"])
    )

    # Step 2: shift/cumsum on this round-level series (leakage-safe, per team)
    round_totals["constructor_points_before_race"] = (
        round_totals.groupby(["season", "constructorId"])["points"]
        .transform(lambda x: x.shift(1).cumsum())
    )
    round_totals["constructor_points_before_race"] = (
        round_totals["constructor_points_before_race"].fillna(0)
    )

    # Step 3: merge the team-level value back onto every driver's row
    df = df.merge(
        round_totals[["season", "constructorId", "round", "constructor_points_before_race"]],
        on=["season", "constructorId", "round"],
        how="left",
    )

    return df


if __name__ == "__main__":
    df = pd.read_csv("data/processed/race_results_clean.csv")
    df = add_constructor_features(df)

    check = df[(df["constructorId"] == "red_bull") & (df["season"] == 2023)]
    print(
        check[["round", "driverCode", "position", "points", "constructor_points_before_race"]]
        .to_string(index=False)
    )