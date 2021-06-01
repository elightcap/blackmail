import discord
import requests
import os
import json
from typing import cast
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv


load_dotenv()
client = discord.Client()
headers = {'Authorization': unbkey}
pokerBotID = "613156357239078913"
botUrl = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/613156357239078913"

class NukeCog(commands.Cog, name="Nuke"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='nuke')
    @commands.guild_only()
    async def do_nuke(self, ctx, *, our_input: str):
        await ctx.send(our_input)

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
async def strike(self, ctx, *, user_input):
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
                  channel = client.get_channel(849121833252159508)
                  send = await channel.send(mes)
                  pd = discord.utils.get(ctx.guild.roles, name="Public Defender")
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
                  channel = client.get_channel(849121833252159508)
                  send = await channel.send(mes)
             pt = discord.utils.get(ctx.guild.roles, name="Patent Troll")
             await ctx.author.remove_roles(pt)


def setup(bot):
    bot.add_cog(NukeCog(bot))