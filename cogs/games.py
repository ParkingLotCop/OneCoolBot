"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""



import discord
from discord.ext import commands

class games(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

def setup(client):
    client.add_cog(games(client))
