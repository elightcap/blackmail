## TODO ##
## Stop looking at the entire raw messge edit as a string. probably inefficient.
## can break the json that is returned down and just look for a specific value. 
## but i was debugging on my phone and that was hard to do.  maybe tomorrow
##
##
import os
import requests
import discord
import json
import math
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
unbkey = os.getenv('UNBKEY')
pokerBotID = "613156357239078913"
botUrl = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/613156357239078913"
client = discord.Client()
Blackmail_role_name = "Blackmailer"
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)
headers = {'Authorization': unbkey}


##function to loop through all members 
##and if they have the black ailer role, remove it
## runs every 2 hours
@tasks.loop(minutes=120)
async def get_all_members_ids(discguild):
     for guild in client.guilds:
          for member in guild.members:
            for role in member.roles:
                    if role.name == "Blackmailer":
                         role = discord.utils.get(member.guild.roles, name="Blackmailer")
                         await member.remove_roles(role)
                         print("{} removed from blackmailers".format(str(member)))

@tasks.loop(hours=168)
async def remove_lawyer(discguild):
     for guild in client.guilds:
          for member in guild.members:
               for role in member.roles:
                    if role.name == "Lawyer'd Up":
                         role = discord.utils.get(member.guild.roles, name="Lawyer'd Up")
                         await member.remove_roles(role)



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
               print("buyin")
               mes = "!pac {0.author.mention} {1}".format(message, amount)
               send = await message.channel.send(mes)
               nCost = '-' + str(int(cost))
               builder = {'cash': nCost}
               jsonString = json.dumps(builder, indent=4)
               rp = requests.patch(url, headers=headers, data=jsonString)
               print(jsonString)

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
               print(pokerBotID)
               print(editID)
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
               print(loser)
               if len(loser) < 8 :
                    mes = "choose somebody to copystrike"
                    send = await message.channel.send(mes)
                    return
               else:
                    loser = int(loser.replace("<@!","").replace(">",""))
                    person = message.guild.get_member(loser)
                    loserroles = [x.name.lower() for x in person.roles]
                    print(loserroles)
                    if "lawyer'd up" in loserroles:
                         mes = "{} has a good lawyer".format(person.mention)
                         send = await message.channel.send(mes)
                         return
                    elif "public defender" in loserroles:
                         mes = "{} was barely able to afford a public defender".format(person.mention)
                         send = await message.channel.send(mes)
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
                         send = await message.channel.send(mes)
                    pt = discord.utils.get(message.guild.roles, name="Patent Troll")
                    await message.author.remove_roles(pt)
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
                    leaderInfo = message.guild.get_member(leader['user_id'])
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
                    for member in members:
                         url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(member)
                         r = requests.get(url, headers=headers)
                         json_data = json.loads(r.text)
                         builder = {'cash': share}
                         jsonString = json.dumps(builder, indent=4)
                         rp = requests.patch(url, headers=headers, data=jsonString)
          else:
               return
          




get_all_members_ids.start(GUILD)
client.run(TOKEN)
