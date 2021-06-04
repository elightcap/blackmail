import discord
import os
from typing import cast
from discord.ext import commands,tasks
from cogs.sqlget import sql_select
from dotenv import load_dotenv
from discord.utils import get

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)



class channelTableCog(commands.Cog, name="channelTable"):
    def __init__(self, bot):
        self.bot = bot
        self.update_table.start()

    @tasks.loop(minutes=1)
    async def update_table(self):
        await self.bot.wait_until_ready()
        embedVar = discord.Embed(title="Channels", description="The channels", color=0x00ff00)
        rows = await sql_select("channels", "owners", "owner", "%")
        if rows:
            for row in rows:
                print(row)
                oID = int(row[0])
                cID = int(row[1])
                print(oID)
                print(cID)
                owner = self.bot.get_user(oID)
                oChannel = self.bot.get_channel(cID)
                print(oChannel)
                print(owner)
                embedVar.add_field(name=f'**{oChannel.name}**', value=f'> Owned By: {owner.name}' )
        channel = self.bot.get_channel(850206859898257408)
        send = await channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(channelTableCog(bot))
