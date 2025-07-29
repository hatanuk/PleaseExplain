import discord
from discord.ext import commands
from discord import app_commands
from discord import SelectOption



async def setup(bot):
    await bot.add_cog(Owner(bot))

class Owner(commands.Cog):
    
    # For yours truly

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload_cog(self, ctx, cog_name: str):
        try:
            ext_name = f"lib.cogs.{cog_name}" 
            if ext_name in self.bot.extensions:
                await self.bot.unload_extension(ext_name)
            await self.bot.load_extension(ext_name)
            await ctx.send(f"Reloaded cog `{cog_name}` successfully.")
        except Exception as e:
            await ctx.send(f"Failed to reload cog `{cog_name}`.\nError: {e}")

    @commands.command(name="reload_all")
    @commands.is_owner()
    async def reload_all(self, ctx):
        try:
            await self.bot.reload_cogs()
        except Exception as e:
            await ctx.send(f"Failed")

    @commands.command(name="global_sync")
    @commands.is_owner()
    async def global_sync(self, ctx):
        await self.bot.tree.sync()

    @commands.command(name="local_sync")
    @commands.is_owner()
    async def local_sync(self, ctx):
        await self.bot.tree.sync(guild=ctx.guild)
