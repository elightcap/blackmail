import discord
from discord.ext import commands

class InviteCog(commands.Cog, name="Invite"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='invite')
    @commands.guild_only()
    async def do_nuke(self, ctx, *, our_input: str):
        await ctx.send(our_input)

def setup(bot):
    bot.add_cog(InviteCog(bot))