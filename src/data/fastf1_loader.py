import fastf1 
def load_race_session(year, grand_prix, session_type="R"):
    """
    Loads an F1 session via FastF1.

    year: season year, e.g. 2023
    grand_prix: name of the Grand Prix, e.g. "Bahrain"
    session_type: "R" = Race, "Q" = Qualifying, "FP1"/"FP2"/"FP3" = Practice
    """
    fastf1.Cache.enable_cache("data/cache")

    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()

    return session


if __name__ == "__main__":
    session = load_race_session(2023, "Bahrain", "R")

    print("Session loaded:", session.event["EventName"])
    print("Number of laps recorded:", len(session.laps)) # session.laps is a Pandas DataFrame with one row per lap, for every driver

    print(session.results[["Abbreviation", "TeamName", "Position"]].head(10)) # session.results is a DataFrame with the final session result