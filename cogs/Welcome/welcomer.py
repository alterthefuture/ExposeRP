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

"""
THIS COG HANDLES THE WELCOME MESSAGE FOR NEW MEMBERS JOINING THE SERVER.
JUST CHANGE THE CHANNEL ID TO YOUR CHANNEL

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

class Welcome(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self,member): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
        embed=discord.Embed(title=f"Welcome to Expose RP!", description="Make sure to check out the following channels if you are new!\n\n<#1391598831212171315>\n<#1393539776220495902>",color=0x2596be)
        embed.set_footer(text=f"We are ALWAYS hiring staff feel free to apply")
        embed.set_image(url="https://media.discordapp.net/attachments/1395337204745764904/1395337341459234849/SMDBANNERWLECOME.png?ex=687e092a&is=687cb7aa&hm=d032e788725d838dee434a76017f106c22a03e4c7bde36c3071cbad069990db6&=&format=webp&quality=lossless&width=1227&height=690")

        channel = self.client.get_channel(1391598583719133255)

        return await channel.send(f"{member.mention}",embed=embed)
            
async def setup(client):
    await client.add_cog(Welcome(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD 