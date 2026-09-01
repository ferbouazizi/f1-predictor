from fastf1.ergast import Ergast
import pandas as pd


def get_season_results(year):
    """
    Fetches full race results for every round of a given F1 season.

    year: season year, e.g. 2023

    Returns a single DataFrame where each row is one driver's
    result in one race, tagged with season and round number.
    """
    ergast = Ergast()
    response = ergast.get_race_results(season=year)

    all_races = []
    for i, race_results in enumerate(response.content):
        race_results = race_results.copy()
        race_results["season"] = response.description.loc[i, "season"]
        race_results["round"] = response.description.loc[i, "round"]
        all_races.append(race_results)

    season_df = pd.concat(all_races, ignore_index=True)
    return season_df


if __name__ == "__main__":
    df = get_season_results(2023)

    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print(df[["season", "round", "familyName", "position", "points"]].head(10))