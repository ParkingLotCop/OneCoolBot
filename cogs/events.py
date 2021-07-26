"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
import asyncio
from discord import Member, Embed
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Cog
from discord import Embed, Emoji
from utils import log
from db import db   

#DevelopingThings GuildID
guild_id = (869061881250324531)
class Events(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)
    
    #ON_MEMBER_JOIN
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await db.execute("INSERT INTO users (UserID, GuildID) VALUES (?, ?)", member.id, member.guild.id)
            await db.commit()
            await log.member_add_db(self, member)

        except Exception as error:
            await log.member_add_db_error(self, member)
    
    #ON_MEMBER_LEAVE
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            await db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            await db.commit()
            await log.member_remove_db(self, member)

        except Exception as error:
            await log.member_remove_db_error(self, member)

    #ON_MEMBER_JOIN > ROLE_ADD
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == devthings_guild_id:
            
            role = member.guild.get_role(869300375591743551)
            await member.add_roles(role)

        else:
            return

    #KARMA_COUNTER
    @commands.Cog.listener()
    async def on_message(self, message):
         if not message.author.bot:
            context = await self.client.get_context(message)

            if context.command:
                return

            message = 1
            await db.execute(f"UPDATE users SET GlobalMessageCount = GlobalMessageCount + ? WHERE UserID = {context.author.id}",
                message
            )
            await db.commit()

def setup(client):
    client.add_cog(Events(client))