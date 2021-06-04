import discord
import os
from typing import cast
from discord.ext import commands,tasks
from cogs.sqlget import sql_select

class channelTableCog(commands.Cog, name="channelTable"):
    def __init__(self, bot):
        self.bot = bot
        self.update_table.start()
        
    @tasks.loop(minutes=1)
    async def update_table(self, ctx):
        embedVar = discord.Embed(title="Channels", description="The channels", color=0x00ff00)
        rows = sql_select("channels", "owners", "owner", "%")
        for row in rows:
            oID = row[0]
            cID = row[1]
            owner = ctx.guild.get_member(oID)
            channel = self.bot.get_channel(cID)
            embedVar.add_field(name=f'**{channel.name}**', value=f'>{owner.name}' )
         channel = self.bot.get_channel(850206859898257408)
        send = await channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(channelTableCog(bot))