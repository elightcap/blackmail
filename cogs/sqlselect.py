from discord.ext import commands

class SqlSelectCog(commands.Cog, name="Nuke"):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(SqlSelectCog(bot))