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

cluster = MongoClient("your-mongo-link-here") # REPLACE WITH YOUR MONGO LINK
db = cluster["Expose"]
collection = db["database"]

"""
THIS COG CHECKING SITS LOGGED THROUGH THE DISCORD BOTS.
ONLY CERTAIN ROLES CAN USE THIS COMMAND.

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

ALLOWED_ROLES = [  # CHANGE THE FOLLOWING ROLES TO YOUR SERVER'S ROLES (ONLY USERS WITH THESE ROLES CAN USE THE COMMAND)
    1391525588027834498, # [Management Team]
    1391525585301409852, # [Higher Management]
    1391525573012226149, # [Executive Team]
    1391525576719859806 # [Ownership Team]
]

class CheckCommands(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.group()
    async def check(self,ctx): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if ctx.invoked_subcommand is None:
            if not any(role.name in ALLOWED_ROLES or role.id in ALLOWED_ROLES for role in ctx.author.roles):
                return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))
            
            embed=discord.Embed(title="Check Commands", description="Use `e!log <command>` with the following args.",color=0x2596be,timestamp=datetime.datetime.now())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.add_field(name="Available Commands", value="`sit`, `all`", inline=False)
            embed.add_field(name="Usage", value="`check sit <id>`\n`check all <@user>`", inline=False)
            await ctx.send(embed=embed)

    @check.command(
        name='sit',
        description='Check a sit by its ID.',
        usage='check sit <id>'
    )
    async def sit(self, ctx, id: int): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if not any(role.name in ALLOWED_ROLES or role.id in ALLOWED_ROLES for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))

        data = collection.find_one({"_id": ctx.guild.id})
        if not data or "sits" not in data:
            return await ctx.send(embed=create_embed("❌ No sits found in this server.", 0xFF0000))
        
        sit = next((s for s in data["sits"] if s["id"] == id), None)

        if not sit:
            return await ctx.send(embed=create_embed(f"📭 No sit found with ID: `{id}`", 0xFF0000))
        
        logged_by_member = ctx.guild.get_member(sit['logged_by'])
        logged_by_name = logged_by_member.name if logged_by_member else f"Unknown User (ID: {sit['logged_by']})"
        logged_by_avatar = logged_by_member.avatar.url if logged_by_member and logged_by_member.avatar else None
        
        embed=discord.Embed(title=f"📁 Sit Details for ID: {sit['id']}", description=f"Sit ID: `{sit['id']}`\nConsequence: `{sit['consequence']}`\nTimestamp: `{sit['timestamp'].strftime('%Y-%m-%d %H:%M')}`\nLogged by: {logged_by_member.mention}\n\nProof: {sit['proof']}", color=0x2596be, timestamp=datetime.datetime.now())
        embed.set_footer(text=f"User ID: {sit['logged_by']}", icon_url=logged_by_avatar)
        embed.set_author(name=f"{logged_by_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        await ctx.send(embed=embed)

    @check.command(
        name="all",
        description="Check logged sits of a user.",
        usage="check all <@user>",
    )
    async def all(self, ctx, member:discord.Member=None): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        member = member or ctx.author
        if not any(role.name in ALLOWED_ROLES or role.id in ALLOWED_ROLES for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))

        data = collection.find_one({"_id": ctx.guild.id})
        if not data or "sits" not in data:
            return await ctx.send(embed=create_embed("❌ No sits found in this server.", 0xFF0000))
        
        user_sits = [s for s in data["sits"] if s["logged_by"] == member.id]

        if not user_sits:
            return await ctx.send(embed=create_embed(f"📭 No sits logged by {member.mention}", 0xFF0000))
        
        embed=discord.Embed(title=f"📁 Sits logged by {member.display_name}", color=0x2596be, timestamp=datetime.datetime.now())
        embed.set_author(name=str(member.name), icon_url=member.avatar.url if member.avatar else None)
        embed.set_footer(text=f"User ID: {member.id}", icon_url=member.avatar.url if member.avatar else None)
        for sit in user_sits:
            embed.add_field(
                name=f"✅ ID: `{sit['id']}` | Consequence: `{sit['consequence']}` | Timestamp: `{sit['timestamp'].strftime('%Y-%m-%d %H:%M')}`",
                value=f"Proof: {sit['proof']}", inline=False
            )

        await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(CheckCommands(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD