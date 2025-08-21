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
from helper import *
from pymongo import MongoClient
import datetime

cluster = MongoClient("your-mongo-link-here") # REPLACE WITH YOUR MONGO LINK
db = cluster["Expose"]
collection = db["database"]

"""
THIS COG HANDLES INVITE TRACKING FOR MEMBERS JOINING THE SERVER.
BASICALLY A SHITTIER BASIC VERSION OF INVITE TRACKER.

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

class InviteChecker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.invite_cache = {}

    @commands.Cog.listener() # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def on_ready(self):
        for guild in self.client.guilds:
            try:
                invites = await guild.invites()
                self.invite_cache[guild.id] = {invite.code: invite.uses for invite in invites}
            except discord.Forbidden:
                self.invite_cache[guild.id] = {}

    @commands.Cog.listener() # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def on_member_join(self, member):
        guild = member.guild
        
        try:
            current_invites = await guild.invites()
            current_invite_dict = {invite.code: invite.uses for invite in current_invites}
            
            used_invite = None
            if guild.id in self.invite_cache:
                for code, uses in current_invite_dict.items():
                    if code in self.invite_cache[guild.id]:
                        if uses > self.invite_cache[guild.id][code]:
                            used_invite = discord.utils.get(current_invites, code=code)
                            break
                    else:
                        if uses > 0:
                            used_invite = discord.utils.get(current_invites, code=code)
                            break
            
            self.invite_cache[guild.id] = current_invite_dict
            
            if used_invite and used_invite.inviter:
                guild_data = collection.find_one({"_id": guild.id})
                if not guild_data:
                    collection.insert_one({
                        "_id": guild.id,
                        "sits": [],
                        "points": [],
                        "muted_members": [],
                        "invites": {}})
                elif "invites" not in guild_data:
                    collection.update_one(
                        {"_id": guild.id},
                        {"$set": {"invites": {}}})
                
                collection.update_one(
                    {"_id": guild.id},
                    {"$inc": {f"invites.{used_invite.inviter.id}": 1}},
                    upsert=True)
                
        except discord.Forbidden:
            pass

    @commands.Cog.listener() # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def on_invite_create(self, invite):
        if invite.guild.id not in self.invite_cache:
            self.invite_cache[invite.guild.id] = {}
        self.invite_cache[invite.guild.id][invite.code] = invite.uses

    @commands.Cog.listener() # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD 
    async def on_invite_delete(self, invite):
        if invite.guild.id in self.invite_cache:
            self.invite_cache[invite.guild.id].pop(invite.code, None)

    @commands.group() # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def invite(self, ctx):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="Invite Commands", description="Use `e!invite <command>` with the following args.",color=0x2596be,timestamp=datetime.datetime.now())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.add_field(name="Available Commands", value="`check`, `leaderboard`", inline=False)
            embed.add_field(name="Usage", value="`invite check <@user>`\n`invite leaderboard`", inline=False)
            await ctx.send(embed=embed)
        
    @invite.command(
        name='check',
        description='Check the invites of a user.',
        usage='invite check <@user>'
    )
    async def check(self, ctx, member: discord.Member = None): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if member is None:
            member = ctx.author
        
        guild_data = collection.find_one({"_id": ctx.guild.id})
        
        if not guild_data or "invites" not in guild_data:
            invite_count = 0
        else:
            invite_count = guild_data["invites"].get(str(member.id), 0)
        
        embed = discord.Embed(title="📊 Invite Statistics",description=f"{member.mention} has invited **{invite_count}** members to this server.",color=0x2596be,timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        
        await ctx.send(embed=embed)

    @invite.command(
        name='leaderboard',
        description='Show the invite leaderboard.',
        usage='invite leaderboard',
        aliases=['lb']
    )
    async def leaderboard(self, ctx): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        guild_data = collection.find_one({"_id": ctx.guild.id})
        
        if not guild_data or "invites" not in guild_data or not guild_data["invites"]:
            embed = discord.Embed(title="📊 Invite Leaderboard",description="No invite data available yet.",color=0x2596be,timestamp=datetime.datetime.now())
            return await ctx.send(embed=embed)
        
        invite_data = guild_data["invites"]
        sorted_invites = sorted(invite_data.items(), key=lambda x: x[1], reverse=True)
        
        embed = discord.Embed(title="📊 Invite Leaderboard",color=0x2596be,timestamp=datetime.datetime.now())
        
        description = ""
        for index, (user_id, count) in enumerate(sorted_invites[:10], 1):  # Top 10
            try:
                user = ctx.guild.get_member(int(user_id))
                if user:
                    if index == 1:
                        description += f"🥇 **{user.display_name}** - {count} invites\n"
                    elif index == 2:
                        description += f"🥈 **{user.display_name}** - {count} invites\n"
                    elif index == 3:
                        description += f"🥉 **{user.display_name}** - {count} invites\n"
                    else:
                        description += f"{index}. **{user.display_name}** - {count} invites\n"
            except:
                continue
        
        if not description:
            description = "No active inviters found."
        
        embed.description = description
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(InviteChecker(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD