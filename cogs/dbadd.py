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

class dbaddCog(commands.Cog, name="dbadd"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        if len(before.roles)<len(after.roles):
            newRole = next(role for role in after.roles if role not in before.roles)
            uid = int(after.id)
            if newRole.name == "Robbery Victim":
                await sql_insert("robbed", "users", uid)
                print("rob vic success add")
            elif newRole.name == "Blackmailer":
                await sql_insert("blackmailer", "users", uid)
                print("blackmail success add")
            elif newRole.name == "Lawyer'd Up":
                await sql_insert("lawyer", "users", uid)
                print("lawyer vic success add")
            elif newRole.name == "Robinhood Immune":
                await sql_insert("rhimmune", "users", uid)


def setup(bot):
    bot.add_cog(dbaddCog(bot))
