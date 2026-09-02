import os
import time

import pandas as pd
import requests
from fastf1.ergast import Ergast
from fastf1.exceptions import ErgastInvalidRequestError


def _fetch_page_with_retry(ergast, year, limit, offset, max_retries=6):
    """
    Fetches one page of season results. Retries with increasing wait
    times if the request fails due to rate limiting, a timeout, or a
    dropped connection — all common, expected issues with a public API.
    """
    wait_seconds = 5

    for attempt in range(max_retries):
        try:
            return ergast.get_race_results(season=year, limit=limit, offset=offset)

        except ErgastInvalidRequestError as e:
            is_rate_limit = "Too Many Requests" in str(e)
            is_last_attempt = attempt == max_retries - 1

            if is_rate_limit and not is_last_attempt:
                print(f"  Rate limited, waiting {wait_seconds}s and retrying...")
                time.sleep(wait_seconds)
                wait_seconds *= 2
            else:
                raise

        except requests.exceptions.RequestException as e:
            # Covers timeouts, connection resets, and other network-level
            # failures that aren't the API rejecting the request, just the
            # connection itself misbehaving.
            is_last_attempt = attempt == max_retries - 1

            if not is_last_attempt:
                print(f"  Network error ({type(e).__name__}), waiting {wait_seconds}s and retrying...")
                time.sleep(wait_seconds)
                wait_seconds *= 2
            else:
                raise


def get_season_results(year):
    """
    Fetches ALL race results for a season, handling pagination so we
    don't silently get a partial season back, and handling rate-limit
    or network errors by waiting and retrying.
    """
    ergast = Ergast()
    all_races = []
    offset = 0
    page_limit = 100
    total_expected = None
    max_pages = 20  # safety cap: no season should ever need this many pages

    for page_number in range(max_pages):
        response = _fetch_page_with_retry(ergast, year, page_limit, offset)

        if total_expected is None:
            total_expected = response.total_results
            print(f"  Season {year}: expecting {total_expected} total rows")

        for i, race_results in enumerate(response.content):
            race_results = race_results.copy()
            race_results["season"] = response.description.loc[i, "season"]
            race_results["round"] = response.description.loc[i, "round"]
            all_races.append(race_results)

        rows_so_far = sum(len(r) for r in all_races)

        if rows_so_far >= total_expected:
            break

        offset += page_limit
        time.sleep(2)  # pause between pages to avoid tripping the rate limit again
    else:
        print(f"  WARNING: hit the {max_pages}-page safety cap for {year} — data may be incomplete")

    season_df = pd.concat(all_races, ignore_index=True)
    return season_df


def get_multiple_seasons(start_year, end_year):
    """
    Fetches race results for a range of seasons (inclusive) and
    combines them into a single DataFrame.
    """
    all_seasons = []

    for year in range(start_year, end_year + 1):
        print(f"Fetching {year}...")
        season_df = get_season_results(year)
        all_seasons.append(season_df)
        time.sleep(3)  # pause between seasons too

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