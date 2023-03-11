import matplotlib.pyplot as plt

from utils import annotate_axis, ax_logo, save_figure


def plt_g_a(
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
        f"figures/{column_name.lower()}/{competition}/{file_name}.png",
        300,
        False,
        "#EFE9E6",
        "tight",
    )

    plt.close()


def plt_g_a_stacked(
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
        f"figures/{column_name.lower()}/{competition}/{file_name}.png",
        300,
        False,
        "#EFE9E6",
        "tight",
    )

    plt.close()
