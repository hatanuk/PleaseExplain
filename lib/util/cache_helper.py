import discord
import os
import lib.data.datalib as db

IMAGE_CACHE_DIR = "lib/data/image_data/image_cache"
def cache_image(image, guild_id, requestor_id):
    filename = f"{guild_id}A{requestor_id}.png"
    url = f'attachment://{filename}'

    save_path = f"{IMAGE_CACHE_DIR}/{filename}"
    image.save(save_path)
    file = discord.File(f"{IMAGE_CACHE_DIR}/{filename}", filename=filename)

    return file, url

def uncache_image(guild_id, requestor_id):
    filename = f"{guild_id}A{requestor_id}.png"
    save_path = f"{IMAGE_CACHE_DIR}/{filename}"
    if os.path.exists(save_path):
        os.remove(save_path)

class UsageCounter:

    def __init__(self):

        self.REFRESH_RATE = 1

        self.cache = {}
        self.to_refresh = {}


    def setup(self, guilds):
        self.cache_all_counts(guilds)
        self.init_refresh(guilds)

    def cache_guild_count(self, guild_id):
        if db.is_monitoring_on(guild_id):

            if guild_id not in self.cache:
                self.cache[guild_id] = {}

            results = db.fetch_all_terms(guild_id)
            if not results: return
            for result in results:
                term_name, _, _, _, _, _, usage_count = result

                if usage_count is None:
                    usage_count = 0

                self.cache[guild_id][term_name] = usage_count


    def refresh(self, guild_id):
        print(self.cache[guild_id])
        for term in self.cache[guild_id].keys():
            print(f"setting {term} to {self.cache[guild_id][term]}")
            db.set_usage_count(guild_id, term, self.cache[guild_id][term])
        self.to_refresh[guild_id] = 0

    def init_refresh(self, guilds):
        for guild in guilds:
            self.to_refresh[guild.id] = 0


    def cache_all_counts(self, guilds):
        for guild in guilds:
            self.cache_guild_count(guild.id)

    def clear_cache(self, guild_id):
        self.cache[guild_id] = {}


    