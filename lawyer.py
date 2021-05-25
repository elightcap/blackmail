import os
import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)


def remove_lawyer(discguild):
     1==1 

thing=remove_lawyer(GUILD)
print(thing)
client.run(TOKEN)
