import discord
import os

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
