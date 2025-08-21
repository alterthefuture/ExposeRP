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
THIS COG HANDLES THE VERIFICATION SYSTEM FOR THE SERVER SO USERS CAN GET ACCESS TO THE REST OF THE SERVER.

YOU CAN CHANGE THE STYLE AS NEEDED.
MADE BY PLAYEDYABTCH - DISCORD.GG/WRD

"""

VERIFIED_ROLE_NAME = "Community" # CHANGE THIS TO THE ROLE NAME YOU WANT TO GIVE ON VERIFY

class VerifyButton(discord.ui.View): # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    def __init__(self,client):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Verify", style=discord.ButtonStyle.success, custom_id="verify_button") # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user
        role = discord.utils.get(guild.roles, name=VERIFIED_ROLE_NAME)

        if role is None:
            print(f"Role '{VERIFIED_ROLE_NAME}' not found in guild '{guild.name}'")

        if role in member.roles:
            print(f"{member.name} already has the {VERIFIED_ROLE_NAME} role.")
           
        await member.add_roles(role, reason="Verified via button")

class Verifier(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(
        name="verify",
        description="Verify yourself to get access to the server.",
        usage="verify"
    )
    @commands.is_owner()
    async def verify(self, ctx):  # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD 
        embed = discord.Embed(title="Verification",description="To gain access to the rest of the server, make sure to click the `Verify` button!",color=0x2596be)
        embed.set_footer(text=f"Contact a staff member if you run into any issues")
        embed.set_image(url="https://media.discordapp.net/attachments/1395337204745764904/1395337292708581376/discordbannerahh.png?ex=687e091e&is=687cb79e&hm=17aa6a18e9b60b5608453ad29ea293fc62a0dde48ec41bab34d17604ed74b889&format=webp&quality=lossless&")

        view = VerifyButton(self.client)
        await ctx.send(embed=embed, view=view)
  
async def setup(client):
    await client.add_cog(Verifier(client)) # MADE BY PLAYEDYABTCH - DISCORD.GG/WRD