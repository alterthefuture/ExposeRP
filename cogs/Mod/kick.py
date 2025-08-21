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

"""
THIS COG HANDLES KICKING MEMBERS FROM THE SERVER.
YOU CAN FOLLOW THE SAME STRUCTURE FOR OTHER MODERATION COMMANDS IF NEEDED.

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

class KickMember(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(
            name="kick",
            description="kicks mentioned user from the server.",
            usage="kick [@user] (reason)",
    )
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user) 
    async def kick(self, ctx, member: discord.Member, *, reason=None): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if member is None:
            return await ctx.send(embed=create_embed("❌ Please mention a user to kick. `e!kick [@user] (reason)`", 0xFF0000))
        
        if ctx.author == member:
            return await ctx.send(embed=create_embed("❌ You can't kick yourself.", 0xFF0000))
        
        if ctx.guild.owner == member:
            return await ctx.send(embed=create_embed("❌ You can't kick the server owner.", 0xFF0000))
        
        if ctx.author.top_role.position <= member.top_role.position and ctx.author != ctx.guild.owner:
            return await ctx.send(embed=create_embed("❌ You can't kick a user with a role higher or equal to yours.", 0xFF0000))
        
        if ctx.guild.me.top_role.position <= member.top_role.position:
            return await ctx.send(embed=create_embed("❌ I can't kick a user with a role higher or equal to mine.", 0xFF0000))
        
        try:
            embed=discord.Embed(title='🔨 Kicked', color=0xFF0000,timestamp=datetime.datetime.now())
            embed.add_field(name="You have been kicked from", value=ctx.guild.name)
            embed.add_field(name="Moderator", value=ctx.author.mention)
            embed.add_field(name="Reason", value=reason if reason else "No reason provided.")
            embed.set_footer(text="If you think this is a mistake, please contact the administrator.", icon_url=ctx.author.display_avatar.url)

            if ctx.guild.icon:
                    embed.set_thumbnail(url=ctx.guild.icon.url)

            try:
                await member.send(embed=embed)
            except Exception as e:
                print(f"Error sending DM to {member.name}: {e}")

            try:
                await member.kick(reason=f"kicked by {ctx.author} for: {reason if reason else 'No reason provided.'}")
                await ctx.send(embed=create_embed(f"✅ {member.mention} has been successfully kicked."))
            except discord.Forbidden:
                return await ctx.send(embed=create_embed("❌ I do not have permission to kick this user. Check my role position and permissions", 0xFF0000))
            except discord.NotFound:
                return await ctx.send(embed=create_embed("❌ User not found. They may have left the server.", 0xFF0000))

        except Exception as e:
            print(f"Error kicking member: {e}")
            return await ctx.send(embed=create_embed("❌ I do not have permission to kick this user.", 0xFF0000))
        
    @kick.error # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def kick_error(self, ctx, error): 
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=create_embed(f"❌ You are missing the permission: **{error.missing_permissions}**", 0xFF0000))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=create_embed(f"❌ I am missing the permission: **{error.missing_permissions}**", 0xFF0000))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=create_embed("❌ User not found. Please mention a valid user.", 0xFF0000))
  
async def setup(client):
    await client.add_cog(KickMember(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD