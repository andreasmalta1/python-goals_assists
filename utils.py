import urllib.request
import matplotlib.pyplot as plt
from PIL import Image


def ax_logo(logo_id, ax):
    fotmob_url_club = "https://images.fotmob.com/image_resources/logo/teamlogo/"
    fotmob_url_league = "https://images.fotmob.com/image_resources/logo/leaguelogo/"

    if logo_id == 47:
        icon = Image.open(urllib.request.urlopen(f"{fotmob_url_league}{logo_id}.png"))
    else:
        icon = Image.open(urllib.request.urlopen(f"{fotmob_url_club}{logo_id}.png"))
    ax.imshow(icon)
    ax.axis("off")
    return ax


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


def save_figure(fig_name, dpi, transparency, face_color, bbox):
    plt.savefig(
        fig_name,
        dpi=dpi,
        transparent=transparency,
        facecolor=face_color,
        bbox_inches=bbox,
    )


def minutes_battery(ax, minutes, num_games):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    pct = minutes / (90 * num_games)
    ax.barh([0.5], [1], fc="#EFE9E6", ec="black", height=0.35)
    ax.barh([0.5], [pct], fc="#00529F", height=0.35)
    if pct > 0.3:
        ax.annotate(
            xy=(pct, 0.5),
            text=f"{pct:.0%}",
            xytext=(-8, 0),
            textcoords="offset points",
            weight="bold",
            color="#EFE9E6",
            va="center",
            ha="center",
            size=5,
        )
    else:
        ax.annotate(
            xy=(pct + 0.01, 0.5),
            text=f"{pct:.0%}",
            weight="bold",
            color="#00529F",
            va="center",
            ha="left",
            size=5,
        )
    ax.set_axis_off()
    return ax
