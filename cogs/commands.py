

import discord
import requests
import os
import json
import time
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
                   loser = int(loser.replace("<@!","").replace(">",""))
                   person = ctx.guild.get_member(loser)
                   loserroles = [x.name.lower() for x in person.roles]
                   if "lawyer'd up" in loserroles:
                        mes = "{} has a good lawyer".format(person.mention)
                        send = await ctx.channel.send(mes)
                        return
                   elif "public defender" in loserroles:
                        mes = "{} was barely able to afford a public defender".format(person.mention)
                        channel = self.bot.get_channel(831400394184851456)
                        send = await channel.send(mes)
                        pd = discord.utils.get(ctx.guild.roles, name="Public Defender")
                        await person.remove_roles(pd)
                   else:
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
                        channel = self.bot.get_channel(831400394184851456)
                        send = await channel.send(mes)
                   pt = discord.utils.get(ctx.guild.roles, name="Patent Troll")
                   await ctx.author.remove_roles(pt)
          else:
               mes = "You don't have the legal prowess to copy strike"
               send = await ctx.channel.send(mes)

     @commands.command(name='robinhood')
     @commands.guild_only()
     async def robinhood(self,ctx):
          roles = [y.name.lower() for y in ctx.author.roles]
          if "little john" in roles:
               role = discord.utils.get(ctx.guild.roles, name="Merry People")
               members = [y.id for y in role.members]
               memberCount = len(members)
               if memberCount == 0:
                    mes = "My merry gang has no members!"
                    send = await ctx.channel.send(mes)
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
          else:
               mes= "Little John role required"
               send = await ctx.channel.send(mes)

     @commands.command(name='nuke')
     @commands.guild_only()
     async def nuke(self, ctx, *, user_input : str):
          roles = [y.name.lower() for y in ctx.author.roles]
          if  "usa! usa! usa!" in roles:
               hiroshima =  user_input
               if len(hiroshima) < 1:
                    mes = "choose a channel to nuke"
                    send = await ctx.channel.send(mes)
                    return
               nukeChannel = discord.utils.get(ctx.guild.channels, name=hiroshima)
               warning = "@everyone NORAD has detected a nuclear warhead! Take cover!"
               channel = self.bot.get_channel(831400394184851456)
               send = await channel.send(warning)
               i = 10
               while i >= 0:
                    mes = str(i)
                    send = await channel.send(mes)
                    time.sleep(1)
                    i -= 1

               try:
                    nukeChannel = discord.utils.get(ctx.guild.channels, name=hiroshima)
                    rows = await sql_select("channels", "owners", "channelid", nukeChannel.id)
                    if rows:
                         for row in rows:
                              oID = int(row[0])
                              cID = int(row[1])
                              rID = int(row[2])
                              role = ctx.guild.get_role(rID)
                              owner = ctx.guild.get_member(int(oID))
                              members = role.members
                              for member in members:
                                   await member.remove_roles(role)
                              hd = discord.utils.get(ctx.guild.roles, name="Home Destroyed")
                              await owner.add_roles(hd)
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
          else:
               mes = "No nukes left in your arsenal"
               send = await ctx.channel.send(mes)

     @commands.command(name='build')
     @commands.guild_only()
     async def channel_create(self, ctx, *, user_input : str):
          roles = [y.name.lower() for y in ctx.author.roles]
          if "home builder" in roles:
               aID = ctx.author.id
               channelName = user_input
               cat = discord.utils.get(ctx.guild.categories, name="Degen City")
               await ctx.guild.create_role(name=channelName)
               channelName=channelName.replace(" ", "-")
               role = discord.utils.get(ctx.guild.roles, name=channelName)
               await ctx.author.add_roles(role)
               overwrites = {
                    role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
               }
               await ctx.guild.create_text_channel(channelName, overwrites=overwrites, category=cat)
               newChannel = discord.utils.get(ctx.guild.channels, name=channelName)
               await sql_insert("channels", "owners", aID, newChannel.id, role.id)
               ownerRole = discord.utils.get(ctx.guild.roles, name="Home Builder")
               await ctx.author.remove_roles(ownerRole)
          else:
               mes = "Youre too clumsy to try to build your own home"
               send = await ctx.channel.send(mes)

     @commands.command(name='invite')
     @commands.guild_only()
     async def channel_invite(self, ctx, *, user_input : str):
          roles = [y.name.lower() for y in ctx.author.roles]
          if "home destroyed" in roles:
               mes = "You need to rebuild your home before anyone bothers visting"
               send = await ctx.channel.send(mes)
               return
          elif "home owner" in roles:
               aID = ctx.author.id
               rows = await sql_select("channels", "owners", "owner", aID)
               invited = user_input
               inviteID = int(invited.replace("<@!","").replace(">",""))
               member = ctx.guild.get_member(inviteID)
               if rows:
                    for row in rows:
                         oID = int(row[0])
                         cID = int(row[1])
                         rID = int(row[2])
                         if aID == oID:
                              role = ctx.guild.get_role(rID)
                              await member.add_roles(role)
          else:
               mes = "Where are you inviting people? the dumpster behind Chipotle?"
               send = await ctx.channel.send(mes)

     @commands.command(name='privatize')
     @commands.guild_only()
     async def private_channel(self, ctx):
          roles = [y.name.lower() for y in ctx.author.roles]
          if "home owner" in roles:
               aID = ctx.author.id
               rows = await sql_select("channels","owners","owner",aID)
               if rows:
                    for row in rows:
                         oID = int(row[0])
                         cID = int(row[1])
                         rID = int(row[2])
                         if aID == oID:
                              channel =  self.bot.get_channel(cID)
                              await channel.set_permissions(ctx.guild.default_role, read_messages=False)
                              await channel.set_permissions(ctx.guild.me, read_messages=True)
          else:
               mes = "you cant make the dumpster behind Chipotle private"
               send = await ctx.channel.send(mes)
     
     @commands.command(name='kick')
     @commands.guild_only()
     async def remove_member(self,ctx,*,user_input : str):
          aID = ctx.author.id
          roles = [y.name.lower() for y in ctx.author.roles]
          if "home owner" in roles:
               rows = await sql_select("channels", "owners","owner", aID)
               if rows:
                    for row in rows:
                              oID = int(row[0])
                              cID = int(row[1])
                              rID = int(row[2])
                              if aID == oID:
                                   remove = user_input
                                   removeID = int(remove.replace("<@!","").replace(">",""))
                                   removeObj = ctx.guild.get_member(removeID)
                                   username = removeObj.name
                                   role = ctx.guild.get_role(rID)
                                   await removeObj.remove_roles(role)
                                   mes = "{} has been evicted!".format(username)
                                   send = await ctx.channel.send(mes)
          else:
               mes = "And you cant kick the other bums out of the dumpster behind Chipotle!"
               send = await ctx.channel.send(mes)

     @commands.command(name='rename')
     @commands.guild_only()
     async def rename_channel(self, ctx, *, user_input : str):
          roles = [y.name.lower() for y in ctx.author.roles]
          if "renovator" in roles:
               aID = ctx.author.id
               newName = user_input
               rows = await sql_select("channels", "owners", "owner", aID)
               if rows:
                    for row in rows:
                         oID = int(row[0])
                         cID = int(row[1])
                         rID = int(row[2])
                         if aID == oID:
                              channel = self.bot.get_channel(cID)
                              await channel.edit(name=newName)
                              ren = discord.utils.get(ctx.guild.roles, name="Renovator")
                              await ctx.author.remove_roles(ren)
          else:
               mes = "Looks like you forgot to pay the town building fees"
               send = await ctx.channel.send(mes)


def setup(bot):
    bot.add_cog(CommandsCog(bot))
