import discord
import sys
import importlib
from discord.ext import commands
import lib.data.datalib as db
import os
import lib.util
from lib.util.cache_helper import UsageCounter

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.messages = True
intents.guilds = True

COG_DIR = "lib/cogs"
UTIL_DIR = "lib/util"
DB_LIB_PATH = "lib/data/datalib"

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usage_counter = UsageCounter()

    async def setup_hook(self):
        self.reload_utils()
        await self.reload_cogs()

    async def on_ready(self):
        print("RADDADNADNE")
        self.build_db()
        self.usage_counter.setup(self.guilds)
        print("ready")
        print(self.usage_counter)

    def reload_utils(self): 

        # Reload util __init__
        importlib.reload(lib.util)

        # Reload all util submodules
        submodules = [submodule for submodule in sys.modules if submodule.startswith(UTIL_DIR.replace("/", ".") + ".")]
        for submodule in submodules:
            submodule = sys.modules.get(submodule)
            importlib.reload(submodule)

        # Reload datalib as well
        importlib.reload(db)
        

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
