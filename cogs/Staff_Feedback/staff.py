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
from discord import Webhook
import datetime
from helper import *
from pymongo import MongoClient
from collections import defaultdict
import aiohttp

cluster = MongoClient("your-mongo-link-here") # REPLACE WITH YOUR MONGO LINK
db = cluster["Expose"]
collection = db["database"]

"""
THIS COG HANDLES STAFF FEEDBACK, INCLUDING UPVOTES AND DOWNVOTES FOR STAFF MEMBERS ALSO PROMOTIONS DEMOTIONS AND ETC

YOU CAN CHANGE THE STYLE AS NEEDED. YOU ALSO HAVE TO CHANGE THE WEBHOOK LINKS AND CERTAIN CHANNEL IDS.
BASICALLY READ THE COMMAND AND CREATE A CORRESPONDING WEBHOOK AND CHANNEL FOR IT.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

STAFF_ROLE_ID = [1391525568620662916] # [Staff Team] # REPLACE WITH YOUR STAFF ROLE ID (ONLY USERS WITH THIS ROLE CAN USE THE COMMANDS)
CHANNEL_ID = [1394186706613178512] # [Commands] # REPLACE WITH YOUR COMMANDS CHANNEL ID (ONLY MESSAGES IN THIS CHANNEL CAN USE THE COMMANDS)
ALLOWED_ROLES = [ # CHANGE THE FOLLOWING ROLES TO YOUR SERVER'S ROLES (THESE ARE ALL STAFF ROLES IN ORDER OF HIERARCHY FOR PROMOTIONS AND DEMOTIONS)
    1391525588027834498, # [Management Team]
    1391525585301409852, # [Higher Management]
    1391525573012226149, # [Executive Team]
    1391525576719859806 # [Ownership Team]
]
MOD_TEAM = [
    1391525566729158686, # Trial Mod
    1391525565814673488, # Moderation Team
    1391525565093384192, # Senior Moderation
    1391525564065779884 # Moderation Team
]
ADMIN_TEAM = [
    1391525562262229022, # Trial Administrator
    1391525561397936129, # Administrator
    1391525560995414058, # Senior Administrator
    1391525560345432094, # Head Administrator
    1391525538505556028 # Lead Administrator
]
HIGHERUP_TEAM = [
    1391525537238880276, # Trial Head of Staff
    1391525536429379734, # Head of Staff
    1391525535955550268, # Trial Community Manager
    1391525535166758942, # Community Manager
    1391525534537748620 # Staff Manager
]
MANAGEMENT_TEAM = [
    1391525533090582548, # Trial Management
    1391525532520157356, # Management
    1391525531735822468, # Senior Management
    1391525531165655190 # Head Management
]
HIGHMANAGEMENT_TEAM = [
    1391525530062557307, # Lead Management
    1391525529894518928, # Server Management
    1391525528967577871 # Executive Management
]
EXECUTIVE_TEAM = [
    1391525527793307728, # Overseer
    1391525526912634941, # Executive
    1391525523003412593, # Operations
    1391525526233026621 # Head Operations
]
ALL_PERMS = [
    1391525589151912018, # [Administrator]
    1391525583489339392, # [Higher Ups]
    1391525588027834498, # [Management Team]
    1391525585301409852, # [Higher Management]
    1391525573012226149 # [Executive Team]
]
ROLE_HIERARCHY = (
    MOD_TEAM +
    ADMIN_TEAM +
    HIGHERUP_TEAM +
    MANAGEMENT_TEAM +
    HIGHMANAGEMENT_TEAM +
    EXECUTIVE_TEAM 
)

class StaffCommands(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.group()
    async def staff(self,ctx): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if ctx.invoked_subcommand is None:
            if not any(role.name in STAFF_ROLE_ID or role.id in STAFF_ROLE_ID for role in ctx.author.roles):
                embed=discord.Embed(title="Staff Commands", description="Use `!staff <command>` with the following args.", color=0x2596be, timestamp=datetime.datetime.now())
                embed.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                embed.add_field(name="Available Commands", value="`upvote`, `downvote`, `leaderboard`", inline=False)
                embed.add_field(name="Usage", value="`upvote <@user> <points 1-10> <reason>`\n `downvote <@user> <points 1-10> <reason>\n`leaderboard`", inline=False)
                return await ctx.send(embed=embed)
        
            if any(role.id in STAFF_ROLE_ID for role in ctx.author.roles):
                if not any(role.id in ALLOWED_ROLES for role in ctx.author.roles):
                    embed=discord.Embed(title="Staff Commands", description="Use `!staff <command>` with the following args.", color=0x2596be, timestamp=datetime.datetime.now())
                    embed.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                    embed.add_field(name="Available Commands", value="`upvote`, `downvote`, `leaderboard`, `check`", inline=False)
                    embed.add_field(name="Usage", value="`upvote <@user> <points 1-10> <reason>`\n `downvote <@user> <points 1-10> <reason>`\n`leaderboard`\n `check <@user>`", inline=False)
                    return await ctx.send(embed=embed)

            embed=discord.Embed(title="Staff Commands", description="Use `!staff <command>` with the following args.", color=0x2596be, timestamp=datetime.datetime.now())
            embed.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.add_field(name="Available Commands", value="`upvote`, `downvote`, `leaderboard`, `check`, `list`, `set`, `remove`, `promote`, `demote`", inline=False)
            embed.add_field(name="Usage", value="`upvote <@user> <points 1-10> <reason>`\n `downvote <@user> <points 1-10> <reason>`\n`leaderboard`\n `check <@user>`\n `list`\n`set <@user> <role>`\n`remove <@user>`\n`promote <@user> <1 or 2>`\n `demote <@user> <1 or 2>`", inline=False)
            await ctx.send(embed=embed)
            
    @staff.command(
        name="upvote",
        description="Upvote a staff member.",
        usage="staff upvote <@user> <points 1-10> <reason>",
    )   
    @commands.cooldown(1, 18000, commands.BucketType.user)
    async def upvote(self,ctx, member: discord.Member, points: int, *, reason: str): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if ctx.channel.id not in CHANNEL_ID:
            ctx.command.reset_cooldown(ctx)
            return

        if member.id == ctx.author.id:
            return await ctx.send(embed=create_embed("❌ You can't upvote yourself!", 0xFF000))
        
        if not any(role.id in STAFF_ROLE_ID for role in member.roles):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=create_embed("❌ You can only upvote staff members.", 0xFF0000))

        if points < 1 or points > 10:
            return await ctx.send(embed=create_embed("❌ Invalid points. Please enter a number between 1 and 10.", 0xFF0000))
        
        if reason is None or reason.strip() == "":
            return await ctx.send(embed=create_embed("❌ Please provide a reason for the upvote.", 0xFF0000))
        
        guild_id = ctx.guild.id
        user_id = member.id
        
        data = collection.find_one({"_id": guild_id})
        total_points = 0

        if data and "points" in data:
            total_points = sum(entry["points"] for entry in data["points"] if entry["id"] == user_id)

        new_total = total_points + points
        
        collection.update_one(
            {"_id": ctx.guild.id},
            {"$push":{
                "points": {
                    "id": member.id,
                    "reason": reason,
                    "points": points,
                    "given_by": ctx.author.id,
                    "timestamp": datetime.datetime.now(),
                } 
            }},
            upsert=True)
            
        await ctx.send(embed=create_embed(f"✅ You have upvoted {member.mention} with **{points}** points for: `{reason}`", 0x00FF00))

    @staff.command(
        name="downvote",
        description="Downvote a staff member.",
        usage="staff downvote <@user> <points 1-10> <reason>",
    )
    @commands.cooldown(1, 18000, commands.BucketType.user)
    async def downvote(self,ctx, member: discord.Member, points: int, *, reason: str): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if ctx.channel.id not in CHANNEL_ID:
            ctx.command.reset_cooldown(ctx)
            return
        
        if member.id == ctx.author.id:
            return await ctx.send(embed=create_embed("❌ You can't upvote yourself!", 0xFF000))
        
        if not any(role.id in STAFF_ROLE_ID for role in member.roles):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=create_embed("❌ You can only upvote staff members.", 0xFF0000))

        if points < 1 or points > 10:
            return await ctx.send(embed=create_embed("❌ Invalid points. Please enter a number between 1 and 10.", 0xFF0000))
        
        if reason is None or reason.strip() == "":
            return await ctx.send(embed=create_embed("❌ Please provide a reason for the upvote.", 0xFF0000))
        
        guild_id = ctx.guild.id
        user_id = member.id

        data = collection.find_one({"_id": guild_id})
        total_points = 0

        if data and "points" in data:
            total_points = sum(entry["points"] for entry in data["points"] if entry["id"] == user_id)

        new_total = total_points - points
        
        collection.update_one(
            {"_id": ctx.guild.id},
            {"$push":{
                "points": {
                    "id": member.id,
                    "reason": reason,
                    "points": -points,
                    "given_by": ctx.author.id,
                    "timestamp": datetime.datetime.now(),
                } 
            }},
            upsert=True)
            
        await ctx.send(embed=create_embed(f"✅ You have downvoted {member.mention} with **{points}** points for: `{reason}`", 0x00FF00))

    @staff.command(
        name='leaderboard',
        description='Displays the staff leaderboard.',
        usage='staff leaderboard',
    ) 
    async def leaderboard(self,ctx): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        data = collection.find_one({"_id": ctx.guild.id})

        if not data or "points" not in data or not data["points"]:
            return await ctx.send(embed=create_embed("❌ No points found in this server.", 0xFF0000))

        score_map = defaultdict(int)

        for entry in data["points"]:
            score_map[entry["id"]] += entry["points"]

        if not score_map:
            return await ctx.send(embed=create_embed("📭 No point data to display.", 0xFF0000))

        top_users = sorted(score_map.items(), key=lambda x: x[1], reverse=True)[:10]

        embed = discord.Embed(title="🏆 Staff Points Leaderboard",color=0x2596be,timestamp=datetime.datetime.now())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        for i, (user_id, total) in enumerate(top_users, start=1):
            member = ctx.guild.get_member(user_id)
            name = member.display_name if member else f"<@{user_id}>"
            embed.add_field(name=f"{i} - {name}",value=f"⭐ {total} points",inline=False)

        await ctx.send(embed=embed)

    @staff.command(
        name="check",
        description="Check points of a staff member.",
        usage="staff check <@user>",
    )
    async def check(self, ctx, member: discord.Member): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if not any(role.name in STAFF_ROLE_ID or role.id in STAFF_ROLE_ID for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))
        
        if member.id != ctx.author.id:
            if not any(role.id in ALLOWED_ROLES for role in member.roles):
                return await ctx.send(embed=create_embed("❌ You can only check your own points.", 0xFF0000))
            
        data = collection.find_one({"_id": ctx.guild.id})
        if not data or "points" not in data:
            return await ctx.send(embed=create_embed("❌ No points found in this server.", 0xFF0000))
        
        user_logs = [entry for entry in data["points"] if entry["id"] == member.id]
        if not user_logs:
            return await ctx.send(embed=create_embed(f"📭 {member.mention} has no point records.", 0xFF0000))

        total = sum(entry["points"] for entry in user_logs)
        latest_logs = sorted(user_logs, key=lambda x: x["timestamp"], reverse=True)[:5]

        embed = discord.Embed(title=f"📊 Point Log for {member.display_name} ({total} points)",color=0x2596be,timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.avatar.url if member.avatar else None)
        embed.set_footer(text=f"ID: {member.id}", icon_url=member.avatar.url if member.avatar else None)

        for log in latest_logs:
            giver = ctx.guild.get_member(log["given_by"])
            giver_tag = giver.mention if giver else f"<@{log['given_by']}>"
            embed.add_field(
                name=f"{'⬆️' if log['points'] > 0 else '⬇️'} `{log['points']}` pts | Timestamp: `{log['timestamp'].strftime('%Y-%m-%d %H:%M')}`",
                value=f"**Reason**: {log['reason']}\n**Given by**: {giver_tag}",
                inline=False
            )

        await ctx.send(embed=embed)

    @staff.command(
        name='list',
        description='List all staff members.',
        usage='staff list',
    )
    async def list(self, ctx): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if not any(role.name in ALLOWED_ROLES or role.id in ALLOWED_ROLES for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))
        
        staff_members = [member for member in ctx.guild.members if any(role.id in STAFF_ROLE_ID for role in member.roles)]

        if not staff_members:
            return await ctx.send(embed=create_embed("📭 No staff members found in this server.", 0xFF0000))
        
        embed = discord.Embed(title="👥 Staff Members", color=0x2596be, timestamp=datetime.datetime.now())
        embed.set_footer(text=f"Expose RP", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.description = ""

        for member in staff_members:
            embed.description += f"**{member.name}**({member.mention}) - {member.id}\n"

        await ctx.send(embed=embed)

    @staff.command(
        name="set",
        description="Set a new staff member's role.",
        usage="staff set <@user> <role_id>",
    )
    async def set(self, ctx, member: discord.Member, *, role_id: int): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD    
        staff_team = ctx.guild.get_role(1391525568620662916)  
        admin_perms = ctx.guild.get_role(1391525589151912018)  
        higherup_perms = ctx.guild.get_role(1391525583489339392)
        management_perms = ctx.guild.get_role(1391525588027834498)  
        higher_management_perms = ctx.guild.get_role(1391525585301409852) 
        executive_team_perms = ctx.guild.get_role(1391525573012226149)

        if not any(role.name in ALLOWED_ROLES or role.id in ALLOWED_ROLES for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))
        
        matched_role = ctx.guild.get_role(role_id)

        if not matched_role:
            return await ctx.send(embed=create_embed(f"❌ Role with ID `{role_id}` not found.", 0xFF0000))
        
        if ctx.author.top_role <= member.top_role:
            return await ctx.send(embed=create_embed("❌ You can't add a role to a member with a role higher or equal to yours.", 0xFF0000))
        
        if ctx.guild.me.top_role <= matched_role:
            return await ctx.send(embed=create_embed("❌ I can't add a role to a member with a role higher or equal to mine.", 0xFF0000))
        
        if staff_team in member.roles:
            return await ctx.send(embed=create_embed(f"{member.mention} is already staff. Use `promote/demote` instead." ,color=0x2596be))
        
        added_roles = []
        
        try:
            await member.add_roles(matched_role)
            added_roles.append(matched_role.name)
            await member.add_roles(staff_team)
            added_roles.append(staff_team.name)
            if matched_role.id in MOD_TEAM:
                await ctx.send(embed=create_embed(f"✅ {member.mention} has been given the `{matched_role.name}` role.", 0x00FF00))
            elif matched_role.id in ADMIN_TEAM:
                await member.add_roles(admin_perms)
                added_roles.append(admin_perms.name)
                await ctx.send(embed=create_embed(f"✅ {member.mention} has been given the `{matched_role.name}` role", 0x00FF00))
            elif matched_role.id in HIGHERUP_TEAM:
                await member.add_roles(higherup_perms)
                added_roles.append(higherup_perms.name)
                await ctx.send(embed=create_embed(f"✅ {member.mention} has been given the `{matched_role.name}` role", 0x00FF00))
            elif matched_role.id in MANAGEMENT_TEAM:
                await member.add_roles(management_perms)
                added_roles.append(management_perms.name)
                await ctx.send(embed=create_embed(f"✅ {member.mention} has been given the `{matched_role.name}` role", 0x00FF00))
            elif matched_role.id in HIGHMANAGEMENT_TEAM:
                await member.add_roles(higher_management_perms)
                added_roles.append(higher_management_perms.name)
                await ctx.send(embed=create_embed(f"✅ {member.mention} has been given the `{matched_role.name}` role", 0x00FF00))
            elif matched_role.id in EXECUTIVE_TEAM:
                await member.add_roles(executive_team_perms)
                added_roles.append(executive_team_perms.name)
                await ctx.send(embed=create_embed(f"✅ {member.mention} has been given the `{matched_role.name}` role", 0x00FF00))

            embed=discord.Embed(title=f"Congratulations on {matched_role.name}!",color=0x2596be,timestamp=datetime.datetime.now())
            embed.set_author(name='Expose RP', icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
            embed.set_footer(text=f"discord.gg/exposerp | Staff Promotions", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)

            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url("your-webhook-link", session=session)
                await webhook.send(f"{member.mention}", embed=embed, avatar_url=self.client.user.avatar.url)

            embed2=discord.Embed(title="Staff added", description=f"Member: {member.mention}`({member.id})`\nStaff roles given: `{", ".join(added_roles)}`\n\nGiven by: {ctx.author.mention}",timestamp=datetime.datetime.now(),color=0x2596be)
            embed2.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed2.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url("your-webhook-link", session=session)
                await webhook.send(embed=embed2, avatar_url=self.client.user.avatar.url)

        except Exception as e:
            print(f"Error setting role: {e}")

    @staff.command(
    name="remove",
    description="Remove staff roles from a user.",
    usage="staff remove <@user>",
    )
    async def remove(self, ctx, member: discord.Member): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        staff_team = ctx.guild.get_role(1391525568620662916) 

        if not any(role.id in ALLOWED_ROLES for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))

        if staff_team not in member.roles:
            return await ctx.send(embed=create_embed(f"{member.mention} is not currently on the staff team.",color=0x2596be))

        if ctx.author.top_role <= member.top_role:
            return await ctx.send(embed=create_embed("❌ You can't remove staff roles from someone with a higher or equal role.", 0xFF0000))

        all_staff_tiers = MOD_TEAM + ADMIN_TEAM + HIGHERUP_TEAM + MANAGEMENT_TEAM + HIGHMANAGEMENT_TEAM + EXECUTIVE_TEAM + ALL_PERMS + STAFF_ROLE_ID
        removed_roles = []

        try:
            for role_id in all_staff_tiers:
                role = ctx.guild.get_role(role_id)
                if role and role in member.roles:
                    await member.remove_roles(role)
                    removed_roles.append(role.name)

            main_removed_roles = [r for r in removed_roles if (discord.utils.get(ctx.guild.roles, name=r) and discord.utils.get(ctx.guild.roles, name=r).id not in ALL_PERMS)]
            main_display_role = main_removed_roles[0] if main_removed_roles else removed_roles[0]  

            await ctx.send(embed=create_embed(f"✅ {member.mention} has been removed from staff roles: `{main_display_role}`", 0x00FF00))

            embed = discord.Embed(title="Staff removed",description=f"Member: {member.mention} (`{member.id}`)\nStaff roles removed `{", ".join(removed_roles)}`\n\nRemoved by: {ctx.author.mention}",color=0xFF0000,timestamp=datetime.datetime.now())
            embed.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url("your-webhook-link", session=session)
                await webhook.send(embed=embed, avatar_url=self.client.user.avatar.url)

        except Exception as e:
            print(f"Error removing roles: {e}")

    @staff.command(
    name="promote",
    description="Promotes a staff member up to 2 roles higher.",
    usage="staff promote <@user> <1 or 2>",
    )
    async def promote(self, ctx, member: discord.Member, steps: int = 1): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if not any(role.id in ALLOWED_ROLES for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))

        if steps < 1 or steps > 2:
            return await ctx.send(embed=create_embed("❌ You can only promote by 1 or 2 tiers.", 0xFF0000))
        
        staff_team = ctx.guild.get_role(1391525568620662916)
        if staff_team not in member.roles:
            return await ctx.send(embed=create_embed("❌ Member is not currently staff.", 0xFF0000))

        current_index = None
        for i, role_id in enumerate(ROLE_HIERARCHY):
            if ctx.guild.get_role(role_id) in member.roles:
                current_index = i
                break

        if current_index is None:
            return await ctx.send(embed=create_embed("❌ Could not determine current role tier.", 0xFF0000))

        new_index = min(current_index + steps, len(ROLE_HIERARCHY) - 1)
        if current_index == new_index:
            return await ctx.send(embed=create_embed(f"⚠️ {member.mention} is already at the highest role.", 0x2596be))

        new_role = ctx.guild.get_role(ROLE_HIERARCHY[new_index])
        old_role = ctx.guild.get_role(ROLE_HIERARCHY[current_index])
        added_roles = []

        if not new_role:
            return await ctx.send(embed=create_embed("❌ New staff promotion role not found", 0xFF0000))


        await member.remove_roles(old_role)
        await member.add_roles(new_role)
        added_roles.append(new_role.name)

        if new_role.id in ADMIN_TEAM:
            perm = ctx.guild.get_role(1391525589151912018)
        elif new_role.id in HIGHERUP_TEAM:
            perm = ctx.guild.get_role(1391525583489339392)
        elif new_role.id in MANAGEMENT_TEAM:
            perm = ctx.guild.get_role(1391525588027834498)
        elif new_role.id in HIGHMANAGEMENT_TEAM:
            perm = ctx.guild.get_role(1391525585301409852)
        elif new_role.id in EXECUTIVE_TEAM:
            perm = ctx.guild.get_role(1391525573012226149)
        else:
            perm = None

        if perm:
            await member.add_roles(perm)
            added_roles.append(perm.name)

        await ctx.send(embed=create_embed(f"✅ {member.mention} has been promoted to `{new_role.name}`", 0x00FF00))

        embed=discord.Embed(title=f"Congratulations on {new_role.name}!",color=0x2596be,timestamp=datetime.datetime.now())
        embed.set_author(name='Expose RP', icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_footer(text=f"discord.gg/exposerp | Staff Promotions", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url("your-webhook-link", session=session)
            await webhook.send(f"{member.mention}", embed=embed, avatar_url=self.client.user.avatar.url)

        embed2=discord.Embed(title="Staff promoted", description=f"Member: {member.mention}`({member.id})`\nStaff roles given: `{", ".join(added_roles)}`\n\nGiven by: {ctx.author.mention}",timestamp=datetime.datetime.now(),color=0x2596be)
        embed2.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed2.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url("your-webhook-link", session=session)
            await webhook.send(embed=embed2, avatar_url=self.client.user.avatar.url)

    @staff.command(
    name="demote",
    description="Demotes a staff member by 1 or 2 roles.",
    usage="staff demote <@user> <1 or 2>",
    )
    async def demote(self, ctx, member: discord.Member, steps: int = 1): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if not any(role.id in ALLOWED_ROLES for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))

        if steps < 1 or steps > 2:
            return await ctx.send(embed=create_embed("❌ You can only demote by 1 or 2 tiers.", 0xFF0000))

        staff_team = ctx.guild.get_role(1391525568620662916)
        if staff_team not in member.roles:
            return await ctx.send(embed=create_embed("❌ Member is not currently staff.", 0xFF0000))

        current_index = None
        for i, role_id in enumerate(ROLE_HIERARCHY):
            if ctx.guild.get_role(role_id) in member.roles:
                current_index = i
                break

        if current_index is None:
            return await ctx.send(embed=create_embed("❌ Could not determine current role tier.", 0xFF0000))

        new_index = max(current_index - steps, 0)
        if current_index == new_index:
            return await ctx.send(embed=create_embed(f"⚠️ {member.mention} is already at the lowest role.", 0x2596be))

        new_role = ctx.guild.get_role(ROLE_HIERARCHY[new_index])
        old_role = ctx.guild.get_role(ROLE_HIERARCHY[current_index])
        added_roles = []

        if not new_role:
            return await ctx.send(embed=create_embed("❌ New demotion role not found", 0xFF0000))

        await member.remove_roles(old_role)

        if new_role.id in ADMIN_TEAM:
            expected_perm = ctx.guild.get_role(1391525589151912018)
        elif new_role.id in HIGHERUP_TEAM:
            expected_perm = ctx.guild.get_role(1391525583489339392)
        elif new_role.id in MANAGEMENT_TEAM:
            expected_perm = ctx.guild.get_role(1391525588027834498)
        elif new_role.id in HIGHMANAGEMENT_TEAM:
            expected_perm = ctx.guild.get_role(1391525585301409852)
        elif new_role.id in EXECUTIVE_TEAM:
            expected_perm = ctx.guild.get_role(1391525573012226149)
        else:
            expected_perm = None

        for perm_id in ALL_PERMS:
            perm_role = ctx.guild.get_role(perm_id)
            if perm_role and perm_role in member.roles and perm_role != expected_perm:
                await member.remove_roles(perm_role)

        if expected_perm and expected_perm not in member.roles:
            await member.add_roles(expected_perm)
            added_roles.append(expected_perm.name)

        await member.add_roles(new_role)
        added_roles.append(new_role.name)

        await ctx.send(embed=create_embed(f"✅ {member.mention} has been demoted to `{new_role.name}`", 0xFF0000))
   
        embed = discord.Embed(title="Staff demoted", description=f"Member: {member.mention} (`{member.id}`)\nStaff roles given: `{', '.join(added_roles)}`\n\nRemoved by: {ctx.author.mention}", timestamp=datetime.datetime.now(), color=0xFF0000)
        embed.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url("your-webhook-link", session=session)
            await webhook.send(embed=embed, avatar_url=self.client.user.avatar.url)

async def setup(client):
    await client.add_cog(StaffCommands(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD