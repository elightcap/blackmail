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
    db='lawyer'
)
cursor = connection.cursor(buffered=True)

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
                print("success add")
            except database.Error as e:
                print(f"update {e}")

@aiocron.crontab('*/1 * * * *')
async def remove_robinhoodimmune():
    try:
        statement = "SELECT * from users;"
        cursor.execute(statement)
        result = cursor.fetchone()
        if result:
            try:
                for(uid, date, time) in cursor:
                    datetimenow = datetime.now()
                    addTime = timedelta(minutes=5)
                    dateNowStr = datetimenow.strftime("%Y-%m-%d")
                    timeNowStr = datetimenow.strftime("%H:%M:%S")
                    mDate = (datetime.strptime(dateNowStr, "%Y-%m-%d")).date()
                    mTime = datetime.strptime(timeNowStr, "%H:%M:%S")
                    newTime = (mTime - addTime).time()
                    uDate = date
                    uTimestr = str(time)
                    uTime = datetime.strptime(uTimestr, "%H:%M:%S").time()
                    uUid = int(uid)
                    print(uid,date)
                    if uDate <= mDate:
                        if uTime <= newTime:
                            member = client.get_user(uid)
                            for guild in client.guilds:
                                for member in guild.members:
                                    for role in member.roles:
                                        if role.name == "Robinhood Immune":
                                            role  = discord.utils.get(member.guild.roles, name="Robinhood Immune")
                                            await member.remove_roles(role)
                                            remove = "DELETE FROM `users` WHERE uid = (%s)"
                                            data = (uid,)
                                            cursor.execute(remove, data)
                                            connection.commit()
                                            print("role removed")
            except:
                return
        else:
            print("empty table")

    except database.Error as e:
        print(f" remove {e}")

remove_robinhoodimmune.start()
client.run(TOKEN)
