import discord
import logging
from discord.ext import commands

# setup logging
logger = logging.getLogger("librarian")


class Echo(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, input):
        """
        Echoes the message
        """
        await ctx.send(input)
        logger.error("This is a test")
        logger.info(input)


def setup(bot):
    bot.add_cog(Echo(bot))
