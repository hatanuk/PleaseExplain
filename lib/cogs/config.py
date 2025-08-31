import discord
import datetime
import importlib
from discord.ext import commands
from discord import app_commands

import lib.data.datalib as db
import lib.util
from lib.data.datalib import MAX_TERMS
from lib.util.cache_helper import cache_image, uncache_image
from lib.util.image_gen import create_def_image, create_dictionary_image
from lib.util.validation import Validator
from lib.util.embed_helper import create_def_embed, create_term_embed, create_dict_embed, create_config_embed
from lib.util.api_helper import get_user_from_id

async def setup(bot):
    await bot.add_cog(Config(bot))

def perform_deletion(type, guild_id):
    match type:
        case "usage":
            db.clear_usage_data(guild_id)
        case "dictionary":
            db.clear_dictionary_data(guild_id)
        case "all":
            db.clear_all_data(guild_id)
    


class Config(commands.Cog):

    # User-controlled configurations for the bot

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="view_config",
        description="displays the bot's configurations"
    )
    async def view_config(self, interaction: discord.Interaction):
        results = db.fetch_config(interaction.guild.id) 

        embed = create_config_embed(results)

        await interaction.response.send_message(embed=embed)



    @app_commands.command(
        name="usage_counting",
        description="allow or disallow messages to be monitored for counting usage of terms"
    )
    @app_commands.describe(option="turn usage counting 'on' or 'off'")
    @app_commands.choices(option=[
        app_commands.Choice(name="on", value="on"),
        app_commands.Choice(name="off", value="off")
    ])
    async def usage_counting(self, interaction: discord.Interaction, option: app_commands.Choice[str]):
        guild_id = interaction.guild_id
        if option.value == "on":
            db.set_monitoring(guild_id, on=True)
            await interaction.response.send_message("usage counting is now `ON`. i'll be listening.", ephemeral=True)
        else:
            db.set_monitoring(guild_id, on=False)
            await interaction.response.send_message("usage counting is now `OFF`. didn't hear nothin'", ephemeral=True)
 
    @app_commands.command(
        name="clear_data",
        description="permanently removes data associated with the bot"
    )
    @app_commands.describe(option="which type of data to delete")
    @app_commands.choices(option=[
        app_commands.Choice(name="usage", value="usage"),
        app_commands.Choice(name="dictionary", value="dictionary"),
        app_commands.Choice(name="all", value="all")
    ])
    async def clear_data(self, interaction: discord.Interaction, option: app_commands.Choice[str]):
        await interaction.response.send_message(
            f"are you sure you want to delete `{option.value}` data? react with ✅ to confirm or ❌ to cancel, just remember, there is no going back.",
            ephemeral=False
        )

        msg = await interaction.original_response()
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return (
                user == interaction.user and
                str(reaction.emoji) in ["✅", "❌"] and
                reaction.message.id == msg.id
            )

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except Exception:
            await msg.edit(content="okay nevermind.")
            await msg.delete(delay=3)
            return

        if str(reaction.emoji) == "✅":
            perform_deletion(option.value, interaction.guild.id)
            await msg.edit(content=f"`{option.value}` data has been eradicated.")
            await msg.delete(delay=3)
        else:
            await msg.edit(content="data deletion cancelled.")
            await msg.delete(delay=3)


    