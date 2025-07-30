import discord

async def get_user_from_id(client, user_id):
    user = client.get_user(user_id)
    if user is None:
        try:
            user = await client.fetch_user(user_id)
        except:
            user = None  
    return user
