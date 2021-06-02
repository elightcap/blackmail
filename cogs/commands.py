

import discord
import requests
import os
import json
from typing import cast
from discord.ext import commands
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

class CommandsCog(commands.Cog, name="Commands"):
     def __init__(self, bot):
          self.bot = bot
          
     @commands.command(name='buyin')
     @commands.guild_only()
     async def buy_in(self, ctx, *, user_input: str):
          aID = ctx.author.id
          amount = int(user_input)
     ##i dont feel like doing rounding stuff and discord money doesnt support float
     ##so we dont let people buy 1 chip, since it will round to zero
          if amount <= 1:
               mes = "Must buy minimum 2 chips"
               send = await ctx.channel.send(mes)
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
               send = await ctx.channel.send(mes)
               return
          else:
               if amount > 200000:
                    mes = "The maximum amount the cashier allows is 200,000 chips"
                    send = await ctx.channel.send(mes)
               else:
                    print("buyin")
                    mes = "!pac {0.author.mention} {1}".format(ctx, amount)
                    send = await ctx.channel.send(mes)
                    nCost = '-' + str(int(cost))
                    builder = {'cash': nCost}
                    jsonString = json.dumps(builder, indent=4)
                    rp = requests.patch(url, headers=headers, data=jsonString)

     @commands.command(name='cashout')
     @commands.guild_only()
     async def cash_out(self, ctx, *, user_input: str):
          aID = ctx.author.id
          amount = int(user_input)
          url = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/{}".format(aID)
          mes = "!prc {0.author.mention} {1}".format(ctx, amount)
          send = await ctx.channel.send(mes)
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
                         send = await ctx.channel.send(mes)
          
     @commands.command(name='strike')
     @commands.guild_only()
     async def strike(self, ctx, *, user_input: str):
          roles = [y.name.lower() for y in ctx.author.roles]
          if "patent troll" in roles:
              aID = ctx.author.id
              loser = user_input
              if len(loser) < 1 :
                   mes = "choose somebody to copystrike"
                   send = await ctx.channel.send(mes)
                   return
              else:
                   print(loser)
                   print(ctx)
                   loser = int(loser.replace("<@!","").replace(">",""))
                   print(loser)
                   person = ctx.guild.get_member(loser)
                   print(person)
                   loserroles = [x.name.lower() for x in person.roles]
                   if "lawyer'd up" in loserroles:
                        mes = "{} has a good lawyer".format(person.mention)
                        print("good")
                        send = await ctx.channel.send(mes)
                        return
                   elif "public defender" in loserroles:
                        print("lawyer")
                        mes = "{} was barely able to afford a public defender".format(person.mention)
                        channel = self.bot.get_channel(849121833252159508)
                        send = await channel.send(mes)
                        pd = discord.utils.get(ctx.guild.roles, name="Public Defender")
                        await person.remove_roles(pd)
                   else:
                        print("strike")
                        url = "https://unbelievaboat.com/api/v1/guilds/267179220051034112/users/{}".format(loser)
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
                        channel = self.bot.get_channel(849121833252159508)
                        send = await channel.send(mes)
                   pt = discord.utils.get(ctx.guild.roles, name="Patent Troll")
                   await ctx.author.remove_roles(pt)

     @commands.command(name='robinhood')
     @commands.guild_only()
     async def robinhood(self,ctx):
          roles = [y.name.lower() for y in ctx.author.roles]
          if "little john" in roles:
               role = discord.utils.get(ctx.guild.roles, name="Merry People")
               members = [y.id for y in role.members]
               memberCount = len(members)
               if memberCount == 0:
                    print("no members")
                    return
               else:
                    url = "https://unbelievaboat.com/api/v1/guilds/267179220051034112/users/"
                    r = requests.get(url, headers=headers)
                    json_data = json.loads(r.text)
                    leader = next((item for item in json_data if item["rank"] == "1"), None)
                    leaderInfo = ctx.guild.get_member(int(leader['user_id']))
                    leaderRoles = [x.name.lower() for x in leaderInfo.roles]
                    if  "robinhood immune" in leaderRoles:
                         mes = "{} has outsmarted you! They are immune to my robbery".format(leaderInfo.mention)
                         send = await ctx.channel.send(mes)
                         lj = discord.utils.get(ctx.guild.roles, name="Little John")
                         await ctx.author.remove_roles(lj)
                    elif  "robbery victim" in leaderRoles:
                         mes = "I've already stolen from {}! lets give them a chance to learn their lesson".format(leaderInfo.mention)
                         send = await ctx.channel.send(mes)
                         lj = discord.utils.get(ctx.guild.roles, name="Little John")
                         await ctx.author.remove_roles(lj)
                    else:
                         leaderProfile = "https://unbelievaboat.com/api/v1/guilds/267179220051034112/users/{}".format(leader['user_id'])
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
                         send = await ctx.channel.send(mes)
                         lj = discord.utils.get(ctx.guild.roles, name="Little John")
                         rv = discord.utils.get(ctx.guild.roles, name="Robbery Victim")
                         await ctx.author.remove_roles(lj)
                         await leaderInfo.add_roles(rv)
                         await sql_insert("robbed", "users",leaderInfo.id)
                         for member in members:
                              memberProfile = ctx.guild.get_member(int(member))
                              url = "https://unbelievaboat.com/api/v1/guilds/267179220051034112/users/{}".format(member)
                              r = requests.get(url, headers=headers)
                              json_data = json.loads(r.text)
                              builder = {'cash': share}
                              jsonString = json.dumps(builder, indent=4)
                              rp = requests.patch(url, headers=headers, data=jsonString)

     @commands.command(name='nuke')
     @commands.guild_only()
     async def nuke(self, ctx, *, user_input : str):
          roles = [y.name.lower() for y in ctx.author.roles]
          print("nuke time")
          if  "usa! usa! usa!" in roles:
               print("has nuke role")
               hiroshima =  user_input
               if len(hiroshima) < 1:
                    mes = "choose a channel to nuke"
                    send = await ctx.channel.send(mes)
                    return
               nukeChannel = discord.utils.get(ctx.guild.channels, name=hiroshima)
               warning = "@everyone NORAD has detected a nuclear warhead! Take cover!"
               channel = self.bot.get_channel(849121833252159508)
               send = await channel.send(warning)
               i = 10
               while i >= 0:
                    mes = str(i)
                    send = await channel.send(mes)
                    time.sleep(1)
                    i -= 1

               try:
                    nukeChannel = discord.utils.get(ctx.guild.channels, name=hiroshima)
                    rows = sql_select("channels", "owners", "channelid", nukeChannel.id)
                    if rows:
                         for row in rows:
                              oId = int(row[0])
                              cID = int(row[1])
                              rID = int(row[2])
                              role = ctx.guild.get_role(rID)
                              print(role)
                              members = role.members
                              print(members)
                              for member in members:
                                   print(member)
                                   await member.remove_roles(role)
                                   mes = "Tactical nuke deployed! https://giphy.com/gifs/HhTXt43pk1I1W"
                                   send = await channel.send(mes)
                              usa = discord.utils.get(ctx.guild.roles, name="USA! USA! USA!")
                              await ctx.author.remove_roles(usa)
               except AttributeError:
                    mes = "{} has implemented a missle defense system. It seems flaky though...".format(hiroshima)
                    send = await channel.send(mes)
                    usa= discord.utils.get(ctx.guild.roles, name="USA! USA! USA!")
                    await ctx.author.remove_roles(usa)
               except:
                    mes = "You cant nuke a _SUPERPOWER_"
                    send = await channel.send(mes)
                    usa= discord.utils.get(ctx.guild.roles, name="USA! USA! USA!")
                    await ctx.author.remove_roles(usa)

def setup(bot):
    bot.add_cog(CommandsCog(bot))
