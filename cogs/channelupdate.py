import discord
import os
from typing import cast
from discord.ext import commands,tasks
from discord.utils import get
from dotenv import load_dotenv
from cogs.sqlget import sql_select
from cogs.sqladd import sql_insert
from datetime import datetime, timedelta

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)
unbkey = os.getenv('UNBKEY')
headers = {'Authorization': unbkey}
pokerBotID = "613156357239078913"
botUrl = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/613156357239078913"

class channelUpdateCog(commands.Cog, name="channelUpdate"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        rows = await sql_select("channels","owners","owner","%")
        embedVar = discord.Embed(title="Current Channels and Owners", description="NUKE THEM ALL", color="#FF0000")
        rows = await sql_select("channels", "owners", "owner", "%")
        if rows:
            for row in rows:
                oID = int(row[0])
                cID = int(row[1])
                owner = self.bot.get_user(oID)
                oChannel = self.bot.get_channel(cID)
                embedVar.add_field(name=f'**{oChannel.name}**', value=f'> Owned By: {owner.name}' )
        channel = self.bot.get_channel(847311082091184138)
        #msg = await channel.fetch_message(850221103963045898)
        send = await channel.send(embed=embedVar)

def setup(bot):
    bot.add_cog(channelUpdateCog(bot))
