import os
from typing import cast

from requests.models import CaseInsensitiveDict
import aiocron
import requests
import discord
import json
import math
import time
import mysql.connector as database
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
from datetime import datetime, timedelta

import sys, traceback

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
unbkey = os.getenv('UNBKEY')
dbUser = os.getenv('MARIAUSER')
dbPass = os.getenv('MARIAPASS')
pokerBotID = "613156357239078913"
botUrl = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/613156357239078913"
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)
headers = {'Authorization': unbkey}

def get_prefix(bot, message):
    prefixes=['!', '!?']
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['cogs.nuke',
                                  'cogs.invite']

bot = commands.bot(command_prefix=get_prefix, description="Bot to do stuff with unbelieveaboat")

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load {extension}', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Streaming(name='Cashier'))
    print(f'Logged in')

bot.run(TOKEN, bot=True, reconnect=True)