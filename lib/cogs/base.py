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
from lib.util.embed_helper import create_def_embed, create_term_embed, create_dict_embed


async def setup(bot):
    await bot.add_cog(Base(bot))


class Base(commands.Cog):

    # Includes the basic functionalities of the bot

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pleaseexplain", description="explains a term in the server's dictionary, if it exists")
    async def pleaseexplain(self, interaction: discord.Interaction, term: str):

        # Fetching from DB ----
        result = db.fetch_term(interaction.guild_id, term)

        if result is None:
            await interaction.response.send_message(
                "sorry, I couldn't find a definition for that term in this server. \nplease do `/dictionary` to see "
                "all available terms!")
            return
        
        term, definition, creatorid, created_at, updated_at, image = result

        # Fetching the creator & requestor
        creator = interaction.client.get_user(creatorid)
        if creator is None:
            creator = await interaction.client.fetch_user(creatorid)
        requestor = interaction.user

        # await create_def_image(term)
        image = create_dictionary_image(term, definition)
        file, url = cache_image(image, interaction.guild.id, requestor.id)
        embed = create_def_embed(url, creator, requestor, created_at, updated_at)
        await interaction.response.send_message(embed=embed, file=file)
        uncache_image(interaction.guild.id, requestor.id)

    @app_commands.command(name="define", description="adds a term and its definition to your server's dictionary")
    async def define(self, interaction: discord.Interaction, term: str, definition: str, image: str = None):

        MIN_DEF_LENGTH = 3
        MAX_DEF_LENGTH = 500
        MAX_TERM_LENGTH = 15

        # String validation
        if index := Validator.validate_string(definition):
            accepted = " ".join(Validator.ACCEPTED_CHAR)
            await interaction.response.send_message(
                f"sorry, i am unable to use the character at `position {index}` of your definition.\nplease only use "
                f"letters or numbers as well as any of these symbols: \n`{accepted}`")
            return
        elif index := Validator.validate_string(term):
            accepted = " ".join(Validator.ACCEPTED_CHAR)
            await interaction.response.send_message(
                f"sorry, i am unable to use the character at `position {index}` of your term.\nplease only use "
                f"letters or numbers as well as any of these symbols: \n`{accepted}`")
            return
        elif len(definition) < MIN_DEF_LENGTH:
            await interaction.response.send_message(
                f"please give a slightly more descriptive description. `(min: {MIN_DEF_LENGTH} characters)`")
            return
        elif len(definition) > MAX_DEF_LENGTH:
            await interaction.response.send_message(
                f"sorry, the character limit for descriptions is `{MAX_DEF_LENGTH}`.")
            return
        elif len(term) > MAX_TERM_LENGTH:
            await interaction.response.send_message(
                f"sorry, the character limit for terms is `{MAX_TERM_LENGTH}`.")
            return

        time = datetime.datetime.now().replace(microsecond=0).isoformat()
        userid = interaction.user.id
        guildid = interaction.guild.id

        feedback = db.insert_definition(term, definition, userid, guildid, time, image)

        if feedback == "successful":
            await interaction.response.send_message(
                f"the term `{term}` has been added to your server dictionary. \nuse `/PleaseExplain` to see it! ")
        elif feedback == "full":
            await interaction.response.send_message(
                f"your server dictionary is at maximum capacity `({str(MAX_TERMS)})`!\n"
                "please use `/undefine` to make some space")
        elif feedback == "already_exists":
            await interaction.response.send_message(
                f"sorry, the term `{term}` already exists in the server dictionary!")
        else:
            await interaction.response.send_message(
                f"ow, there's been an error. please contact `akahunt` if you see this. yes - I'll give you a `cookie`.")

    @app_commands.command(name="undefine", description="removes a definition from your server dictionary")
    async def undefine(self, interaction: discord.Interaction, term: str):
        guild_id = str(interaction.guild.id)
        if db.get_term_count(term, guild_id) < 1:
            await interaction.response.send_message(
                "sorry, I could not find that term in this server. \nplease do `/dictionary` to see all avaliable "
                "terms!")
            return

        success = db.remove_term(term, guild_id)
        if success:
            await interaction.response.send_message(
                "the term has successfully been removed from your server dictionary!")
        else:
            await interaction.response.send_message(
                "oh, uh, I couldn't remove it for whatever reason. please contact `akahunt` if you see this.")

    @app_commands.command(name="pleaseexplainold", description="explains a definition found in the server's dictionary")
    async def pleaseexplainold(self, interaction: discord.Interaction, term: str):

        # Fetching and validating values
        result = db.fetch_term(interaction.guild_id, term)
        if result is None:
            await interaction.response.send_message(
                "sorry, I couldn't find a definition for that term in this server. \nplease do `/dictionary` to see "
                "all server definitions!")
            return

        term, definition, creatorid, created_at, updated_at, image = result

        # Preparing the values for presentation
        creator = interaction.client.get_user(creatorid)
        if creator is None:
            creator = await interaction.client.fetch_user(creatorid)

        # Creating embed
        embed = create_term_embed(interaction, term, creatorid, created_at, updated_at, image)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dictionary", description="displays all the defined terms in the server")
    async def dictionary(self, interaction: discord.Interaction, page: int = 1):

        TERMS_PER_PAGE = 18

        # Fetching from DB
        result = db.fetch_all_terms(interaction.guild.id)

        if result is None:
            await interaction.response.send_message(
                f"I can't find any terms in your server dictionary. have you tried using `/define`?")
            return
        
        # Calculating maximum pages
        max_pages = len(result) // TERMS_PER_PAGE + 1
        # Accounting for if the value is exactly at the boundary, preventing empty pages
        if len(result) % TERMS_PER_PAGE == 0:
            max_pages -= 1


        # Validation
        if page > max_pages or page < 1:
            await interaction.response.send_message(
                f"invalid page number. this server's dictionary contains `{max_pages}` {'page' if max_pages == 1 else 'pages'}, by the way.")
            return
        # Creating list of user objects
        creators = []
        creator_cache = {}
        target_values = []

        # calculating starting and ending indexes to loop through
        start_index = (page - 1) * TERMS_PER_PAGE
        end_index = TERMS_PER_PAGE * page

        for value in result[start_index:end_index]:
            term_name, _, creator_id, _, _, _ = value
            target_values.append(term_name)
            # cache id : user object pairs in dictionary to prevent duplicate fetching
            if creator_id not in creator_cache.keys():
                creator = interaction.client.get_user(creator_id)
                if creator is None:
                    creator = await interaction.client.fetch_user(creator_id)
                creator_cache[creator_id] = creator
            else:
                creator = creator_cache[creator_id]
            creators.append(creator)

        # Creating embed
        total_results = len(result)
        embed = create_dict_embed(target_values, creators, page, max_pages, total_results)
        await interaction.response.send_message(embed=embed)
