import os
import discord
import aiocron
import mysql.connector as database
from dotenv import load_dotenv
from datetime import datetime, timedelta
from discord.ext import tasks
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
dbUser = os.getenv('MARIAUSER')
dbPass = os.getenv('MARIAPASS')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)
connection = database.connect(
    user = dbUser,
    password = dbPass,
    host='localhost',
    db='robbed'
)
cursor = connection.cursor(buffered=True)

@client.event
async def on_member_update(before,after):
    if len(before.roles)<len(after.roles):
        newRole = next(role for role in after.roles if role not in before.roles)

        if newRole.name == "Robbery Victim":
            connection = database.connect(
                user = dbUser,
                password = dbPass,
                host='localhost',
                db='robbed'
            )
            cursor = connection.cursor(buffered=True)
            datetimenow = datetime.now()
            mDate = datetimenow.strftime("%Y-%m-%d")
            mTime = datetimenow.strftime("%H:%M:%S")
            user = int(after.id)
            try:
                statement = "INSERT INTO users (uid,date,time) VALUES (%s, %s, %s)"
                data = (user,mDate,mTime)
                cursor.execute(statement,data)
                connection.commit()
                print("success add")
            except database.Error as e:
                print(f"update {e}")
        
        elif newRole.name == "Blackmailer":
            connection = database.connect(
                user = dbUser,
                password = dbPass,
                host='localhost',
                db='robbed'
            )
            cursor = connection.cursor(buffered=True)
            datetimenow = datetime.now()
            mDate = datetimenow.strftime("%Y-%m-%d")
            mTime = datetimenow.strftime("%H:%M:%S")
            user = int(after.id)
            try:
                statement = "INSERT INTO users (uid,date,time) VALUES (%s, %s, %s)"
                data = (user,mDate,mTime)
                cursor.execute(statement,data)
                connection.commit()
                print("success add")
            except database.Error as e:
                print(f"update {e}")
        elif newRole.name == "Lawyer'd Up":
            connection = database.connect(
                user = dbUser,
                password = dbPass,
                host='localhost',
                db='robbed'
            )
            cursor = connection.cursor(buffered=True)
            datetimenow = datetime.now()
            mDate = datetimenow.strftime("%Y-%m-%d")
            mTime = datetimenow.strftime("%H:%M:%S")
            user = int(after.id)
            try:
                statement = "INSERT INTO users (uid,date,time) VALUES (%s, %s, %s)"
                data = (user,mDate,mTime)
                cursor.execute(statement,data)
                connection.commit()
                print("success add")
            except database.Error as e:
                print(f"update {e}")

@aiocron.crontab('*/1 * * * *')
async def remove_robberyvictim():
    try:
        getUser = "SELECT * from users;"
        cursor.execute(getUser)
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                uUid = int(row[0])
                uDate = row[1]
                strTime = str(row[2])
                uTime = datetime.strptime(strTime,"%H:%M:%S" ).time()
                try:
                    datetimenow = datetime.now()
                    addTime = timedelta(minutes=5)
                    dateNowStr = datetimenow.strftime("%Y-%m-%d")
                    timeNowStr = datetimenow.strftime("%H:%M:%S")
                    mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                    mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                    newTime = (mTime - addTime).time()
                    print(uDate,mDate)
                    if uDate <= mDate:
                        print(uTime,newTime)
                        if uTime <= newTime:
                            print("here")
                            member = client.get_user(uUid)
                            for guild in client.guilds:
                                for member in guild.members:
                                    for role in member.roles:
                                        if role.name == "Robbery Victim":
                                            role  = discord.utils.get(member.guild.roles, name="Robbery Victim")
                                            if member.id == uUid:
                                                await member.remove_roles(role)
                                                remove = "DELETE FROM `users` WHERE uid = (%s)"
                                                data = (uUid,)
                                                cursor.execute(remove, data)
                                                connection.commit()
                                                print("role removed from {uUID}")
                except os.error as e:
                    print(e)

    except database.Error as e:
        print(f" remove {e}")

async def remove_lawyer():
    try:
        getUser = "SELECT * from users;"
        cursor.execute(getUser)
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                uUid = int(row[0])
                uDate = row[1]
                strTime = str(row[2])
                uTime = datetime.strptime(strTime,"%H:%M:%S" ).time()
                try:
                    datetimenow = datetime.now()
                    addTime = timedelta(minutes=5)
                    dateNowStr = datetimenow.strftime("%Y-%m-%d")
                    timeNowStr = datetimenow.strftime("%H:%M:%S")
                    mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                    mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                    newTime = (mTime - addTime).time()
                    print(uDate,mDate)
                    if uDate <= mDate:
                        print(uTime,newTime)
                        if uTime <= newTime:
                            print("here")
                            member = client.get_user(uUid)
                            for guild in client.guilds:
                                for member in guild.members:
                                    for role in member.roles:
                                        if role.name == "Lawyer'd Up":
                                            role  = discord.utils.get(member.guild.roles, name="Lawyere'd Up")
                                            if member.id == uUid:
                                                await member.remove_roles(role)
                                                remove = "DELETE FROM `users` WHERE uid = (%s)"
                                                data = (uUid,)
                                                cursor.execute(remove, data)
                                                connection.commit()
                                                print("role removed from {uUID}")
                except os.error as e:
                    print(e)
    except database.Error as e:
        print(f" remove {e}")

async def remove_blackmail():
    try:
        getUser = "SELECT * from users;"
        cursor.execute(getUser)
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                uUid = int(row[0])
                uDate = row[1]
                strTime = str(row[2])
                uTime = datetime.strptime(strTime,"%H:%M:%S" ).time()
                try:
                    datetimenow = datetime.now()
                    addTime = timedelta(minutes=5)
                    dateNowStr = datetimenow.strftime("%Y-%m-%d")
                    timeNowStr = datetimenow.strftime("%H:%M:%S")
                    mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                    mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                    newTime = (mTime - addTime).time()
                    print(uDate,mDate)
                    if uDate <= mDate:
                        print(uTime,newTime)
                        if uTime <= newTime:
                            print("here")
                            member = client.get_user(uUid)
                            for guild in client.guilds:
                                for member in guild.members:
                                    for role in member.roles:
                                        if role.name == "Blackmailer":
                                            role  = discord.utils.get(member.guild.roles, name="Blackmailer")
                                            if member.id == uUid:
                                                await member.remove_roles(role)
                                                remove = "DELETE FROM `users` WHERE uid = (%s)"
                                                data = (uUid,)
                                                cursor.execute(remove, data)
                                                connection.commit()
                                                print("role removed from {uUID}")
                except os.error as e:
                    print(e)
    except database.Error as e:
        print(f" remove {e}")




remove_robberyvictim.start()
remove_lawyer.start()
client.run(TOKEN)
