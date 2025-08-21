"""
CREATE A BOT INSTANCE FROM DISCORD DEV PAGE AND ENABLE INTENTS FOR THIS TO WORK. 
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

ALSO CREATE A MONGO DB AND REPLACE THE LINK BELOW WITH YOUR MONGO LINK.
MAKE SURE TO REPLACE THE TOKEN BELOW WITH YOUR BOT TOKEN.

I CBA TO WALK YOU THROUGH THE SETUP, JUST FOLLOW THE INSTRUCTIONS ON THE DISCORD DEVELOPER PORTAL AND MONGO DB.

THIS BOT IS FOR A FIVEM DISCORD SERVER. HAVE FUN SKIDDING

"""

from discord.ext import commands
from discord import Webhook
import discord
import datetime
from helper import *
from pymongo import MongoClient
import aiohttp

cluster = MongoClient("your-mongo-link-here") # REPLACE WITH YOUR MONGO LINK
db = cluster["Expose"]
collection = db["database"]

"""
THIS COG HANDLES LOGGING FOR MEMBER BANS, KICKS, AND UNBANS FROM THE FIVEM SERVER.
ONLY USERS WITH THE STAFF ROLE CAN USE THIS COMMAND.

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

STAFF_ROLE_ID = [1391525568620662916] # [Staff Team]  # REPLACE WITH YOUR STAFF ROLE ID (ONLY USERS WITH THIS ROLE CAN USE THE LOG COMMANDS)


class LogBans(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.group()
    async def log(self,ctx): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if ctx.invoked_subcommand is None:
            if not any(role.name in STAFF_ROLE_ID or role.id in STAFF_ROLE_ID for role in ctx.author.roles):
                return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))
            
            embed=discord.Embed(title="Log Commands", description="Use `e!log <command>` with the following args.",color=0x2596be,timestamp=datetime.datetime.now())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.add_field(name="Available Commands", value="`ban`, `kick`", inline=False)
            embed.add_field(name="Usage", value="`log ban <id> <reason> <proof>`\n`log kick <id> <reason> <proof>`", inline=False)
            await ctx.send(embed=embed)

    @log.command(
        name='ban',
        description="Log a ban from the server.",
        usage='log ban <id> <reason> <proof>'
    )
    async def ban(self,ctx, id: int, *args): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        consequence = None
        proof = None

        if not any(role.name in STAFF_ROLE_ID or role.id in STAFF_ROLE_ID for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))

        if len(args) == 1:
            return await ctx.send(embed=create_embed("❌ Please provide proof for the ban.", 0xFF0000))
        elif len(args) == 2:
            consequence = args[0]
            proof = " ".join(args[1:])
        else:
            return await ctx.send(embed=create_embed("❌ Please provide and ID, reason and proof.", 0xFF0000))

        try:

            embed2=discord.Embed(title="Ban logged", description=f"Ban ID: `{id}`\nReason: `{consequence}`\n\nProof: {proof}",timestamp=datetime.datetime.now(),color=0x2596be)
            embed2.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed2.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

            embed = discord.Embed(description=f"**✅ Ban Logged** **|** ID: **{id}** '**{consequence}**' '**{proof}**'",timestamp=datetime.datetime.now(),color=0x00FF00)
            embed.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url("https://discord.com/api/webhooks/1397467918853345280/AEFcLfaBMcfy6xw3PApY9a6iNssLfbUOH1Lso141L60WzUw7cd01La7C_CN0hF7zUXNa", session=session)
                await webhook.send(embed=embed2, avatar_url=self.client.user.avatar.url)

            return await ctx.send(embed=embed)

        except Exception as e:
            print(f"Error logging sit: {e}")

    @log.command(
        name='kick',
        description="Log a kick from the server.",
        usage='log kick <id> <reason> <proof>'
    )
    async def kick(self,ctx, id: int, *args): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        consequence = None
        proof = None

        if not any(role.name in STAFF_ROLE_ID or role.id in STAFF_ROLE_ID for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))

        if len(args) == 1:
            return await ctx.send(embed=create_embed("❌ Please provide proof for the kick.", 0xFF0000))
        elif len(args) == 2:
            consequence = args[0]
            proof = " ".join(args[1:])
        else:
            return await ctx.send(embed=create_embed("❌ Please provide and ID, reason and proof.", 0xFF0000))

        try:

            embed2=discord.Embed(title="Kick logged", description=f"Kick ID: `{id}`\nReason: `{consequence}`\n\nProof: {proof}",timestamp=datetime.datetime.now(),color=0x2596be)
            embed2.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed2.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

            embed = discord.Embed(description=f"**✅ Kick Logged** **|** ID: **{id}** '**{consequence}**' '**{proof}**'",timestamp=datetime.datetime.now(),color=0x00FF00)
            embed.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url("https://discord.com/api/webhooks/1397467918853345280/AEFcLfaBMcfy6xw3PApY9a6iNssLfbUOH1Lso141L60WzUw7cd01La7C_CN0hF7zUXNa", session=session)
                await webhook.send(embed=embed2, avatar_url=self.client.user.avatar.url)

            return await ctx.send(embed=embed)

        except Exception as e:
            print(f"Error logging sit: {e}")

async def setup(client):
    await client.add_cog(LogBans(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD