import discord
import traceback
import sys
from discord.ext import commands
from termcolor import colored

class errorhandler(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("cog errorhandler online...", "green"))

def setup(client):
    client.add_cog(errorhandler(client))
