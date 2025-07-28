import lib.bot
import discord
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

try:
    lib.bot.startup.bot.run(TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for"
            "-toomanyrequests")
    else:
        raise e
