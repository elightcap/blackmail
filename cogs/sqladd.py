import os
from discord.ext import commands
import mysql.connector as database
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
dbUser = os.getenv('MARIAUSER')
dbPass = os.getenv('MARIAPASS')

async def sql_insert(db, table, uid, cid = 1, rid = 1):
    try:
        connection = database.connect(
        user = dbUser,
        password = dbPass,
        host='localhost',
        db=db
        )
        cursor = connection.cursor(buffered=True)
        if db == "robbed":
            datetimenow = datetime.now()
            mDate = datetimenow.strftime("%Y-%m-%d")
            mTime = datetimenow.strftime("%H:%M:%S")
            statement =  """INSERT INTO {table_name} (uid,date,time) VALUES (%s,%s,%s)""".format(table_name=table)
            data = (uid,mDate,mTime)
        elif db == "channels":
            statement = """INSERT INTO {table_name} (owner,channelid,roleid) VALUES(%s,%s,%s)""".format(table_name=table)
            data = (uid,cid,rid)
        cursor.execute(statement,data)
        connection.commit()
        print("{} added to {}".format(uid, db))

    except database.Error as e:
        print(f" remove {e}")