from cogs.sqldel import sql_remove
import discord
import os
from typing import cast
from discord.ext import commands,tasks
from discord.utils import get
from dotenv import load_dotenv
from cogs.sqlget import sql_select
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
        self.remove_lawyer.start()
        self.remove_blackmail.start()
        self.remove_rhimmune.start()

    @tasks.loop(minutes=10)
    async def remove_rv(self):
        rows = await sql_select("robbed", "users", "uid","%")
        for row in rows:
             uUid = int(row[0])
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
                       if uTime <= newTime:
                            member = self.bot.get_user(uUid)
                            for guild in self.bot.guilds:
                                 for member in guild.members:
                                      for role in member.roles:
                                           if role.name == "Robbery Victim":
                                                role  = discord.utils.get(member.guild.roles, name="Robbery Victim")
                                                if member.id == uUid:
                                                     await sql_remove("robbed", "users", "uid", uUid)
                                                     print("rv role removed")
                                                     await member.remove_roles(role)
             except os.error as e:
                  print(e)

    @tasks.loop(minutes=1)
    async def remove_lawyer(self):
        rows = await sql_select("lawyer", "users", "uid","%")
        for row in rows:
             uUid = int(row[0])
             uDate = row[1]
             strTime = str(row[2])
             uTime = datetime.strptime(strTime,"%H:%M:%S" ).time()
             try:
                  datetimenow = datetime.now()
                  addTime = timedelta(minutes=1)
                  addDays = timedelta(days=2)
                  dateNowStr = datetimenow.strftime("%Y-%m-%d")
                  timeNowStr = datetimenow.strftime("%H:%M:%S")
                  mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                  mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                  newTime = (mTime - addTime).time()
                  newDate = (mDate - addDays)
                  if uDate <= mDate:
                       if uTime <= newTime:
                            member = self.bot.get_user(uUid)
                            for guild in self.bot.guilds:
                                 for member in guild.members:
                                      for role in member.roles:
                                           if role.name == "Lawyer'd Up":
                                                role  = discord.utils.get(member.guild.roles, name="Lawyer'd Up")
                                                if member.id == uUid:
                                                     await sql_remove("lawyer", "users", "uid", uUid)
                                                     print("lawyer role removed")
                                                     await member.remove_roles(role)
             except os.error as e:
                  print(e)

    @tasks.loop(minutes=1)
    async def remove_blackmail(self):
        rows = await sql_select("blackmailer", "users", "uid","%")
        for row in rows:
             uUid = int(row[0])
             uDate = row[1]
             strTime = str(row[2])
             uTime = datetime.strptime(strTime,"%H:%M:%S" ).time()
             try:
                  datetimenow = datetime.now()
                  addTime = timedelta(hours=2)
                  dateNowStr = datetimenow.strftime("%Y-%m-%d")
                  timeNowStr = datetimenow.strftime("%H:%M:%S")
                  mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                  mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                  newTime = (mTime - addTime).time()
                  if uDate <= mDate:
                       if uTime <= newTime:
                            member = self.bot.get_user(uUid)
                            for guild in self.bot.guilds:
                                 for member in guild.members:
                                      for role in member.roles:
                                           if role.name == "Blackmailer":
                                                role  = discord.utils.get(member.guild.roles, name="Blackmailer")
                                                if member.id == uUid:
                                                     await sql_remove("blackmailer", "users", "uid", uUid)
                                                     print("blackmail role removed")
                                                     await member.remove_roles(role)
             except os.error as e:
                  print(e)

    @tasks.loop(minutes=1)
    async def remove_rhimmune(self):
          rows = await sql_select("rhimmune", "users", "uid","%")
          for row in rows:
               uUid = int(row[0])
               uDate = row[1]
               strTime = str(row[2])
               uTime = datetime.strptime(strTime,"%H:%M:%S" ).time()
               try:
                    datetimenow = datetime.now()
                    addTime = timedelta(hours=2)
                    dateNowStr = datetimenow.strftime("%Y-%m-%d")
                    timeNowStr = datetimenow.strftime("%H:%M:%S")
                    mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                    mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                    newTime = (mTime - addTime).time()
                    if uDate <= mDate:
                         if uTime <= newTime:
                              member = self.bot.get_user(uUid)
                              for guild in self.bot.guilds:
                                   for member in guild.members:
                                        for role in member.roles:
                                             if role.name == "Robinhood Immune":
                                                  role  = discord.utils.get(member.guild.roles, name="Robinhood Immune")
                                                  if member.id == uUid:
                                                       await sql_remove("rhimmune", "users", "uid", uUid)
                                                       print("immune role removed")
                                                       await member.remove_roles(role)
               except os.error as e:
                    print(e)

def setup(bot):
    bot.add_cog(dbCog(bot))
