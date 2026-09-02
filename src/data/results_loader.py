from fastf1.ergast import Ergast
import pandas as pd
import time
import os


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


def get_multiple_seasons(start_year, end_year):
    """
    Fetches race results for a range of seasons (inclusive)
    and combines them into a single DataFrame.
    """
    all_seasons = []

    for year in range(start_year, end_year + 1):
        print(f"Fetching {year}...")
        season_df = get_season_results(year)
        all_seasons.append(season_df)
        time.sleep(1)

    full_df = pd.concat(all_seasons, ignore_index=True)
    return full_df


if __name__ == "__main__":
    df = get_multiple_seasons(2018, 2024)

    print("Total rows:", len(df))
    print("Seasons included:", sorted(df["season"].unique()))

    os.makedirs("data/raw", exist_ok=True)

    output_path = "data/raw/race_results_2018_2024.csv"
    df.to_csv(output_path, index=False)

    print("Saved to", output_path)