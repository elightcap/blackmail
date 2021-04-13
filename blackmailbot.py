# bot.py
import os
import requests
import discord
import threading
import time
from twister.internet import task, reactor

from dotenv import load_dotenv
from operator import itemgetter

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
timeout = 7200.0

async def removeRole();
     remove = "!mass-role remove @everyone @blackmailer"
     send = await message.channel.send(remove)
     time.sleep(5)
     confirm = "yes"
     send2 = await message.channel.send(confirm)
     time.sleep(5)
     await send.delete()
     await send2.delete()

l = task.LoopingCall(removeRole)
l.start(timeout)

reactor.run()
