import discord
from discord.ext import commands
from discord import app_commands
from discord import SelectOption



async def setup(bot):
    await bot.add_cog(Debug(bot))

class Debug(commands.Cog):
    
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
            await ctx.send(f"reloaded `{cog_name}`")
        except Exception as e:
            await ctx.send(f"failed to reload `{cog_name}`.\nError: {e}")

    @commands.command(name="reload_all")
    @commands.is_owner()
    async def reload_all(self, ctx):
        try:
            self.bot.reload_utils()
            await self.bot.reload_cogs()
            await ctx.send(f"yes king")
        except Exception as e:
            await ctx.send(f"Failed: {e}")

    @commands.command(name="reload_utils")
    @commands.is_owner()
    async def reload_utils(self, ctx):
        try:
            self.bot.reload_utils()
            await ctx.send(f"yes king")
        except Exception as e:
            await ctx.send(f"Failed: {e}")

    @commands.command(name="global_sync")
    @commands.is_owner()
    async def global_sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.send(f"yes king")

    @commands.command(name="local_sync")
    @commands.is_owner()
    async def local_sync(self, ctx):
        self.bot.tree.clear_commands(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        self.bot.tree.copy_global_to(guild=ctx.guild)
        await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"yes king")

    @commands.command(name="log_cmds")
    @commands.is_owner()
    async def log_cmds(self, ctx):
        cmds = self.bot.tree.get_commands()
        await ctx.send([cmd.name for cmd in cmds if isinstance(cmd, discord.app_commands.Command)])
