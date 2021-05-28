import os
import discord
import aiocron
import datetime
import mysql.connector as database
from dotenv import load_dotenv
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
            user = int(after.id)
            try:
                statement = "INSERT INTO users (uid,date,time) VALUES (%s, %s, %s)"
                data = (user,mDate,mTime)
                cursor.execute(statement,data)
                connection.commit()
                print("success")
            except database.Error as e:
                print(f"{e}")

@aiocron.crontab('*/1 * * * *')
async def remove_robinhoodimmune():
    try:
        statement = "SELECT * from users;"
        cursor.execute(statement)
        for(uid, date, time) in cursor:
            datetimenow = datetime.now()
            addTime = datetime.timedelta(minutes=1)
            mDate = datetimenow.strftime("%Y-%m-%d")
            mTime = datetimenow.strftime("%H:%M:%S")
            newTime = mTime - addTime
            uDate = datetime(date)
            uTime = datetime(time)
            uUid = int(uid)
            print({uid},{date})
            print(mDate)
            print(uDate)
            if uDate <= mDate:
                if uTime >= newTime:
                    role = discord.utils.get(member.guild.roles, name="Robinhood Immune")
                    member = guild.get_member(uUid)
                    await member.remove_roles(role)
                    remove = "DELETE FROM `users` WHERE uid = (%s)"
                    data = (uUid)
                    cursor.execute(remove, data)
                    connection.commit()

    except database.Error as e:
        print(f"{e}")

remove_robinhoodimmune.start()
client.run(TOKEN)
