"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
from discord.ext import commands
from db import db
from utils import checks, colours, log, levels
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, wait_for_component
from discord_slash.utils import manage_components
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
import time
from datetime import datetime, timedelta
import asyncio
import psutil
import json
from PIL import Image, ImageDraw, ImageFont, ImageFile, ImageFilter, ImagePath
import aiohttp
from typing import Optional
from io import BytesIO

guild_ids = [869061881250324531]

#loading bot config
with open("config.json") as file:
    config = json.load(file)

#LEADERBOARD GENERATOR
class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        await log.online(self)

    #HELP 
    @cog_ext.cog_slash(
        name="help",
        description="A complete manual of help for the helpless!",
        guild_ids=guild_ids
    )
    async def help(self, context: SlashContext):
        await log.slash_command(self, context)
        page_1 = discord.Embed(
            title="Index",
            description="The home page of the help command!", 
            colour=await colours.colour(context)
        )
        fields = [("`General`", "**Basic commands for day-to-day tasks.", False),
                ("`Economy`", "Collect emeralds and set up shops integrated with minecraft!", False),
                ("`Music`", "Listen to low-latency music streams for studying and hanging out with friends in voice-chat!", False),
                ("`Moderation`", "Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", False)]

        page_1.set_footer(
            text="To scroll through pages, react to the arrows below."
        )

        for name, value, inline in fields:
            page_1.add_field(name=name, value=value, inline=inline)

        page_2 = discord.Embed(
            title="General", 
            description="The overview of the general commands.", 
            colour=await colours.colour(context)
        )
        fields = [("/`info`", "Displays bot status, ping, and other miscellaneous content.", False),
                  ("/`serverinfo`", "Displays server info, such as user count.", False),
                  ("/`userinfo`", "Displays user info, discord stats, and the like.", False),
                  ("/`minecraft-server-info`", "Displays minecrft server info, such as uptime and users playing.\nNot added yet! Working on it.", False),]

        page_2.set_footer(
            text=f"Handy tip! To see what a command can do, try it and see!"
        )

        for name, value, inline in fields:
            page_2.add_field(name=name, value=value, inline=inline)

        page_3 = discord.Embed(
            title="Economy", 
            description="Collect emeralds and set up shops integrated with minecraft!", 
            colour=await colours.colour(context)
        )
        fields = [("Under Construction!", "Economy is currently being polished and completely refactored.", False)]

        for name, value, inline in fields:
            page_3.add_field(name=name, value=value, inline=inline)

        page_4 = discord.Embed(
            title="Music",
            description="Listen to low-latency music streams for studying and hanging with friends in voice-chat!",
            colour=await colours.colour(context)
        )
        fields = [("Commands", "/`connect` connect bot to voice chat\n/`play` <search song to play>\n/`pause` pause player\n/`resume` resume player\n/`skip` skip current song\n/`stop`\n/`volume` change volume\n/`shuffle` shuffle queue\n/`equalizer` change equalizer\n/`queue` see songs queue\n/`current` see currently played song\n/`swap` swap song\n/`music` see music status\n/`spotify` see spotify rich presence", False)]

        for name, value, inline in fields:
            page_4.add_field(name=name, value=value, inline=inline)

        page_4.set_footer(
            text=f"Music is stable, but will be refactored to use new discord features and spotify integration, including playlists!"
        )

        page_5 = discord.Embed(
            title="Moderation", 
            description="Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", 
            colour=await colours.colour(context)
        )
        fields = [(f"`clear` <message_amount>", "Clear messages from a channel.", False),
                (f"`kick` <@member> <reason>", "Kick mentioned member from server.", False),
                (f"`ban` <@member> <reason>", "Ban mentioned member from server.", False),
                (f"`unban` <@member> <reason>", "Unbans mentioned member from server.", False)]

        for name, value, inline in fields:
            page_5.add_field(name=name, value=value, inline=inline)

        page_5.set_footer(
            text="Is being refactored, as is most of the bot lol. Will be complete and shiny with ai moderation soon!"
        )

        message = await context.send(embed=page_1)
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("❌")
        pages = 5
        current_page = 1

        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

        while True:
            try:
                reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and current_page != pages:
                    current_page += 1

                    if current_page == 2:
                        await message.edit(embed=page_2)
                        await message.remove_reaction(reaction, user)
                    
                    elif current_page == 3:
                        await message.edit(embed=page_3)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 4:
                        await message.edit(embed=page_4)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 5:
                        await message.edit(embed=page_5)
                        await message.remove_reaction(reaction, user)
                
                if str(reaction.emoji) == "◀️" and current_page > 1:
                    current_page -= 1
                    
                    if current_page == 1:
                        await message.edit(embed=page_1)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 2:
                        await message.edit(embed=page_2)
                        await message.remove_reaction(reaction, user)
                    
                    elif current_page == 3:
                        await message.edit(embed=page_3)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 4:
                        await message.edit(embed=page_4)
                        await message.remove_reaction(reaction, user)

                if str(reaction.emoji) == "❌":
                    await message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
                    
            except asyncio.TimeoutError:
                await message.delete()
                break

    #BOT-INFO
    @cog_ext.cog_slash(
        name="bot-info",
        description="See detailed information about me... wait may I ask why you need this info?",
        guild_ids=guild_ids
    )
    async def info(self, context):
        await log.cog_command(self, context)

        before = time.monotonic()
        before_ws = int(round(self.client.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        ram_usage = self.client.process.memory_full_info().rss / 1024**2
        current_time = time.time()
        difference = int(round(current_time - self.client.start_time))
        uptime = str(timedelta(seconds=difference))
        users = len(self.client.users)

        info = discord.Embed(
        title="Bot Info",
        description="Everything about me!",
        colour=0x9b59b6
        )
        info.set_thumbnail(
            url=context.bot.user.avatar_url
        )
        fields = [("Developer", "Timmy", True), 
                ("Users", f"{users}", True),
                ("Latency", f"{before_ws}ms", True),
                ("RAM Usage", f"{ram_usage:.2f} MB", True), 
                ("Uptime", uptime, True), 
                ("Version", self.client.version, True)]

        info.set_footer(
            text="Latest changes: Fix levelling."
        )

        for name, value, inline in fields:
            info.add_field(name=name, value=value, inline=inline)

        await context.send(embed=info)


    #USER-INFO
    @cog_ext.cog_slash(
        name="user-info",
        description="Gets user info and other handy information.",
        guild_ids=guild_ids
    )
    async def userinfo(self, context: SlashContext, user: discord.Member=None):
        await log.slash_command(self, context)

        if isinstance(context.channel, discord.DMChannel):
            return

        if user is None:
            user = context.author 

        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.set_author(
            name=str(user), 
            icon_url=user.avatar_url
        )
        
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        members = sorted(context.guild.members, key=lambda m: m.joined_at)
        date_format = "%a, %d %b %Y at %I:%M %p"

        top_role = user.top_role
        
        fields = [("Joined this server at", user.joined_at.strftime(date_format), True),
                  ("Registered this account at", user.created_at.strftime(date_format), False),
                  ("Server join position", str(members.index(user)+1), True),
                  ("Roles [{}]".format(len(user.roles)-1), top_role.mention, True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(
            text="ID: " + str(user.id)
        )
        await context.send(embed=embed)


    #SERVER-INFO
    @cog_ext.cog_slash(
        name="server-info",
        description="Gets server info and other handy information.",
        guild_ids=guild_ids
    )
    async def serverinfo(self, context: SlashContext):
        await log.slash_command(self, context)

        embed = discord.Embed(
        title="Server Info",
        colour=0x9b59b6
        )
        embed.set_thumbnail(
            url=context.guild.icon_url
        )

        fields = [("Owner", context.guild.owner, False),
                  ("Created At", context.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Region", context.guild.region, False),
                  ("Members", len(context.guild.members), False)]

        for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(
            text=f"ID: {context.guild.id}"
        )

        await context.send(embed=embed)

def setup(client):
    client.add_cog(Commands(client))
