import os
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()
Blackmail_role_name = "Blackmailer"
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@tasks.loop(seconds=5)
async def get_all_members_ids(discguild):
     for guild in client.guilds:
          for member in guild.members:
               for role in member.roles:
                    if role.name == "Blackmailer":
                         role = discord.utils.get(member.guild.roles, name="Blackmailer")
                         await member.remove_roles(role)

get_all_members_ids.start(GUILD)
client.run(TOKEN)

