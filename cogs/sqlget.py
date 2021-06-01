from discord.ext import commands

class SqlGetCog(commands.Cog, name="SqlGet"):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(SqlGetCog(bot))