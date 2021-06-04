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
    async def on_message(self, message):
        if message.type == discord.MessageType.pins_add:
            print("name change")

def setup(bot):
    bot.add_cog(channelUpdateCog(bot))
