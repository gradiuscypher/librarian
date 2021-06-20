import csv
import discord
import logging
import os
import time
from discord.ext import commands
from glob import glob

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
        current_files = glob('current*.csv')

        # the current_<TIME>.csv file exists
        if len(current_files) > 0:
            target_name = current_files[0]
            start_time = int(target_name.split('_')[1].split('.')[0])

            # verify whether the current file should be uploaded and rotated
            current_time = int(time.time())
            if current_time - start_time >= 10:
                start_new_csv(old_file=target_name)

            # if it isn't old enough, add on a new row entry
            else:
                with open(target_name, 'a') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter=',')
                    csv_writer.writerow(["4321", "USERNAME", "USER DISCRIM", "TEST GAME", str(current_time), "TEST END"])

        # the current file does not exist, create it.
        else:
            start_new_csv()

def setup(bot):
    bot.add_cog(Echo(bot))

def start_new_csv(old_file=None):
    current_time = int(time.time())
    # TODO: if an old_file name is provided, upload the old file and report to the user
    # TODO: this file removal is broken
    if old_file:
        print("OLD FILE IS OLD")
        full_path = os.path.join(os.getcwd(), old_file)
        print(full_path)
        os.remove(os.path.join(os.getcwd(), old_file))

    with open(f"current_{current_time}.csv", 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(["User ID", "User Name", "User Discriminator", "Game Name", "Game Start Time", "Game End Time"])
        csv_writer.writerow(["1234", "USERNAME", "USER DISCRIM", "TEST GAME", str(current_time), "TEST END"])