import discord
import eng_to_ipa


def create_def_embed(url, creator, requestor, created_at, updated_at):

    creator_name, creator_avatar = _get_name_and_avatar(creator)
    requestor_name, _ = _get_name_and_avatar(requestor)

    created_at, updated_at = created_at[:10], updated_at[:10]
    embed = discord.Embed(title="Requested by " + requestor_name,
                          color=0x006eb3)
    
    print(url)
    embed.set_image(url=url)
    embed.set_footer(text=f"author: {creator_name}\ncreated at: {created_at}; updated at: {updated_at}",
                     icon_url=creator_avatar)
    return embed


def create_term_embed(term, definition, creator, created_at, updated_at, image):
    created_at, updated_at = created_at[:10], updated_at[:10]
    phonetics = eng_to_ipa.convert(term)

    if "*" in list(phonetics):
        phonetics = None
    # -------
    # Creating the embed
    embed = discord.Embed(title=term, description=definition,
                          color=0x006eb3)
    if phonetics:
        embed.set_author(name=phonetics)
    if image:
        embed.set_thumbnail(
            url=image)
    embed.set_footer(text=f"author: {creator.name}; created at: {created_at}; updated at: {updated_at}",
                     icon_url=creator.display_avatar)
    return embed
    # -------


def create_dict_embed(values, creators, page, max_pages, total):
    embed = discord.Embed(title="Server Dictionary",
                          color=0x006eb3)
    embed.set_footer(text=f"page {page} out of {max_pages} | {len(values)} results | {total} total")
    for value, creator in zip(values, creators):
        creator_name, _ = _get_name_and_avatar(creator)
        embed.add_field(name=str(value), value="by " + creator_name, inline=True)

    return embed


def _get_name_and_avatar(user):
        try:
            name = user.name
            avatar = user.display_avatar
        except AttributeError:
            name = "unknown"
            avatar =  discord.User.default_avatar
        return name, avatar