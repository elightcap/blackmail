import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import sys, traceback

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
unbkey = os.getenv('UNBKEY')
dbUser = os.getenv('MARIAUSER')
dbPass = os.getenv('MARIAPASS')
botUrl = "https://unbelievaboat.com/api/v1/guilds/86565008669958144/users/613156357239078913"
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)


def get_prefix(bot, message):
    prefixes=['!', '!?']
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['cogs.commands',
                                  'cogs.db'
                                ]

bot = commands.Bot(command_prefix=get_prefix, description="Bot to do stuff with unbelieveaboat", intents=intents)

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
bot.run(TOKEN, bot=True, reconnect=True)
