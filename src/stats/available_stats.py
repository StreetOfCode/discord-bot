from stats.stat_type import PERCENTAGE_BAR

# id of stat option to tuple(survey_question_id, stat_type, stat-stat_title)
stats_options = {
    "1": (1, PERCENTAGE_BAR, "Pohlavie - percentuálny podiel"),
    "2": (2, PERCENTAGE_BAR, "Vek - percentuálny podiel"),
    "3": (3, PERCENTAGE_BAR, "Skill v programovaní - percentuálny podiel"),
    "4": (4, PERCENTAGE_BAR, "Počúvanie podcastu - percentuálny podiel"),
    "5": (8, PERCENTAGE_BAR, "Vzťah k tikaniu - percentuálny podiel"),
    "6": (9, PERCENTAGE_BAR, "Vzťah k intro hudbe - percentuálny podiel"),
    "7": (
        10,
        PERCENTAGE_BAR,
        "Vzťah k dĺžke podcastových epizód - percentuálny podiel",
    ),
    "8": (
        11,
        PERCENTAGE_BAR,
        "Vzťah k štruktúre podcastových epizód - percentuálny podiel",
    ),
    "9": (
        12,
        PERCENTAGE_BAR,
        "Hodnotenie kvality audia v podcaste - percentuálny podiel",
    ),
}

stats_help = ""


def get_stats_help_info():
    # reuse global stats_help so options can be generated only once
    global stats_help
    if stats_help:
        return stats_help
    else:
        stats_help = "Zoznam dostupných štatistik je nižšie. Pre zobrazenie štatistiky spusti command /show-stats X, kde X je číslo štatistiky zo zoznamu nižšie. Napríklad /show-stats 3\n\n"
        for option, (_, _, title) in stats_options.items():
            stats_help += f"{option}. {title}\n"
        return stats_help
