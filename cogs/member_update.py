"""
ref: https://discordpy.readthedocs.io/en/latest/api.html#discord.ActivityType
ref: https://discordpy.readthedocs.io/en/latest/api.html#discord.Member.activity
"""

import csv
import discord
import logging
import os
import time
from discord.ext import commands
from glob import glob

# setup logging
logger = logging.getLogger("librarian")

class MemberUpdate(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # TODO: make this work
        if before is not None:
            print(before.name, before.id, before.discriminator)
            if before.activity is not None:
                print(before.activity.name, before.activity.start)
        if after is not None:
            print(after.name, after.id, after.discriminator)
            if after.activity is not None:
                print(after.activity.name, after.activity.start)

        if after is None and before:
            current_files = glob('current*.csv')

            # the current_<TIME>.csv file exists
            if len(current_files) > 0:
                target_name = current_files[0]
                start_time = int(target_name.split('_')[1].split('.')[0])

                # verify whether the current file should be uploaded and rotated
                current_time = int(time.time())
                if current_time - start_time >= 10:
                    start_new_csv(old_file=target_name, before_obj=before)

                # if it isn't old enough, add on a new row entry
                else:
                    with open(target_name, 'a') as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter=',')
                        csv_writer.writerow([before.id, before.name, before.discriminator, before.activity.game, before.start, time.time()])

            # the current file does not exist, create it.
            else:
                start_new_csv(before_obj=before)

def setup(bot):
    bot.add_cog(MemberUpdate(bot))


def start_new_csv(old_file=None, before_obj=None):
    current_time = int(time.time())
    # TODO: if an old_file name is provided, upload the old file and report to the user

    if old_file:
        os.remove(os.path.join(os.getcwd(), old_file))

    with open(f"current_{current_time}.csv", 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(["User ID", "User Name", "User Discriminator", "Game Name", "Game Start Time", "Game End Time"])
        csv_writer.writerow([before_obj.id, before_obj.name, before_obj.discriminator, before_obj.activity.game, before_obj.start, time.time()])