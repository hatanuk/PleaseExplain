from collections import defaultdict
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


        self.cache = defaultdict(dict)
        self.to_refresh = defaultdict(int)


    def setup(self, guilds):
        self.cache_all_counts(guilds)
        self.init_refresh(guilds)

    def cache_guild_count(self, guild_id):
        if db.is_monitoring_on(guild_id):

            # Ensure entry exists
            _ = self.cache[guild_id]

            results = db.fetch_all_terms(guild_id)
            if not results:
                # keep empty mapping if nothing to cache
                self.cache[guild_id] = {}
                return

            for result in results:
                # TermName is first; UsageCount may or may not be included depending on query
                term_name = result[0]
                usage_count = result[6] if len(result) > 6 else 0

                if usage_count is None:
                    usage_count = 0

                self.cache[guild_id][term_name] = usage_count
        else:
            # monitoring off; ensure empty mapping to avoid KeyErrors elsewhere
            self.cache[guild_id] = {}


    def refresh(self, guild_id):
        # Ensure cache is present for this guild; populate on-demand
        data = self.cache.get(guild_id)
        if not data:
            self.cache_guild_count(guild_id)
            data = self.cache.get(guild_id)
            if not data:
                self.to_refresh[guild_id] = 0
                return

        for term, count in data.items():
            db.set_usage_count(guild_id, term, count)
        self.to_refresh[guild_id] = 0

    def init_refresh(self, guilds):
        for guild in guilds:
            # touch defaults
            _ = self.to_refresh[guild.id]


    def cache_all_counts(self, guilds):
        for guild in guilds:
            self.cache_guild_count(guild.id)

    def clear_cache(self, guild_id):
        self.cache[guild_id] = {}


