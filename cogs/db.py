from cogs.sqldel import sql_remove
import discord
import requests
import os
import json
from typing import cast
from discord.ext import commands,tasks
from discord.utils import get
from dotenv import load_dotenv
from cogs.sqlget import sql_select
from cogs.sqladd import sql_insert
from cogs.sqldel import sql_remove
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

class dbCog(commands.Cog, name="db"):
    def __init__(self, bot):
        self.bot = bot
        self.remove_rv.start()

    @tasks.loop(minutes=1)
    async def remove_rv(self):
        rows = await sql_select("robbed", "users", "uid","%")
        for row in rows:
             uUid = int(row[0])
             print(uUid)
             uDate = row[1]
             strTime = str(row[2])
             uTime = datetime.strptime(strTime,"%H:%M:%S" ).time()
             try:
                  datetimenow = datetime.now()
                  addTime = timedelta(minutes=1)
                  dateNowStr = datetimenow.strftime("%Y-%m-%d")
                  timeNowStr = datetimenow.strftime("%H:%M:%S")
                  mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                  mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                  newTime = (mTime - addTime).time()
                  if uDate <= mDate:
                       print("date")
                       if uTime <= newTime:
                            print("time")
                            member = self.bot.get_user(uUid)
                            print(member)
                            for guild in self.bot.guilds:
                                 for member in guild.members:
                                      for role in member.roles:
                                           if role.name == "Robbery Victim":
                                                print("role")
                                                role  = discord.utils.get(member.guild.roles, name="Robbery Victim")
                                                if member.id == uUid:
                                                     await sql_remove("robbed", "users", "uid", uUid)
                                                     print("blackmail role removed")
                                                     await member.remove_roles(role)
             except os.error as e:
                  print(e)

def setup(bot):
    bot.add_cog(dbCog(bot))