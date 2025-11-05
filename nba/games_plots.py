import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def bar_plot_simple(df: pd.DataFrame) -> Figure:
    """
    Create and return a bar plot of team wins of top 15 teams
    Parameters
    df : pd.DataFrame
        DataFrame with columns 'team' and 'wins'.

    Returns
    Figure
        The matplotlib Figure object containing the plot.
    """
    df = df.iloc[0:20]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df["Team Name"], df["Win"])
    ax.set_title("Team Wins")
    ax.set_xlabel("Team")
    ax.set_ylabel("Number of Wins")
    plt.xticks(rotation=90)
    plt.tight_layout
    return fig


def home_away_plots(agg_df: pd.DataFrame) -> Figure:
    """
    Create and return a pie chart for the wins and losses of home/away teams
    Parameters
    df : pd.DataFrame
        DataFrame with columns 'team_type' and 'wins'.

    Returns
    Figure
        The matplotlib Figure object containing the plot.
    """
    agg_df = agg_df.drop("Loss", axis=1)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.pie(
        agg_df["Win"],
        labels=agg_df["Team Type"].astype(str).tolist(),
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.set_title("Percent of Wins for Home and Away Teams since 1946")
    ax.axis("equal")
    return fig
