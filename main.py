"""
CREATE A BOT INSTANCE FROM DISCORD DEV PAGE AND ENABLE INTENTS FOR THIS TO WORK. 
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

ALSO CREATE A MONGO DB AND REPLACE THE LINK BELOW WITH YOUR MONGO LINK.
MAKE SURE TO REPLACE THE TOKEN BELOW WITH YOUR BOT TOKEN.

I CBA TO WALK YOU THROUGH THE SETUP, JUST FOLLOW THE INSTRUCTIONS ON THE DISCORD DEVELOPER PORTAL AND MONGO DB.

THIS BOT IS FOR A FIVEM DISCORD SERVER. HAVE FUN SKIDDING

"""

import os
import discord
from discord.ext import commands
import asyncio
from pymongo import MongoClient
from helper import *

os.system(f'cls & mode 85,20 & title [DISCORD.GG/WRD] - PLAYEDYABTCH')

cluster = MongoClient("your-mongo-link-here") # REPLACE WITH YOUR MONGO LINK
db = cluster["Expose"]
collection = db["database"]

intents = discord.Intents.all()
client = commands.Bot(command_prefix="e!",intents=intents,case_insensitive=True,owner_ids=[837939884429279252,1050907666068807721]) # CHANGE PREFIX AND OWNER IDS AS NEEDED
client.remove_command("help")

token = "token-here" # REPLACE WITH YOUR BOT TOKEN
client.config_token = token

@client.event
async def on_ready():
    
    print("$-> Evade bot is online.")

    guilds = client.guilds
    dbguilds = []
    for item in collection.find():
      dbguilds.append(item["_id"])
    for guild in guilds:
      if guild.id not in dbguilds:
        collection.insert_one({
            "_id": guild.id,
            "sits": [],
            "points": [],
            "muted_members": [],
            "invites": {}})
        print(f"> {guild.id} Has been added to database.")

@client.event
async def on_message(message):
    if message.author.bot:
        return 
    
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=create_embed(f"❌ This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.", 0xFF0000))

async def load_cogs():
    for root, dirs, files in os.walk('./cogs'):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                path = os.path.join(root, file)
                module = path.replace('./', '').replace('\\', '/').removesuffix('.py').replace('/', '.')
                try:
                    await client.load_extension(module)
                    print(f"Loaded: {module}")
                except Exception as e:
                    print(f"Failed to load {module}: {e}")

async def main():
    async with client:
        await load_cogs()
        await client.start(client.config_token)

asyncio.run(main())