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
import asyncio
from collections import Counter

cluster = MongoClient("your-mongo-link-here") # REPLACE WITH YOUR MONGO LINK
db = cluster["Expose"]
collection = db["database"]

"""
THIS COG IS FOR LOGGING STAFF SITS THROUGH THE DISCORD BOT, CAN ALSO CHECK LEADERBOARD AND CLEAR SITS.
ONLY CERTAIN ROLES CAN USE THIS COMMAND.

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

STAFF_ROLE_ID = [1391525568620662916] # [Staff Team] # REPLACE WITH YOUR STAFF ROLE ID (ONLY USERS WITH THIS ROLE CAN USE THE COMMANDS)
ALLOWED_ROLES = [ # CHANGE THE FOLLOWING ROLES TO YOUR SERVER'S ROLES (ONLY USERS WITH THESE ROLES CAN USE THE COMMAND)
    1391525588027834498, # [Management Team]
    1391525585301409852, # [Higher Management]
    1391525573012226149, # [Executive Team]
    1391525576719859806 # [Ownership Team]
]

class SitCommands(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.group()
    async def sit(self,ctx): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if ctx.invoked_subcommand is None:
            if not any(role.name in STAFF_ROLE_ID or role.id in STAFF_ROLE_ID for role in ctx.author.roles):
                return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))
            
            if any(role.name in STAFF_ROLE_ID or role.id in STAFF_ROLE_ID for role in ctx.author.roles):
                if not any(role.name in ALLOWED_ROLES or role.id in ALLOWED_ROLES for role in ctx.author.roles):

                    embed=discord.Embed(title="Sit Commands", description="Use `e!sit <command>` with the following args.",color=0x2596be,timestamp=datetime.datetime.now())
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                    embed.add_field(name="Available Commands", value="`log`, `leaderboard`", inline=False)
                    embed.add_field(name="Usage", value="`sit log <id> <consequence/end result> <proof>`\n`sit leaderboard <weekly/global>`", inline=False)
                    await ctx.send(embed=embed)
            
            embed=discord.Embed(title="Sit Commands", description="Use `e!sit <command>` with the following args.",color=0x2596be,timestamp=datetime.datetime.now())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.add_field(name="Available Commands", value="`log`, `clear`, `leaderboard`", inline=False)
            embed.add_field(name="Usage", value="`sit log <id> <consequence/end result> <proof>`\n`sit clear <weekly/global>`\n`sit leaderboard <weekly/global>`", inline=False)
            await ctx.send(embed=embed)

    @sit.command(
        name='log',
        description="Log completed admin sit.",
        usage='sit log <id> <consequence/end result> <proof>'
    ) 
    async def log(self,ctx,id: int, *args): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        consequence = None
        proof = None

        if not any(role.name in STAFF_ROLE_ID or role.id in STAFF_ROLE_ID for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))

        if len(args) == 1:
            consequence = "Question"
            proof = args[0]
        elif len(args) == 2:
            consequence = args[0]
            proof = " ".join(args[1:])
        else:
            return await ctx.send(embed=create_embed("❌ Please provide at least a consequence or a question.", 0xFF0000))

        try:
            collection.update_one(
                {"_id": ctx.guild.id},
                {"$push":{
                    "sits": {
                        "id": id,
                        "consequence": consequence,
                        "proof": proof,
                        "logged_by": ctx.author.id,
                        "timestamp": datetime.datetime.now(),
                        "weekly": True
                    } 
                }},
                upsert=True
            )

            embed2=discord.Embed(title="Sit logged", description=f"Sit ID: `{id}`\nConsequence: `{consequence}`\n\nProof: {proof}",timestamp=datetime.datetime.now(),color=0x2596be)
            embed2.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed2.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

            embed = discord.Embed(description=f"**✅ Sit Logged** **|** ID: **{id}** '**{consequence}**' '**{proof}**'",timestamp=datetime.datetime.now(),color=0x00FF00)
            embed.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url("https://discord.com/api/webhooks/1397752548722610358/8ZgtCtDBcx9kuw4RVj1cIrdzxBUGJclta5vzM6mgP859gXVzyxcheUAaWVeB_lhjCMTG", session=session)
                await webhook.send(embed=embed2, avatar_url=self.client.user.avatar.url)

            return await ctx.send(embed=embed)

        except Exception as e:
            print(f"Error logging sit: {e}")

    @sit.command(
        name="clear",
        description="Reset weekly sit logs.",
        usage="clear <weekly/global>"
    )
    async def clear(self,ctx, mode: str = None): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if not any(role.name in ALLOWED_ROLES or role.id in ALLOWED_ROLES for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))
        
        if mode not in ["weekly", "global"]:
            return await ctx.send(embed=create_embed("❌ Invalid mode. Use `e!clearsits weekly` or `e!clearsits global`", 0xFF0000))
        
        confirm_text = {
            "weekly": "Are you sure you want to reset **WEEKLY** sit logs? This action cannot be undone.",
            "global": "Are you sure you want to reset **ALL** sit logs? This action cannot be undone."
        }
        
        confirmation = await ctx.send(embed=create_embed(confirm_text[mode], color=0x2596be))
        await confirmation.add_reaction("✅")
        await confirmation.add_reaction("❌")   

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == confirmation.id

        try:  
            reaction, user = await self.client.wait_for("reaction_add", timeout=15.0, check=check)

            if str(reaction.emoji) == "✅":   
                if mode == "weekly":
                    await confirmation.delete()
                    collection.update_one({"_id": ctx.guild.id}, {"$set": {"sits.$[].weekly": False}})
                    await ctx.send(embed=create_embed("✅ Weekly sit logs have been cleared.", 0x00FF00))

                    embed2=discord.Embed(title="📭 Weekly Sit Logs Cleared", description=f"**Expose RP |** Weekly sit logs have been cleared by {ctx.author.mention}", timestamp=datetime.datetime.now(),color=0x2596be)
                    embed2.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                    embed2.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url("https://discord.com/api/webhooks/1397752548722610358/8ZgtCtDBcx9kuw4RVj1cIrdzxBUGJclta5vzM6mgP859gXVzyxcheUAaWVeB_lhjCMTG", session=session)
                        await webhook.send(embed=embed2, avatar_url=self.client.user.avatar.url)

                elif mode == "global":
                    await confirmation.delete()
                    collection.update_one({"_id": ctx.guild.id}, {"$set": {"sits": []}})
                    await ctx.send(embed=create_embed("✅ All sit logs have been cleared.", 0x00FF00))

                    embed2=discord.Embed(title="📭 Global Sit Logs Cleared", description=f"**Expose RP |** All sit logs have been cleared by {ctx.author.mention}", timestamp=datetime.datetime.now(),color=0x2596be)
                    embed2.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                    embed2.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

                    async with aiohttp.ClientSession() as session:

                        webhook = Webhook.from_url("https://discord.com/api/webhooks/1397752548722610358/8ZgtCtDBcx9kuw4RVj1cIrdzxBUGJclta5vzM6mgP859gXVzyxcheUAaWVeB_lhjCMTG", session=session)
                        await webhook.send(embed=embed2, avatar_url=self.client.user.avatar.url)

            else:
                await ctx.message.delete()
                return await confirmation.delete()
        except asyncio.TimeoutError:
            await confirmation.delete()
            return await ctx.send(embed=create_embed("You took too long to respond. Please try again.",color=0x2596be))
        except Exception as e:
            print(f"An error occurred: {e}")

    @sit.command(
        name="leaderboard",
        description="Displays the sits leaderboard.",
        usage="sit leaderboard <weekly/global>",
        aliases=["lb"],
    )
    async def leaderboard(self, ctx, mode: str = "global"): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if not any(role.name in STAFF_ROLE_ID or role.id in STAFF_ROLE_ID for role in ctx.author.roles):
            return await ctx.send(embed=create_embed("❌ You do not have permission to use this command.", 0xFF0000))

        mode = mode.lower()
        data=collection.find_one({"_id": ctx.guild.id})

        if not data or "sits" not in data:
            return await ctx.send(embed=create_embed("❌ No sits found in this server.", 0xFF0000))

        if mode not in ["global", "weekly"]:
            return await ctx.send(embed=create_embed("❌ Invalid mode. Use `e!leaderboard global` or `e!leaderboard weekly`.", 0xFF0000))
        
        if mode == "weekly":
            sits = [s for s in data["sits"] if s.get("weekly") == True]
        else:
            sits = data["sits"]

        if not sits:
            return await ctx.send(embed=create_embed(f"📭 No sits found for `{mode}` leaderboard.", 0xFF0000))
        
        counter = Counter([s["logged_by"] for s in sits])
        top_users = counter.most_common(10)


        embed=discord.Embed(title=f"🏆 Sit Leaderboard - {mode.capitalize()}",color=0x2596be,timestamp=datetime.datetime.now())
        embed.set_footer(text=f"User ID: {ctx.author.id}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_author(name=str(ctx.author.name), icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        for i, (user_id, count) in enumerate(top_users, start=1):
            member = ctx.guild.get_member(user_id)
            name = member.display_name if member else f"<@{user_id}>"
            embed.add_field(name=f"{i} - {name}", value=f"<:starsltool:1394165960688009276> `{count}` sit(s) logged.", inline=False)

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(SitCommands(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD