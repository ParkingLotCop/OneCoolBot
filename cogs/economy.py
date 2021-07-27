"""
MIT License
Copyright (c) 2021 Timothy Pidashev
"""


import discord
from discord.ext import commands
from db import db
from utils import checks, colours, log
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed, Emoji

guild_ids = [869061881250324531]

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)

    @cog_ext.cog_slash(
        name="wallet",
        description="See how many emeralds you have!",
        guild_ids=guild_ids
    )
    async def wallet(self, context: SlashContext, user: discord.Member=None):
        await log.slash_command(self, context)

        user = user or context.author
        balance = (await db.record("SELECT Coins FROM users WHERE UserID = ?", user.id))[0]
        
        embed = discord.Embed(colour=await colours.colour(context))
        embed.set_author(name=f"{user.name}", icon_url=user.avatar_url)
        embed.add_field(
            name="Balance:",
            value=f"<:emerald:869368527734337606> {balance}",
            inline=True
        )

        await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="emerald-cap",
        description="See how many emeralds are widespread globally!",
        guild_ids=guild_ids
    )
    async def market_cap(self, context: SlashContext):
        cap = (await db.record("SELECT sum(Coins) FROM users"))[0]
        embed = discord.Embed(colour=await colours.colour(context))
        embed.add_field(name=f"**Current Market Cap:**", value=f"There are currently <:emerald:869368527734337606> **{cap}** emeralds widespread globally")
        await context.send(embed=embed)

def setup(client):
    client.add_cog(Economy(client))