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
                         role = discord.utils.get(
                              member.guild.roles, name="Blackmailer")
                         await member.remove_roles(role)
                         print("{} removed from blackmailers".format(str(member)))



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
     elif "!strike" in case:
         roles = [y.name.lower() for y in message.author.roles]
         if "patent troll" in roles:
               aID = message.author.id
               loser = case.replace("!strike ","")
               loser = loser.replace("<@","").replace(">","")
               print(loser)
               loser2 = get_user(loser)


get_all_members_ids.start(GUILD)
client.run(TOKEN)
