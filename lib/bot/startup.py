import discord
from discord.ext import commands
import lib.data.datalib as db
import os

intents = discord.Intents.default()
intents.presences = False
intents.typing = False
intents.messages = True
intents.guilds = True

COG_DIR = "lib/cogs"

GUILD_IDS = []

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():

    # Loads all .py files under COG_DIR as extensions
    for filename in os.listdir(COG_DIR):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f'{COG_DIR.replace("/", ".")}.{filename[:-3]}')

    for guild in bot.guilds:
        bot.tree.clear_commands(guild=guild)
        GUILD_IDS.append(guild.id)
    
    await bot.tree.sync()

    db.build(GUILD_IDS)

    print("guild_ids: ")
    print(GUILD_IDS)
    print('We have logged in as {0.user}'.format(bot))

