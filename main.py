import os
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from PIL import Image

from teams import TEAMS

pd.options.mode.chained_assignment = None

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


def annotate_axis(ax):
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
    return ax


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


def plot_single_unit(
    df=None,
    column_name="Gls",
    label="Goals",
    team_name=None,
    plot_color="cadetblue",
    fotmob_id="47",
    competition="pl",
):
    comp_description = "All Competitions"
    if competition == "pl":
        comp_description = "Premier League"

    if label == "Goals":
        descriptor = "Scored"
    if label == "Assists":
        descriptor = "Provided"
    if label == "Goals + Assists":
        descriptor = "Leaderboard"

    if team_name:
        file_name = f"{team_name.replace('-', '_').lower()}_{column_name.lower()}"
        title = f"{team_name.replace('-', ' ')} {label} {descriptor} {comp_description} 22/23"
    else:
        file_name = f"all_{column_name.lower()}"
        title = f"{label} {descriptor} {comp_description} 22/23"

    df = df[["Player", column_name]]
    df = df[~df[column_name].isna()]
    df[column_name] = df[column_name].astype(int)
    df = df[df[column_name] != 0]
    df = df.sort_values(column_name)

    if fotmob_id == 47:
        df = df.tail(30)

    fig = plt.figure(figsize=(8, 10), dpi=300, facecolor="#EFE9E6")
    ax = plt.subplot()
    ax.set_facecolor("#EFE9E6")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.set_title(
        title,
        fontweight="bold",
        fontsize=12,
    )
    ax.set_xlabel(f"{label} {descriptor}", fontweight="bold")
    ax.barh(df["Player"], df[column_name], align="center", color=plot_color)
    increment_value = df[column_name].iloc[0] * 0.02
    for index, value in enumerate(df[column_name]):
        plt.text(
            value + increment_value,
            index,
            str(value),
            color="#000000",
            va="center",
            fontweight="bold",
        )

    logo_ax = fig.add_axes([0.60, 0.2, 0.2, 0.2])
    ax_logo(fotmob_id, logo_ax)

    annotate_axis(ax)

    save_figure(
        f"figures/{competition}/{file_name}.png",
        300,
        False,
        "#EFE9E6",
        "tight",
    )

    plt.close()


def plot_stacked(
    df=None,
    column_name="Gls",
    label="Goals",
    team_name=None,
    fotmob_id="47",
    competition="pl",
):
    comp_description = "All Competitions"
    if competition == "pl":
        comp_description = "Premier League"

    if label == "Goals":
        descriptor = "Scored"
    if label == "Assist":
        descriptor = "Provided"
    if label == "Goals + Assists":
        descriptor = "Leaderboard"

    if team_name:
        file_name = f"{team_name.replace('-', '_').lower()}_{column_name.lower()}"
        title = f"{team_name.replace('-', ' ')} {label} {descriptor} {comp_description} 22/23"
    else:
        file_name = f"all_{column_name.lower()}"
        title = f"{label} {descriptor} {comp_description} 22/23"

    df = df[~df[column_name].isna()]
    df[column_name] = df[column_name].astype(int)
    df["Gls"] = df["Gls"].astype(int)
    df["Ast"] = df["Ast"].astype(int)
    df = df[df[column_name] != 0]
    df = df.sort_values(column_name)

    if fotmob_id == 47:
        df = df.tail(30)

    players = df.Player.values.tolist()
    goals = df.Gls.values.tolist()
    assists = df.Ast.values.tolist()

    fig = plt.figure(figsize=(8, 10), dpi=300, facecolor="#EFE9E6")
    ax = plt.subplot()
    ax.set_facecolor("#EFE9E6")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.set_title(
        title,
        fontweight="bold",
        fontsize=12,
    )
    ax.set_xlabel(f"{label} {descriptor}", fontweight="bold")
    ax.barh(players, goals, align="center", color="#C4961A", label="Goals")
    ax.barh(
        players, assists, align="center", left=goals, color="cadetblue", label="Assists"
    )

    increment_value = df[column_name].iloc[0] * 0.02
    for index, value in enumerate(df[column_name]):
        plt.text(
            value + increment_value,
            index,
            str(value),
            color="#000000",
            va="center",
            fontweight="bold",
        )

    for index, value in enumerate(goals):
        if value == 0:
            continue
        plt.text(
            value / 2,
            index,
            str(value),
            color="cadetblue",
            va="center",
            fontweight="bold",
        )

    for index, value in enumerate(assists):
        if value == 0:
            continue
        plt.text(
            goals[index] + (value / 2),
            index,
            str(value),
            color="#C4961A",
            va="center",
            fontweight="bold",
        )

    ax.legend(loc="lower right")

    logo_ax = fig.add_axes([0.60, 0.2, 0.2, 0.2])
    ax_logo(fotmob_id, logo_ax)

    annotate_axis(ax)

    save_figure(
        f"figures/{competition}/{file_name}.png",
        300,
        False,
        "#EFE9E6",
        "tight",
    )

    plt.close()


def main():
    pl_url = "https://fbref.com/en/squads/{fbref_id}/{team_name}-Stats"
    comps_url = "https://fbref.com/en/squads/{fbref_id}/2022-2023/all_comps/{team_name}-Stats-All-Competitions"

    pl_list = []
    comps_list = []

    if not os.path.isdir('figures/pl'):
        os.makedirs('figures/pl')

    if not os.path.isdir('figures/comps'):
        os.makedirs('figures/comps')

    for team_name in TEAMS:
        fbref_id = TEAMS[team_name]["fbref_id"]
        fotmob_id = TEAMS[team_name]["fotmob_id"]

        df_pl = get_info(pl_url.format(fbref_id=fbref_id, team_name=team_name))
        df_pl.drop(df_pl.tail(2).index, inplace=True)
        df_comps = get_info(comps_url.format(fbref_id=fbref_id, team_name=team_name))
        pl_list.append(df_pl)
        comps_list.append(df_comps)
        plot_single_unit(df_pl, "Gls", "Goals", team_name, "#C4961A", fotmob_id, "pl")
        plot_single_unit(
            df_pl, "Ast", "Assists", team_name, "cadetblue", fotmob_id, "pl"
        )
        plot_stacked(df_pl, "G+A", "Goals + Assists", team_name, fotmob_id, "pl")

        plot_single_unit(
            df_comps, "Gls", "Goals", team_name, "#C4961A", fotmob_id, "comps"
        )
        plot_single_unit(
            df_comps, "Ast", "Assists", team_name, "cadetblue", fotmob_id, "comps"
        )
        plot_stacked(
            df_comps,
            "G+A",
            "Goals + Assists",
            team_name,
            fotmob_id,
            "comps",
        )

    df_pl = pd.concat(pl_list, axis=0, ignore_index=True)
    df_comps = pd.concat(comps_list, axis=0, ignore_index=True)
    plot_single_unit(
        df=df_pl,
        column_name="Gls",
        label="Goals",
        plot_color="#C4961A",
        fotmob_id=47,
        competition="pl",
    )
    plot_single_unit(
        df=df_pl,
        column_name="Ast",
        label="Assists",
        plot_color="cadetblue",
        fotmob_id=47,
        competition="pl",
    )
    plot_stacked(
        df=df_pl,
        column_name="G+A",
        label="Goals + Assists",
        fotmob_id=47,
        competition="pl",
    )
    plot_single_unit(
        df=df_comps,
        column_name="Gls",
        label="Goals",
        plot_color="#C4961A",
        fotmob_id=47,
        competition="pl",
    )
    plot_single_unit(
        df=df_comps,
        column_name="Ast",
        label="Assists",
        plot_color="cadetblue",
        fotmob_id=47,
        competition="pl",
    )
    plot_stacked(
        df=df_comps,
        column_name="G+A",
        label="Goals + Assists",
        fotmob_id=47,
        competition="pl",
    )


if __name__ == "__main__":
    main()
