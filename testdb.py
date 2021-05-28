import os
import discord
import mysql.connector as database
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import tasks
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
dbUser = os.getenv('MARIAUSER')
dbPass = os.getenv('MARIAPASS')
client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)
connection = database.connect(
    user = dbUser,
    password = dbPass,
    host='localhost',
    db='lawyer'
)
cursor = connection.cursor()

@client.event
async def on_member_update(before,after):
    if len(before.roles)<len(after.roles):
        newRole = next(role for role in after.roles if role not in before.roles)

        if newRole.name == "Robinhood Immune":
            datetimenow = datetime.now()
            mDate = datetimenow.strftime("%Y-%m-%d")
            mTime = datetimenow.strftime("%H:%M:%S")
            user = after.name
            print(after.id)
            try:
                statment = "INSERT INTO users (uid,date,time) VALUES (%s, %s, %s)"
                data = (user,mDate,mTime)
                cursor.execute(statement,data)
                connection.commit()
                print("success")
            except database.Error as e:
                print(f"{e}")
            connection.close()

client.run(TOKEN)
