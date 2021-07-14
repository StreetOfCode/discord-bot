import datetime
import pathlib
import random

import discord
import matplotlib.pyplot as plt
import pyimgur

import db as db
from config import ADMIN_ROLE_ID, BOT_COMMANDS_CHANNEL_ID, IMGUR_CLIENT_ID
from stats.available_stats import get_stats_help_info, stats_options
from stats.stat_type import PERCENTAGE_BAR
from utils import has_role_with_id

DEFAULT_GRAPH_SIZE = (10, 10)

# color names from https://matplotlib.org/stable/gallery/color/named_colors.html
COLORS = ("blue", "orange", "green", "purple", "pink", "yellow", "cyan", "grey")

imgur = pyimgur.Imgur(IMGUR_CLIENT_ID)


async def show_stats(ctx, stat_id):
    if ctx.channel.id != BOT_COMMANDS_CHANNEL_ID and not has_role_with_id(
        ctx.author, ADMIN_ROLE_ID
    ):
        await ctx.channel.send("Nesprávny channel")
        return

    if not stat_id:
        await ctx.channel.send(get_stats_help_info())
        return

    if stat_id not in stats_options:
        await ctx.channel.send(f"Nevalidná možnosť - {stat_id}")
        return

    survey_question_id, stat_type, stat_title = stats_options[stat_id]

    if stat_type == PERCENTAGE_BAR:
        options, answers = get_options_and_their_counts(survey_question_id)

        graph_size = (
            # these graphs have verbose answer_options therefore graphs need to be wider
            (25, 10)
            if stat_id in ("7", "8", "9")
            else DEFAULT_GRAPH_SIZE
        )
        make_percentage_graph(
            stat_id, options, answers, stat_title, graph_size=graph_size
        )

        await send_graph_to_channel(ctx, stat_id, stat_title)


def get_options_and_their_counts(survey_question_id):
    """
    i.e will return tuple (['muz', 'zena'], [15, 12]) as in 15 users answered as muz and 12 as zena
    """
    answer_ids_with_text = db.get_answer_ids_with_text_from_question_id(
        survey_question_id
    )
    answer_ids = [answer_id for answer_id, _ in answer_ids_with_text]
    answer_ids_with_count = db.get_user_answers_count(survey_question_id, answer_ids)

    answer_ids_to_count = {key: 0 for key in answer_ids}
    for answer_id, count in answer_ids_with_count:
        if answer_id in answer_ids_to_count:
            answer_ids_to_count[answer_id] = count

    options = [text for _, text in answer_ids_with_text]
    answers = list(answer_ids_to_count.values())
    return options, answers


def create_answer_percentages(answers):
    total_answers = sum(answers)
    percentages = []
    for answer in answers:
        pct = (answer / total_answers) * 100
        percentages.append((round(pct, 2)))
    return percentages


def make_percentage_graph(stat_id, options, answers, title, graph_size=None):
    data = {"Option": options, "Answers": answers}
    data["Percentages"] = create_answer_percentages(data["Answers"])

    plt.style.use("dark_background")
    plt.figure(figsize=graph_size if graph_size else DEFAULT_GRAPH_SIZE)
    colors_list = random.sample(COLORS, len(options))
    graph = plt.bar(data["Option"], data["Answers"], color=colors_list)
    plt.ylabel("Počet odpovedí")
    plt.title(title)

    print_percentages_above_graph_bars(graph, data)

    plt.savefig(f"{stat_id}.png", transparent=True)


def print_percentages_above_graph_bars(graph, data):
    for i, p in enumerate(graph):
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        plt.text(
            x + width / 2,
            y + height * 1.01,
            f"{data['Percentages'][i]}% ({data['Answers'][i]})",
            ha="center",
            weight="bold",
        )
        i += 1


async def send_graph_to_channel(ctx, stat_id, stat_title):
    graph_embed = discord.Embed(title=stat_title, colour=discord.Colour(0xFFFF00))
    graph_embed.set_image(url=upload_graph_to_imgur(stat_id))
    await ctx.channel.send(embed=graph_embed)


def upload_graph_to_imgur(stat_id):
    uploaded_image = imgur.upload_image(f"{stat_id}.png")
    return uploaded_image.link
