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
THIS COG HANDLES PUNISHMENT FOR DIFFERENT OFFENSES.
NEVER FINISHED IT SO YOU CAN DO IT YOURSELF IF YOU WANT.

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

class PunishEmbed(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.group()
    async def punishments(self, ctx): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="Punishment Commands", description="Use `e!punishments <command>` with the following args.", color=0x2596be, timestamp=datetime.datetime.now())
            
async def setup(client):
    await client.add_cog(PunishEmbed(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD