"""
CREATE A BOT INSTANCE FROM DISCORD DEV PAGE AND ENABLE INTENTS FOR THIS TO WORK. 
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

THIS IS ALSO THE DEFAULT EMBED COLOR, YOU CAN CHANGE IT AS NEEDED.

"""

import discord

def create_embed(text, color=None):
    if color == None:
        embed = discord.Embed(description=text, colour=0x2596be)
    else:
        embed = discord.Embed(description=text, colour=color)

    return embed