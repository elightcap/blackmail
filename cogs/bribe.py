import discord
import os
from typing import cast
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import re
import time

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)
unbkey = os.getenv('UNBKEY')
headers = {'Authorization': unbkey}
pokerBotID = "613156357239078913"
botUrl = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/613156357239078913"

class BribeCog(commands.Cog, name="Bribe"):
     def __init__(self, bot):
          self.bot = bot
     
     @commands.command(name='pokerbribe')
     @commands.guild_only()
     async def give_bribe(self, ctx, *, user_input: str):
          roles = [y.name.lower() for y in ctx.author.roles]
          #if "poker bribe" in roles:
          target = user_input
          targetID = int(target.replace("<@!","").replace(">",""))
          member = ctx.guild.get_member(targetID)
          pw = "!pw {}".format(member.mention)
          send = await ctx.channel.send(pw)
          print(send.id)
          msg = await ctx.channel.fetch_message(send.id)
          @commands.Cog.listener()
          async def on_raw_message_edit(before, after):
              embeds = after.embeds
              print(after)
              for emb in embeds:
                  mDict = emb.to_dict()
                  desc = mDict['description']
                  p = re.compile("\*\*.* chips\*\*.*",)
                  result = p.search(desc)
                  myMatch = result.group(0)
                  chipCount = int(myMatch.replace("*","").replace("chips",""))
                  print(chipCount)

     @commands.Cog.listener()
     async def on_raw_message_edit(before,after):
         print(after)

def setup(bot):
    bot.add_cog(BribeCog(bot))
