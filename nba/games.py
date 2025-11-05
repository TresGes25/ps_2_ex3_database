import pandas as pd
from nba.simple_clean import simple_clean

# Data manipulation and visualisations for the games.csv.
query_game = """
    SELECT *
    FROM game
"""


def data_view() -> pd.DataFrame:
    """
    This is a simple function to view the data before making any manipulations
    """
    data = simple_clean(query_game)
    return data


def games_clean(data: pd.DataFrame) -> pd.DataFrame:
    """
    Parameters:
    data: pd.DataFrame
    This is the output from the data_view() function which
    connects to sql and read the data into a pandas dataframe

    Returns:
    pd.DataFrame
    Cleaned DataFrame
    """
    data["game_date"] = pd.to_datetime(data["game_date"])
    data["wl_home"] = data["wl_home"].map(
        {"W": "Home", "L": "Away"}
    )  # make the analysis easier by indicating who won the game
    data["pts_away"] = data["pts_away"].astype(int)  # change to integer
    data["pts_home"] = data["pts_home"].astype(int)  # change to integer
    data = data[
        data["season_type"] == "Regular Season"
    ]  # only interested in games played during the season
    cols_to_keep = [
        "game_date",
        "team_abbreviation_home",
        "team_name_home",
        "team_abbreviation_away",
        "team_name_away",
        "wl_home",
        "pts_home",
        "pts_away",
    ]
    data = data[cols_to_keep]
    data.columns = [
        "Game Date",
        "Home abbr.",
        "Home team name",
        "Away abbr.",
        "Away team name",
        "Winner",
        "Score - Home",
        "Score - Away",
    ]  # new column names
    return data


def team_stats(data: pd.DataFrame) -> pd.DataFrame:
    """
    Parameters:
    data: pd.DataFrame
    This is the output from the games_clean() function
    which contains a cleaned dataframe for games.csv

    Returns:
    pd.DataFrame
    A new DataFrame containing Win/loss count for each team,
    aggregated over time
    This function is used to create win/loss statistics for each team
    """
    records = []
    # iterating over each game
    for _, row in data.iterrows():
        home_team = row["Home team name"]
        away_team = row["Away team name"]
        winner = row["Winner"]

        if winner == "Home":
            records.append({"Team Name": home_team, "Win": 1, "Loss": 0})
            records.append({"Team Name": away_team, "Win": 0, "Loss": 1})

        elif winner == "Away":
            records.append({"Team Name": away_team, "Win": 1, "Loss": 0})
            records.append({"Team Name": home_team, "Win": 0, "Loss": 1})

    team_records = pd.DataFrame(records)
    team_values = team_records.groupby("Team Name", as_index=False).sum()
    team_values = team_values.sort_values(by="Win", ascending=False)

    return team_values


def home_away_count(data: pd.DataFrame) -> pd.DataFrame:
    home_records = []
    for _, row in data.iterrows():
        winner = row["Winner"]

        if winner == "Home":
            home_records.append({"Team Type": "Home", "Win": 1, "Loss": 0})
            home_records.append({"Team Type": "Away", "Win": 0, "Loss": 1})

        elif winner == "Away":
            home_records.append({"Team Type": "Away", "Win": 1, "Loss": 0})
            home_records.append({"Team Type": "Home", "Win": 0, "Loss": 1})

    home_away_count_df = pd.DataFrame(home_records)
    home_stats = home_away_count_df.groupby("Team Type", as_index=False).sum()

    return home_stats
