# NOTE : Might not need this file

import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")
    
    @commands.command()
    async def check_perms(self, ctx):
        perms = ctx.channel.permissions_for(ctx.guild.get_member(self.bot.user.id))
        await ctx.send(f"My permissions here:\n{perms}")



async def setup(bot):
    await bot.add_cog(Commands(bot))