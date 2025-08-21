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
import datetime
from pymongo import MongoClient

cluster = MongoClient("your-mongo-link-here") # REPLACE WITH YOUR MONGO LINK
db = cluster["Expose"]
collection = db["database"]

"""
THIS COG HANDLES MUTING MEMBERS IN THE SERVER.
YOU CAN FOLLOW THE SAME STRUCTURE FOR OTHER MODERATION COMMANDS IF NEEDED.

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

class MuteMember(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(
            name="mute",
            description="Mutes mentioned user.",
            usage="mute [@user] (reason)",
    )
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def mute(self, ctx, member: discord.Member, *, reason=None): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        muted = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted:
            return await ctx.send(embed=create_embed(f"❌  Muted role does not exist. Please run the `e!setup` command first.", 0xFF0000))
        
        if member is None:
            return await ctx.send(embed=create_embed("❌ Please mention a user to mute. `e!mute [@user] (reason)`", 0xFF0000))
        
        if muted in member.roles:
            muted_members = collection.find_one({"_id": ctx.guild.id})["muted_members"]
            if member.id in muted_members:
                return await ctx.send(embed=create_embed("Mentioned user is already muted."))
            else:
                collection.update_one({"_id": ctx.guild.id}, {"$push": {"muted_members": member.id}})
                return await ctx.send(embed=create_embed("Mentioned user is already muted."))
            
        if ctx.author == member:
            return await ctx.send(embed=create_embed("❌ You can't mute yourself.", 0xFF0000))
        
        if ctx.guild.owner == member:
            return await ctx.send(embed=create_embed("❌ You can't mute the server owner.", 0xFF0000))
        
        if ctx.author.top_role.position <= member.top_role.position and ctx.author != ctx.guild.owner:
            return await ctx.send(embed=create_embed("❌  can't mute a user with a role higher or equal to yours.", 0xFF0000))
        
        if ctx.guild.me.top_role.position <= member.top_role.position:
            return await ctx.send(embed=create_embed("❌ I can't mute a user with a role higher or equal to mine.", 0xFF0000))

        try:
            await member.add_roles(muted, reason=f"Muted by {ctx.author} for: {reason if reason else 'No reason provided.'}")
            collection.update_one({"_id": ctx.guild.id}, {"$push": {"muted_members": member.id}})

            embed=discord.Embed(title='🔨 Muted', color=0xFF0000,timestamp=datetime.datetime.now())
            embed.add_field(name="You have been muted in", value=ctx.guild.name)
            embed.add_field(name="Moderator", value=ctx.author.mention)
            embed.add_field(name="Reason", value=reason if reason else "No reason provided.")
            embed.set_footer(text="If you think this is a mistake, please contact the moderator.", icon_url=ctx.author.display_avatar.url)

            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon.url)

            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass

            return await ctx.send(embed=create_embed(f"✅ {member.mention} has been successfully muted."))
        except Exception as e:
            print(f"Error muting member: {e}")
            return await ctx.send(embed=create_embed("❌ I do not have permission to mute this user.", 0xFF0000))
    
    @mute.error # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=create_embed(f"❌ You are missing the permission: **{error.missing_permissions}**", 0xFF0000))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=create_embed(f"❌ I am missing the permission: **{error.missing_permissions}**", 0xFF0000))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=create_embed("❌ User not found. Please mention a valid user.", 0xFF0000))
  
async def setup(client):
    await client.add_cog(MuteMember(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD