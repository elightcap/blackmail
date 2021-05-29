## TODO ##
## Stop looking at the entire raw messge edit as a string. probably inefficient.
## can break the json that is returned down and just look for a specific value. 
## but i was debugging on my phone and that was hard to do.  maybe tomorrow
##
##
import os
from typing import cast

from requests.models import CaseInsensitiveDict
import aiocron
import requests
import discord
import json
import math
import mysql.connector as database
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
unbkey = os.getenv('UNBKEY')
dbUser = os.getenv('MARIAUSER')
dbPass = os.getenv('MARIAPASS')
pokerBotID = "613156357239078913"
botUrl = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/613156357239078913"
client = discord.Client()
Blackmail_role_name = "Blackmailer"
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)
headers = {'Authorization': unbkey}

##on message events
@client.event
async def on_message(message):
     if message.author == client.user:
        return
     msg = message.content
     case = msg.lower()
     ##buyin to turn discord money to poker chips at a rate of $1:2 chips
     if "!buyin" in case:
          aID = message.author.id
          sAmount = case.replace("!buyin ", "")
          amount = int(sAmount)

          ##i dont feel like doing rounding stuff and discord money doesnt support float
          ##so we dont let people buy 1 chip, since it will round to zero
          if amount <= 1:
               mes = "Must buy minimum 2 chips"
               send = await message.channel.send(mes)
               return

          url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(aID)
          r = requests.get(url, headers=headers)
          json_data = json.loads(r.text)
          strMoney = json_data['cash']
          uMoney = float(strMoney)
          cost = float(amount//2.00)
          if uMoney < cost:
               print("broke bitch")
               mes = "Not enough money. Loser."
               send = await message.channel.send(mes)
               return
          else:
               if amount > 200000:
                    mes = "The maximum amount the cashier allows is 200,000 chips"
                    send = await message.channel.send(mes)
               else:
                    print("buyin")
                    mes = "!pac {0.author.mention} {1}".format(message, amount)
                    send = await message.channel.send(mes)
                    nCost = '-' + str(int(cost))
                    builder = {'cash': nCost}
                    jsonString = json.dumps(builder, indent=4)
                    rp = requests.patch(url, headers=headers, data=jsonString)

     ##cashout function to turn chips into discord money at a rate of $1:2 chips.
     ##dealer takes a 10% rake in discord money, which is given to poker bot for use someday
     if "!cashout" in case:
          aID = message.author.id
          sAmount = case.replace("!cashout ", "")
          amount = int(sAmount)
          url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(aID)
          mes = "!prc {0.author.mention} {1}".format(message, sAmount)
          send = await message.channel.send(mes)

          ##since poker bot actually sends a blank message and edits it, we need to trigger
          ##an event on edit. through this part we are filtering messages from users that
          #are not poker bot, or messages that are from poker bot that we dont want to do 
          ##shit with
          @client.event
          async def on_raw_message_edit(edit):
               msgData = edit.data
               editID = str(msgData['author']['id'])
               ##making sure the editor is poker bot
               if editID == pokerBotID:
                    #print("in for loop")
                    if "done! I removed" in str(edit):
                         print("user has chips")
                         payout = str((amount//2)*.9)
                         rake = str((amount//2)*.1)
                         payBuilder = {'cash': payout}
                         rakeBuilder = {'bank': rake}
                         payJson = json.dumps(payBuilder, indent=4)
                         rakeJson = json.dumps(rakeBuilder, indent=4)
                         rp = requests.patch(url, headers=headers, data=payJson)
                         rr = requests.patch(botUrl, headers=headers, data=rakeJson)

                    elif "this user only has" in str(edit):
                         print("user doesnt have chips")
                         mes = "ya broke"
                         send = await message.channel.send(mes)
     ###strike function to remove 30% of money from targeted user.
     ###person calling must have the "Patent Troll" role, and
     ###will fail if the target has either of the lawyer roles
     elif "!strike" in case:
         roles = [y.name.lower() for y in message.author.roles]
         if "patent troll" in roles:
               aID = message.author.id
               loser = case.replace("!strike ","")
               if len(loser) < 8 :
                    mes = "choose somebody to copystrike"
                    send = await message.channel.send(mes)
                    return
               else:
                    loser = int(loser.replace("<@!","").replace(">",""))
                    person = message.guild.get_member(loser)
                    loserroles = [x.name.lower() for x in person.roles]
                    if "lawyer'd up" in loserroles:
                         mes = "{} has a good lawyer".format(person.mention)
                         send = await message.channel.send(mes)
                         return
                    elif "public defender" in loserroles:
                         mes = "{} was barely able to afford a public defender".format(person.mention)
                         channel = client.get_channel(831400394184851456)
                         send = await channel.send(mes)
                         pd = discord.utils.get(message.guild.roles, name="Public Defender")
                         await person.remove_roles(pd)
                    else:
                         url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(loser)
                         r = requests.get(url, headers=headers)
                         json_data = json.loads(r.text)
                         strCash = json_data['cash']
                         strBank = json_data['bank']
                         uCash = float(strCash)
                         uBank = float(strBank)
                         percentCash = float(uCash*.3)
                         percentBank = float(uBank*.3)
                         feeCash = '-' + str(int(percentCash))
                         feeBank = '-' + str(int(percentBank))
                         builder = {'cash': feeCash, 'bank':feeBank}
                         total = str(int(percentBank + percentCash))
                         jsonString = json.dumps(builder, indent=4)
                         rp = requests.patch(url, headers=headers, data=jsonString)
                         mes = "{} lost {} because they were too cheap to pay their legal fees".format(person.mention,total)
                         channel = client.get_channel(831400394184851456)
                         send = await channel.send(mes)
                    pt = discord.utils.get(message.guild.roles, name="Patent Troll")
                    await message.author.remove_roles(pt)
     ###function that will remove
     ###10% of casdh leaders total
     ###money and distributes it
     ###evenly to everyone with the merry
     ###people role
     elif "!robinhood" in case:
          roles = [y.name.lower() for y in message.author.roles]
          if "little john" in roles:
               role = discord.utils.get(message.guild.roles, name="Merry People")
               members = [y.id for y in role.members]
               memberCount = len(members)
               if memberCount == 0:
                    print("no members")
                    return
               else:
                    url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/"
                    r = requests.get(url, headers=headers)
                    json_data = json.loads(r.text)
                    leader = next((item for item in json_data if item["rank"] == "1"), None)
                    leaderInfo = message.guild.get_member(int(leader['user_id']))
                    leaderRoles = [x.name.lower() for x in leaderInfo.roles]
                    if  "robinhood immune" in leaderRoles:
                         mes = "{} has outsmarted you! They are immune to my robbery".format(leaderInfo.mention)
                         send = await message.channel.send(mes)
                    elif  "robbery victim" in leaderRoles:
                         mes = "I've already stolen from {}! lets give them a chance to learn their lesson".format(leaderInfo.mention)
                         send = await message.channel.send(mes)
                    else:
                         leaderProfile = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(leader['user_id'])
                         r = requests.get(leaderProfile, headers=headers)
                         json_data = json.loads(r.text)
                         leaderCash = float(json_data['cash'])
                         leaderBank = float(json_data['bank'])
                         percentCash = float(leaderCash*.1)
                         percentBank = float(leaderBank*.1)
                         total = float(percentBank+percentCash)
                         share = str(float(total//memberCount))
                         feeCash = '-' + str(int(percentCash))
                         feeBank = '-' + str(int(percentBank))
                         builder = {'cash': feeCash, 'bank':feeBank}
                         total = str(int(percentBank + percentCash))
                         jsonString = json.dumps(builder, indent=4)
                         rp = requests.patch(leaderProfile, headers=headers, data=jsonString)
                         mes = "I steal from the rich and give to the needy! My name is Robinhood and i am very greedy! I took {} from {} to distribute amongst my Merry People.".format(total, leaderInfo.mention)
                         send = await message.channel.send(mes)
                         lj = discord.utils.get(message.guild.roles, name="Little John")
                         await message.author.remove_roles(lj)
                         for member in members:
                              memberProfile = message.guild.get_member(int(member))
                              url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(member)
                              r = requests.get(url, headers=headers)
                              json_data = json.loads(r.text)
                              builder = {'cash': share}
                              jsonString = json.dumps(builder, indent=4)
                              rp = requests.patch(url, headers=headers, data=jsonString)
          else:
               return

     elif "!nuke" in case:
          roles = [y.name.lower() for y in message.author.roles]
          if  "usausausa" in roles:
               hiroshima =  case.replace("!nuke ","")
               if len(hiroshima) < 3:
                    mes = "choose a channel to nuke"
                    send = await message.channel.send(mes)
                    return
               nukeChannel = discord.utils.get(message.guild.channels, name=hiroshima)
               i = 10
               while i >= 0:
                    mes = str(i)
                    send = await message.channel.send(mes)
                    i -= 1
               try:
                    await nukeChannel.delete()
               except:
                    mes = "{} has implemented a missle defense system! it seems pretty flaky though...".format(hiroshima)



@client.event
async def on_member_update(before,after):
     if len(before.roles)<len(after.roles):
          newRole = next(role for role in after.roles if role not in before.roles)

          if newRole.name == "Robbery Victim":
               connection = database.connect(
                    user = dbUser,
                    password = dbPass,
                    host='localhost',
                    db='robbed'
               )
               cursor = connection.cursor(buffered=True)
               datetimenow = datetime.now()
               mDate = datetimenow.strftime("%Y-%m-%d")
               mTime = datetimenow.strftime("%H:%M:%S")
               user = int(after.id)
               try:
                    statement = "INSERT INTO users (uid,date,time) VALUES (%s, %s, %s)"
                    data = (user,mDate,mTime)
                    cursor.execute(statement,data)
                    connection.commit()
                    print("rob vic success add")
               except database.Error as e:
                    print(f"update {e}")

          elif newRole.name == "Blackmailer":
               connection = database.connect(
                    user = dbUser,
                    password = dbPass,
                    host='localhost',
                    db='blackmailer'
            )
               cursor = connection.cursor(buffered=True)
               datetimenow = datetime.now()
               mDate = datetimenow.strftime("%Y-%m-%d")
               mTime = datetimenow.strftime("%H:%M:%S")
               user = int(after.id)
               try:
                    statement = "INSERT INTO users (uid,date,time) VALUES (%s, %s, %s)"
                    data = (user,mDate,mTime)
                    cursor.execute(statement,data)
                    connection.commit()
                    print("blackmail success add")
               except database.Error as e:
                    print(f"update {e}")
          elif newRole.name == "Lawyer'd Up":
               connection = database.connect(
                    user = dbUser,
                    password = dbPass,
                    host='localhost',
                    db='lawyer'
               )
               cursor = connection.cursor(buffered=True)
               datetimenow = datetime.now()
               mDate = datetimenow.strftime("%Y-%m-%d")
               mTime = datetimenow.strftime("%H:%M:%S")
               user = int(after.id)
               try:
                    statement = "INSERT INTO users (uid,date,time) VALUES (%s, %s, %s)"
                    data = (user,mDate,mTime)
                    cursor.execute(statement,data)
                    connection.commit()
                    print(" lawyer success add")
               except database.Error as e:
                    print(f"update {e}")

@aiocron.crontab('*/1 * * * *')
async def remove_robberyvictim():
     try:
          connection = database.connect(
               user = dbUser,
               password = dbPass,
               host='localhost',
               db='robbed'
          )
          cursor = connection.cursor(buffered=True)
          getUser = "SELECT * from users;"
          cursor.execute(getUser)
          rows = cursor.fetchall()
          if rows:
               for row in rows:
                    uUid = int(row[0])
                    uDate = row[1]
                    strTime = str(row[2])
                    uTime = datetime.strptime(strTime,"%H:%M:%S" ).time()
                    try:
                         datetimenow = datetime.now()
                         addTime = timedelta(minutes=5)
                         dateNowStr = datetimenow.strftime("%Y-%m-%d")
                         timeNowStr = datetimenow.strftime("%H:%M:%S")
                         mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                         mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                         newTime = (mTime - addTime).time()
                         if uDate <= mDate:
                              if uTime <= newTime:
                                   member = client.get_user(uUid)
                                   for guild in client.guilds:
                                        for member in guild.members:
                                             for role in member.roles:
                                                  if role.name == "Robbery Victim":
                                                       role  = discord.utils.get(member.guild.roles, name="Robbery Victim")
                                                       if member.id == uUid:
                                                            await member.remove_roles(role)
                                                            remove = "DELETE FROM `users` WHERE uid = (%s)"
                                                            data = (uUid,)
                                                            cursor.execute(remove, data)
                                                            connection.commit()
                                                            print("robvic role removed")
                    except os.error as e:
                         print(e)

     except database.Error as e:
          print(f" remove {e}")

@aiocron.crontab('*/1 * * * *')
async def remove_lawyer():
     try:
          connection = database.connect(
                user = dbUser,
                password = dbPass,
                host='localhost',
                db='lawyer'
          )
          cursor = connection.cursor(buffered=True)
          getUser = "SELECT * from users;"
          cursor.execute(getUser)
          rows = cursor.fetchall()
          if rows:
               for row in rows:
                    uUid = int(row[0])
                    uDate = row[1]
                    strTime = str(row[2])
                    uTime = datetime.strptime(strTime,"%H:%M:%S" ).time()
                    try:
                         datetimenow = datetime.now()
                         addTime = timedelta(minutes=5)
                         addDays = timedelta(days=7)
                         dateNowStr = datetimenow.strftime("%Y-%m-%d")
                         timeNowStr = datetimenow.strftime("%H:%M:%S")
                         mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                         newDate = (mDate - addDays).time()
                         mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                         newTime = (mTime - addTime).time()
                         if uDate <= newTime:
                              if uTime <= newTime:
                                   member = client.get_user(uUid)
                                   for guild in client.guilds:
                                        for member in guild.members:
                                             for role in member.roles:
                                                  if role.name == "Lawyer'd Up":
                                                       role  = discord.utils.get(member.guild.roles, name="Lawyere'd Up")
                                                       if member.id == uUid:
                                                            await member.remove_roles(role)
                                                            remove = "DELETE FROM `users` WHERE uid = (%s)"
                                                            data = (uUid,)
                                                            cursor.execute(remove, data)
                                                            connection.commit()
                                                            print("lawyer role removed")
                    except os.error as e:
                         print(e)
     except database.Error as e:
          print(f" remove {e}")

@aiocron.crontab('*/1 * * * *')
async def remove_blackmail():
    try:
          connection = database.connect(
               user = dbUser,
               password = dbPass,
               host='localhost',
               db='blackmailer'
          )
          cursor = connection.cursor(buffered=True)
          getUser = "SELECT * from users;"
          cursor.execute(getUser)
          rows = cursor.fetchall()
          if rows:
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
                                   member = client.get_user(uUid)
                                   for guild in client.guilds:
                                        for member in guild.members:
                                             for role in member.roles:
                                                  if role.name == "Blackmailer":
                                                       role  = discord.utils.get(member.guild.roles, name="Blackmailer")
                                                       if member.id == uUid:
                                                            await member.remove_roles(role)
                                                            remove = "DELETE FROM `users` WHERE uid = (%s)"
                                                            data = (uUid,)
                                                            cursor.execute(remove, data)
                                                            connection.commit()
                                                            print("blackmail role removed")
                    except os.error as e:
                         print(e)
    except database.Error as e:
        print(f" remove {e}")

remove_robberyvictim.start()
remove_lawyer.start()
remove_blackmail.start()
client.run(TOKEN)
