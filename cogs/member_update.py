"""
ref: https://discordpy.readthedocs.io/en/latest/api.html#discord.ActivityType
ref: https://discordpy.readthedocs.io/en/latest/api.html#discord.Member.activity
"""

import discord
import logging
from discord.ext import commands

# setup logging
logger = logging.getLogger("librarian")


class MemberUpdate(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.activity:
            if after.activity.type == discord.ActivityType.listening:
                print(after.activity.album)
            else:
                print(after.activity.type)

def setup(bot):
    bot.add_cog(MemberUpdate(bot))
