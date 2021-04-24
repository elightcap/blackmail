import os
import requests
import discord
import json
import math
from discord.ext import tasks, commands
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


@client.event
async def on_message(message):
     if message.author == client.user:
        return
     msg = message.content
     case = msg.lower()
     if "!buyin" in case:
          aID = message.author.id
          sAmount = case.replace("!buyin ", "")
          amount = int(sAmount)
          if amount <= 1:
               mes = "Must buy minimum 2 chips"
               send = await message.channel.send(mes)
               return
          url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(aID)
          r = requests.get(url, headers=headers)
          json_data = json.loads(r.text)
          strMoney = json_data['cash']
          uMoney = int(strMoney)
          cost = amount//2
          if uMoney < cost:
               print("broke bitch")
               mes = "Not enough money. Loser."
               send = await message.channel.send(mes)
               return
          else:
               print("buyin")
               mes = "!pac {0.author.mention} {1}".format(message, amount)
               send = await message.channel.send(mes)
               nCost = '-' + str(cost)
               builder = {'cash': nCost}
               jsonString = json.dumps(builder, indent=4)
               rp = requests.patch(url, headers=headers, data=jsonString)
               print(jsonString)

     if "!cashout" in case:
          aID = message.author.id
          sAmount = case.replace("!cashout ", "")
          amount = int(sAmount)
          url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(aID)
          mes = "!prc {0.author.mention} {1}".format(message, sAmount)
          send = await message.channel.send(mes)

          @client.event
          async def on_raw_message_edit(edit):
               msgData = edit.data
               editID = str(msgData['author']['id'])
               print(pokerBotID)
               print(editID)
               print(edit.data)
               return editID == pokerBotID
               if editID == pokerBotID:
                    #print(edit.data)
                    #print(editID)
                    #for key in edit.keys():
                    #     print(key)
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

                    else:
                         print("user doesnt have chips")
                         mes = "ya broke"
                         send = await message.channel.send(mes)
     #print(case)
     #if message.author.id == 613156357239078913 and "done!" in case:
     #     print("users got the chips")
     #     payout = str((amount//2s)*.9)
     #     rake = str((amount//2)*.1)
     #     payBuilder = {'cash': payout}
     #     rakeBuilder = {'bank': rake}
     #     payJson = json.dumps(payBuilder, indent=4)
     #     rakeJson = json.dumps(rakeBuilder, indent=4)
     #     rp = requests.patch(url, headers=headers, data=payJson)
     #     rr = requests.patch(botUrl, headers=headers, data=rakeJson)
     #     


get_all_members_ids.start(GUILD)
client.run(TOKEN)
