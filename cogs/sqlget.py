import os
from discord.ext import commands
import mysql.connector as database
from dotenv import load_dotenv

load_dotenv()
dbUser = os.getenv('MARIAUSER')
dbPass = os.getenv('MARIAPASS')

async def sql_select(db, table, uid):
     try:
            connection = database.connect(
                    user = dbUser,
                    password = dbPass,
                    host='localhost',
                    db=db
            )
            cursor = connection.cursor(buffered=True)
            statement = 'SELECT * from (%s) where uid=(%s)'
            data = (table, uid)
            cursor.execute(statement, data)
            rows = cursor.fetchall()
            return rows