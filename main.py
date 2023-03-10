import pandas as pd
from teams import TEAMS
import matplotlib.pyplot as plt
from PIL import Image
import urllib.request

fotmob_url_club = "https://images.fotmob.com/image_resources/logo/teamlogo/"
fotmob_url_league = "https://images.fotmob.com/image_resources/logo/leaguelogo/"


def ax_logo(logo_id, ax):
    if logo_id == 47:
        icon = Image.open(urllib.request.urlopen(f"{fotmob_url_league}{logo_id}.png"))
    else:
        icon = Image.open(urllib.request.urlopen(f"{fotmob_url_club}{logo_id}.png"))
    ax.imshow(icon)
    ax.axis("off")
    return ax


def save_figure(fig_name, dpi, transparency, face_color, bbox):
    plt.savefig(
        fig_name,
        dpi=dpi,
        transparent=transparency,
        facecolor=face_color,
        bbox_inches=bbox,
    )


def get_info(url):
    html = pd.read_html(url, header=0)
    df = html[0]
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df = df[["Player", "Gls", "Ast", "G+A"]]
    df.columns = ["Player", "Gls", "xG", "Ast", "xA", "G+A", "xG+xA"]
    df = df[["Player", "Gls", "Ast", "G+A"]]
    return df


def plot_goals(df):
    df = df[["Player", "Gls"]]
    df = df[~df["Gls"].isna()]
    df["Gls"] = df["Gls"].astype(int)
    df = df[df["Gls"] != 0]
    df = df.sort_values("Gls")

    fig = plt.figure(figsize=(8, 10), dpi=300, facecolor="#EFE9E6")
    ax = plt.subplot()
    ax.set_facecolor("#EFE9E6")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.set_xlabel("Goals Scored", fontweight="bold")
    ax.barh(df["Player"], df["Gls"], align="center", color="#C4961A")
    for index, value in enumerate(df["Gls"]):
        plt.text(
            value + 0.2,
            index,
            str(value),
            color="#C4961A",
            va="center",
            fontweight="bold",
        )

    logo_ax = fig.add_axes([0.60, 0.2, 0.2, 0.2])
    ax_logo(10260, logo_ax)

    fig.text(
        x=0.1,
        y=0.87,
        s="Manchester United Goals Scored 2022/2023 Premier League",
        ha="left",
        va="bottom",
        weight="bold",
        size=12,
    )

    ax.annotate(
        "Stats from fbref.com",
        (0, 0),
        (0, -20),
        fontsize=8,
        xycoords="axes fraction",
        textcoords="offset points",
        va="top",
    )
    ax.annotate(
        "Data Viz by @plvizstats || u/plvizstats",
        (0, 0),
        (0, -30),
        fontsize=8,
        xycoords="axes fraction",
        textcoords="offset points",
        va="top",
    )

    save_figure(
        "test.png",
        300,
        False,
        "#EFE9E6",
        "tight",
    )


def main():
    pl_url = "https://fbref.com/en/squads/{fbref_id}/{team_name}-Stats"
    comps_url = "https://fbref.com/en/squads/{fbref_id}/2022-2023/all_comps/{team_name}-Stats-All-Competitions"

    pl_list = []
    comps_list = []

    for team_name in TEAMS:
        # fbref_id = TEAMS[team_name]["fbref_id"]
        # fotmob_id = TEAMS[team_name]["fotmob_id"]
        fbref_id = 19538871
        team_name = "Manchester-United"
        fotmob_id = 10260

        pl_url = pl_url.format(fbref_id=fbref_id, team_name=team_name)
        comps_url = comps_url.format(fbref_id=fbref_id, team_name=team_name)

        df_pl = get_info(pl_url)
        df_pl.drop(df_pl.tail(2).index, inplace=True)
        df_comps = get_info(comps_url)
        pl_list.append(df_pl)
        comps_list.append(df_comps)
        plot_goals(df_pl)
        #     num_games = get_matches(url_game)
        #     df_players["club_id"] = fotmob_id
        #     df_list.append(df_players)
        #     df_players = format_data(df_players)
        #     plot_data(df_players, team_name, num_games, fotmob_id)
        break

    # df_teams = pd.concat(df_list, axis=0, ignore_index=True)
    # df = format_data_all(df_teams)
    # plot_data_all(df)


if __name__ == "__main__":
    main()
