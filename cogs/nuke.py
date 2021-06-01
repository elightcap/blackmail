import discord
from discord.ext import commands

class NukeCog(commands.Cog, name="Nuke"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='nuke')
    @commands.guild_only()
    async def do_nuke(self, ctx, *, our_input: str):
        await ctx.send(our_input)

def setup(bot):
    bot.add_cog(NukeCog(bot))