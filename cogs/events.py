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
from utils import log, colours
from db import db   
import os
from PIL import Image, ImageDraw, ImageFont, ImageFile, ImageFilter, ImagePath
import aiohttp
from typing import Optional
from io import BytesIO

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

            role = member.guild.get_role(869338493451632682)
            await member.add_roles(role)

            with Image.open("./data/img/welcome_cards/welcome.png", "r") as f:
                background = f.convert("RGB")

        except Exception as error:
            await log.member_add_db_error(self, member)
                
        finally:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(member.avatar_url)) as response:
                    image = await response.read()
                    icon = Image.open(BytesIO(image)).convert("RGBA").resize((200, 200))
                    bigsize = (icon.size[0] * 3, icon.size[1] * 3)
                    mask = Image.new("L", bigsize, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0) + bigsize, 255)

                    mask = mask.resize(icon.size, Image.ANTIALIAS)
                    icon.putalpha(mask)
                    background.paste(icon, (20, 20), mask=icon)
                    draw = ImageDraw.Draw(background, "RGB")
                    big_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 175, encoding="utf-8")
                    medium_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 40, encoding="utf-8")
                    small_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 30, encoding="utf-8")

                    text_size = draw.textsize(str(member.name), font=big_font)
                    offset_x = 1250 - 125 - text_size[0]
                    offset_y = 10
                    draw.text((offset_x, offset_y), str(member.name), font=big_font, fill=await colours.colour_hex(member, member))

                    text_size = draw.textsize(str("Joined the server!"), font=small_font)
                    offset_x = 365 - 25 - text_size[0]
                    offset_y = 650
                    draw.text((offset_x, offset_y), str("Joined the server!"), font=big_font, fill="#fff")

                    background.show()

                    background.save("./data/img/bkgrndswap.png")
                    ffile = discord.File("./data/img/bkgrndswap.png")
                    channel = self.client.get_channel(869062081327013929)
                    await channel.send(file=ffile)          
          
    #ON_MEMBER_LEAVE
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            await db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            await db.commit()
            await log.member_remove_db(self, member)

        except Exception as error:
            await log.member_remove_db_error(self, member)

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

    #VERIFICATION_AND_WHITELIST
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = 869339105534816267

        if payload.message_id == message_id:
            member = payload.member
            guild = member.guild
            emoji = payload.emoji.name

            await member.send("Success! You now have access to the whole server, welcome! One final step, please type in your minecraft ign to get whitelisted:")

            #remove @unverified role
            role = member.guild.get_role(869338493451632682)
            await member.remove_roles(role)

            #add @merchant role
            role = member.guild.get_role(869300375591743551)
            await member.add_roles(role)

def setup(client):
    client.add_cog(Events(client))