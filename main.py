import os
import pandas as pd

from plots_goals_assists import plt_g_a, plt_g_a_stacked
from plots_minutes import plt_minutes, plt_minutes_all
from teams import TEAMS

pd.options.mode.chained_assignment = None


def get_info(url):
    html = pd.read_html(url, header=0)
    df = html[0]
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    return df


def get_matches(df):
    df = df["Result"].tail(1)
    total_games = df.iloc[0].split("-")
    num_games = 0
    for value in total_games:
        num_games += int(value)

    return num_games


def get_goals_assists(df):
    df = df[["Player", "Gls", "Ast", "G+A"]]
    df.columns = ["Player", "Gls", "xG", "Ast", "xA", "G+A", "xG+xA"]
    df = df[["Player", "Gls", "Ast", "G+A"]]
    return df


def get_minutes(df):
    df = df[["Player", "Nation", "Pos", "Age", "Min", "MP", "Starts", "90s"]]
    df = df[~df["Min"].isna()]
    df = df[~df["Min"].isna()]
    df["Min"] = df["Min"].astype(float)
    df = df[df["Min"] >= 400].reset_index(drop=True)
    df = df.sort_values(by="Min").reset_index(drop=True)
    df = df[~df["Pos"].isna()]
    df["Nation"] = [x.split(" ")[1].lower() for x in df["Nation"]]
    df["Min"] = [int(x) for x in df["Min"]]
    return df


def get_minutes_all(df):
    df = df[["Player", "Nation", "Pos", "Age", "Min", "MP", "Starts", "90s", "club_id"]]
    df = df.sort_values(by="Min").reset_index(drop=True)
    df = df[~df["Pos"].isna()]
    df["Nation"] = [x.split(" ")[1].lower() for x in df["Nation"]]
    df["Min"] = [int(x) for x in df["Min"]]
    return df.tail(20)


def goals_and_assists(df_pl, df_comps, team_name, fotmob_id):
    pl_goal_list = []
    comps_goal_list = []

    df_pl = get_goals_assists(df_pl)
    df_pl.drop(df_pl.tail(2).index, inplace=True)
    df_comps = get_goals_assists(df_comps)

    pl_goal_list.append(df_pl)
    comps_goal_list.append(df_comps)

    plt_g_a(df_pl, "Gls", "Goals", team_name, "#C4961A", fotmob_id, "pl")
    plt_g_a(df_pl, "Ast", "Assists", team_name, "cadetblue", fotmob_id, "pl")
    plt_g_a_stacked(df_pl, "G+A", "Goals + Assists", team_name, fotmob_id, "pl")

    plt_g_a(df_comps, "Gls", "Goals", team_name, "#C4961A", fotmob_id, "comps")
    plt_g_a(df_comps, "Ast", "Assists", team_name, "cadetblue", fotmob_id, "comps")
    plt_g_a_stacked(
        df_comps,
        "G+A",
        "Goals + Assists",
        team_name,
        fotmob_id,
        "comps",
    )

    return pl_goal_list, comps_goal_list


def minutes(df_pl, df_comps, team_name, matches_pl, matches_comp, fotmob_id):
    pl_minutes_list = []
    comps_minutes_list = []

    df_pl = get_minutes(df_pl)
    df_comps = get_minutes(df_comps)

    plt_minutes(df_pl, team_name, matches_pl, fotmob_id, "pl")
    plt_minutes(df_comps, team_name, matches_comp, fotmob_id, "comps")

    df_pl["club_id"] = fotmob_id
    df_comps["club_id"] = fotmob_id
    pl_minutes_list.append(df_pl)
    comps_minutes_list.append(df_comps)

    return pl_minutes_list, comps_minutes_list


def main():
    pl_url = "https://fbref.com/en/squads/{fbref_id}/{team_name}-Stats"
    comps_url = "https://fbref.com/en/squads/{fbref_id}/2022-2023/all_comps/{team_name}-Stats-All-Competitions"
    pl_games_url = "https://fbref.com/en/squads/{fbref_id}/2022-2023/matchlogs/c9/misc/{team_name}-Match-Logs-Premier-League"
    comps_games_url = "https://fbref.com/en/squads/{fbref_id}/2022-2023/matchlogs/all_comps/misc/{team_name}-Match-Logs-All-Competitions"

    for competition in ["pl", "comps"]:
        for category in ["gls", "ast", "g+a", "minutes"]:
            if not os.path.isdir(f"figures/{category}/{competition}"):
                os.makedirs(f"figures/{category}/{competition}")

    for team_name in TEAMS:
        fbref_id = TEAMS[team_name]["fbref_id"]
        fotmob_id = TEAMS[team_name]["fotmob_id"]

        df_pl = get_info(pl_url.format(fbref_id=fbref_id, team_name=team_name))
        df_comps = get_info(comps_url.format(fbref_id=fbref_id, team_name=team_name))
        df_matches_pl = get_info(
            pl_games_url.format(fbref_id=fbref_id, team_name=team_name)
        )
        df_matches_comp = get_info(
            comps_games_url.format(fbref_id=fbref_id, team_name=team_name)
        )
        matches_pl = get_matches(df_matches_pl)
        matches_comp = get_matches(df_matches_comp)

        pl_goal_list, comps_goal_list = goals_and_assists(
            df_pl, df_comps, team_name, fotmob_id
        )

        pl_minutes_list, comps_minutes_list = minutes(
            df_pl, df_comps, team_name, matches_pl, matches_comp, fotmob_id
        )

    df_goals_pl = pd.concat(pl_goal_list, axis=0, ignore_index=True)
    df_goals_comps = pd.concat(comps_goal_list, axis=0, ignore_index=True)
    df_minutes_pl = pd.concat(pl_minutes_list, axis=0, ignore_index=True)
    df_minutes_comps = pd.concat(comps_minutes_list, axis=0, ignore_index=True)
    df_minutes_pl = get_minutes_all(df_minutes_pl)
    df_minutes_comps = get_minutes_all(df_minutes_comps)
    plt_g_a(
        df=df_goals_pl,
        column_name="Gls",
        label="Goals",
        plot_color="#C4961A",
        fotmob_id=47,
        competition="pl",
    )
    plt_g_a(
        df=df_goals_pl,
        column_name="Ast",
        label="Assists",
        plot_color="cadetblue",
        fotmob_id=47,
        competition="pl",
    )
    plt_g_a_stacked(
        df=df_goals_pl,
        column_name="G+A",
        label="Goals + Assists",
        fotmob_id=47,
        competition="pl",
    )
    plt_g_a(
        df=df_goals_comps,
        column_name="Gls",
        label="Goals",
        plot_color="#C4961A",
        fotmob_id=47,
        competition="comps",
    )
    plt_g_a(
        df=df_goals_comps,
        column_name="Ast",
        label="Assists",
        plot_color="cadetblue",
        fotmob_id=47,
        competition="comps",
    )
    plt_g_a_stacked(
        df=df_goals_comps,
        column_name="G+A",
        label="Goals + Assists",
        fotmob_id=47,
        competition="comps",
    )
    plt_minutes_all(df_minutes_pl, "pl")
    plt_minutes_all(df_minutes_comps, "comps")


if __name__ == "__main__":
    main()


# Fix issues with long names
# Issue with getting minutes for all teams
