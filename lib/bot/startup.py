import discord
import sys
import importlib
from discord.ext import commands
import lib.data.datalib as db
import os

intents = discord.Intents.default()
intents.message_content = True
intents.presences = False
intents.typing = False
intents.messages = True
intents.guilds = True

COG_DIR = "lib/cogs"
UTIL_DIR = "lib/util"

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        self.reload_utils()
        await self.reload_cogs()

    async def on_ready(self):
        self.build_db()

        print("Commands loaded:")
        for cmd in bot.commands:
            print(cmd.name)

    def reload_utils(self): 
        submodules = [submodule for submodule in sys.modules if submodule.startswith(UTIL_DIR.replace("/", ".") + ".")]
        for submodule in submodules:
            submodule = sys.modules.get(submodule)
            importlib.reload(submodule)

    async def reload_cogs(self):
        for filename in os.listdir(COG_DIR):
            if filename.endswith(".py") and not filename.startswith("_"):
                ext_name = f'{COG_DIR.replace("/", ".")}.{filename[:-3]}'
                if ext_name in self.extensions:
                    await self.unload_extension(ext_name)
                await self.load_extension(ext_name)
                print(f'{ext_name} loaded')

    def build_db(self):
        db.build([guild.id for guild in self.guilds])


bot = Bot(command_prefix='!', intents=intents)
