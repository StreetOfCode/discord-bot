from discord.ext import commands

from stats import show_stats


class PublicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="show-stats")
    async def show_stats(self, ctx, stat_id=None):
        """
        Anyone can run this command in the `BOT_COMMANDS_CHANNEL_ID`. Admins can run it anywhere.
        If run without the `stat_id` argument prints a description with available stats.
        If run with a valid `stat_id` argument then a graph visualizing the given stats is shown.
        """
        await show_stats.show_stats(ctx, stat_id)
