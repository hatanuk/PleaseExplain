import discord
from discord.ext import commands
from discord import app_commands
from discord import SelectOption



async def setup(bot):
    await bot.add_cog(Owner(bot))

class Owner(commands.Cog):
    
    # For yours truly

     def __init__(self, bot):
        self.bot = bot
