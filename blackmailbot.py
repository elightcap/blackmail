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
pokerBotID = "@Poker Now Bot#8842"
botUrl = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/botid"
client = discord.Client()
Blackmail_role_name = "Blackmailer"
intents = discord.Intents.default()
intents.members = True
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
     #if message.author == client.user:
     #   return
     msg = message.content
     case = msg.lower()
     if "!buyin" in case:
          aID = message.author.id
          sAmount = case.replace("!buyin ", "")
          amount = int(sAmount)
          url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(aID)
          r = requests.get(url, headers=headers)
          json_data = json.loads(r.text)
          print(json_data)
          strMoney = json_data['cash']
          uMoney = int(strMoney)
          cost = amount//3
          if uMoney < cost:
               mes = "Not enough money. Loser."
               send = await message.channel.send(mes)
               return
          else:
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
          print(message.author)

          #@client.event
          #async def on_message(message):
          #     print(message)
          #     def check(m):
          #          return message.mentions[0] == pokerBotID
          #
          #     message = await client.wait_for('message', check=check)
          #     if "done!" in message.content:
          #          print("user has chips")
          #          payout = str(amount*3)
          #          builder = {'cash': payout}
          #          jsonString = json.dumps(builder, indent=4)
          #          rp = requests.patch(url, headers=headers, data=jsonString)
          #
          #     else:
          #          print("user doesnt have chips")
          #          mes = "ya broke"
          #          await message.channel.send(mes)

     if message.id.author == pokerBotID and "done!" in case:
          print("users got the chips")
          payout = str((amount//3)*.9)
          rake = str((amount//3)*.1)
          payBuilder = {'cash': payout}
          rakeBuilder = {'bank': rake}
          payJson = json.dumps(payBuilder, indent=4)
          rakeJson = json.dumps(rakeBuilder, indent=4)
          rp = requests.patch(url, headers=headers, data=payJson)
          rr = requests.patch(botUrl, headers=headers, data=rakeJson)
          


get_all_members_ids.start(GUILD)
client.run(TOKEN)
