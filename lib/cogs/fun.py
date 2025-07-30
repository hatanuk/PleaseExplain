import discord
import random
import lib.data.datalib as db
from lib.util.image_gen import create_dictionary_image
from lib.util.cache_helper import cache_image, uncache_image
from lib.util.embed_helper import create_def_embed

from discord.ext import commands
from discord import app_commands
from discord import SelectOption



async def setup(bot):
    await bot.add_cog(Fun(bot))

class Fun(commands.Cog):
    
    # Extra features

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="random", description="samples a random quote from the server's dictionary" )
    async def random(self, interaction: discord.Interaction):


        result = db.fetch_all_terms(interaction.guild.id)

        if result is None:
            await interaction.response.send_message(
                f"I can't find any terms in your server dictionary. have you tried using `/define`?")
            return
        
        
        sampled = random.sample(result, 1)[0]
        term, definition, creator_id, created_at, updated_at, *_ = sampled
        requestor = interaction.user
        image = create_dictionary_image(term, definition)
        print(image)
        file, url = cache_image(image, interaction.guild.id, requestor.id)
        embed = create_def_embed(url, creator_id, requestor.id, created_at, updated_at)
        await interaction.response.send_message(embed=embed, file=file)
        uncache_image(interaction.guild.id, requestor.id)



        
