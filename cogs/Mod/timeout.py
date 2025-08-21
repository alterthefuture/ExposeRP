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
THIS COG HANDLES TIMINGOUT MEMBERS FROM THE SERVER.
YOU CAN FOLLOW THE SAME STRUCTURE FOR OTHER MODERATION COMMANDS IF NEEDED.

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

class TimeoutMember(commands.Cog):
    def __init__(self,client):
        self.client = client

    def parse_duration(duration_str): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        import re
        
        duration_str = duration_str.replace(" ", "").lower()
        
        match = re.match(r'^(\d+)([smhd])$', duration_str)
        if not match:
            return None
        
        amount, unit = match.groups()
        amount = int(amount)
        
        multipliers = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400
        }
        
        return amount * multipliers.get(unit, 0)

    def format_duration(seconds): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m"
        elif seconds < 86400:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes > 0:
                return f"{hours}h {minutes}m"
            return f"{hours}h"
        else:
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            if hours > 0:
                return f"{days}d {hours}h"
            return f"{days}d"
    
    @commands.command(
    name="timeout",
    description="Times out mentioned user for specified duration.",
    usage="timeout [@user] [duration] (reason)",
    )
    @commands.bot_has_guild_permissions(moderate_members=True)
    @commands.has_permissions(moderate_members=True)
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def timeout(self, ctx, member: discord.Member = None, duration: str = None, *, reason=None): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if member is None:
            return await ctx.send(embed=create_embed("❌ Please mention a user to timeout.\n`e!timeout [@user] [duration] (reason)`", 0xFF0000))
        
        if duration is None:
            return await ctx.send(embed=create_embed("❌ Please specify a duration.\n`e!timeout [@user] [1m/5m/1h/1d] (reason)`", 0xFF0000))
        
        try:
            time_seconds = self.parse_duration(duration)
            if time_seconds is None or time_seconds <= 0:
                return await ctx.send(embed=create_embed("❌ Invalid duration format. Use: `1m, 5m, 1h, 1d, etc.`", 0xFF0000))
            
            if time_seconds > 28 * 24 * 3600: 
                return await ctx.send(embed=create_embed("❌ Timeout duration cannot exceed 28 days.", 0xFF0000))
                
        except:
            return await ctx.send(embed=create_embed("❌ Invalid duration format. `Use: 1m, 5m, 1h, 1d, etc.`", 0xFF0000))
        
        if member.timed_out_until and member.timed_out_until > datetime.datetime.now(datetime.timezone.utc):
            return await ctx.send(embed=create_embed(f"❌ {member.mention} is already timed out until {member.timed_out_until.strftime('%Y-%m-%d %H:%M:%S UTC')}.", 0xFF0000))
        
        if ctx.author == member:
            return await ctx.send(embed=create_embed("❌ You can't timeout yourself.", 0xFF0000))
        
        if ctx.guild.owner == member:
            return await ctx.send(embed=create_embed("❌ You can't timeout the server owner.", 0xFF0000))
        
        if ctx.author.top_role.position <= member.top_role.position and ctx.author != ctx.guild.owner:
            return await ctx.send(embed=create_embed("❌ You can't timeout a user with a role higher or equal to yours.", 0xFF0000))
        
        if ctx.guild.me.top_role.position <= member.top_role.position:
            return await ctx.send(embed=create_embed("❌ I can't timeout a user with a role higher or equal to mine.", 0xFF0000))
        
        try:
            timeout_until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=time_seconds)
            
            await member.timeout(timeout_until, reason=f"Timed out by {ctx.author} for: {reason if reason else 'No reason provided.'}")
            
            embed = discord.Embed(title='⏰ Timed Out', color=0xFF0000, timestamp=datetime.datetime.now())
            embed.add_field(name="You have been timed out in", value=ctx.guild.name, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
            embed.add_field(name="Duration", value=self.format_duration(time_seconds), inline=False)
            embed.add_field(name="Until", value=timeout_until.strftime('%Y-%m-%d %H:%M:%S UTC'), inline=False)
            embed.add_field(name="Reason", value=reason if reason else "No reason provided.", inline=False)
            embed.set_footer(text="If you think this is a mistake, please contact the moderator.", icon_url=ctx.author.display_avatar.url)
            
            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                pass
            
            return await ctx.send(embed=create_embed(f"✅ {member.mention} has been successfully timed out for {self.format_duration(time_seconds)}."))
            
        except Exception as e:
            print(f"Error timing out member: {e}")
            return await ctx.send(embed=create_embed("❌ I do not have permission to timeout this user.", 0xFF0000))

    @timeout.error # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def timeoute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=create_embed(f"❌ You are missing the permission: **{error.missing_permissions}**", 0xFF0000))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=create_embed(f"❌ I am missing the permission: **{error.missing_permissions}**", 0xFF0000))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=create_embed("❌ User not found. Please mention a valid user.", 0xFF0000))
  
async def setup(client):
    await client.add_cog(TimeoutMember(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD