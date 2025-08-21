"""
CREATE A BOT INSTANCE FROM DISCORD DEV PAGE AND ENABLE INTENTS FOR THIS TO WORK. 
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

ALSO CREATE A MONGO DB AND REPLACE THE LINK BELOW WITH YOUR MONGO LINK.
MAKE SURE TO REPLACE THE TOKEN BELOW WITH YOUR BOT TOKEN.

I CBA TO WALK YOU THROUGH THE SETUP, JUST FOLLOW THE INSTRUCTIONS ON THE DISCORD DEVELOPER PORTAL AND MONGO DB.

THIS BOT IS FOR A FIVEM DISCORD SERVER. HAVE FUN SKIDDING

"""

from discord.ext import commands
import discord
import datetime
from helper import *
from pymongo import MongoClient
from discord import Webhook
import aiohttp

cluster = MongoClient("your-mongo-link-here") # REPLACE WITH YOUR MONGO LINK
db = cluster["Expose"]
collection = db["database"]

"""
THIS COG HANDLES AUDIT LOGS FOR MEMBER BANS, KICKS, AND UNBANS. 
YOU CAN FOLLOW THE SAME STRUCTURE FOR OTHER AUDIT LOG EVENTS IF NEEDED.

JUST REPLACE WITH YOUR ACTUAL WEBHOOK LINK
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

class logs(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener() # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def on_member_ban(self, guild, member):
        entry = None
        async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            entry = log
            break

        if not entry:
            return
        logs = entry

        embed=discord.Embed(description=f"**Expose RP Logging** **|** {logs.user.mention} has banned **{member}**({member.mention})",timestamp=datetime.datetime.now(),color=0x2596be)
        embed.set_footer(text=f"ID: {logs.user.id}")
        embed.set_author(name=f"{logs.user}", icon_url=logs.user.display_avatar.url)

        get_data = collection.find_one({"_id": guild.id})
        if get_data["log_channel"] != "none":
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url("your-webhook-link", session=session)
                await webhook.send(embed=embed, avatar_url=self.client.user.avatar.url)
        else:
            pass
    
    @commands.Cog.listener() # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def on_member_remove(self, member):
        guild = member.guild
        logs = None

        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id:
                time_diff = (datetime.datetime.now() - entry.created_at.replace(tzinfo=None)).total_seconds()
                if time_diff < 5:
                    logs = entry
                    break

        if not logs:
            return 

        embed = discord.Embed(description=f"**Expose RP Logging** **|** {logs.user.mention} has kicked **{member}** ({member.mention})",timestamp=datetime.datetime.now(),color=0x2596be)
        embed.set_footer(text=f"Executor ID: {logs.user.id}")
        embed.set_author(name=str(logs.user), icon_url=logs.user.display_avatar.url)

        get_data = collection.find_one({"_id": guild.id})
        if get_data and get_data["log_channel"] != "none":
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url("your-webhook-link", session=session)
                await webhook.send(embed=embed, avatar_url=self.client.user.avatar.url)
        else:
            pass

    @commands.Cog.listener() # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def on_member_unban(self, guild, member):
        entry = None
        async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            entry = log
            break

        if not entry:
            return
        logs = entry

        embed=discord.Embed(description=f"**Expose RP Logging** **|** {logs.user.mention} has unbanned **{member}**({member.mention})",timestamp=datetime.datetime.now(),color=0x2596be)
        embed.set_footer(text=f"ID: {logs.user.id}")
        embed.set_author(name=f"{logs.user}", icon_url=logs.user.display_avatar.url)

        get_data = collection.find_one({"_id": guild.id})
        if get_data["log_channel"] != "none":
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url("your-webhook-link", session=session)
                await webhook.send(embed=embed, avatar_url=self.client.user.avatar.url)
        else:
            pass

async def setup(client): 
    await client.add_cog(logs(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD