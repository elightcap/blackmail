import os
from discord.ext import commands
import mysql.connector as database
from dotenv import load_dotenv

load_dotenv()
dbUser = os.getenv('MARIAUSER')
dbPass = os.getenv('MARIAPASS')

async def sql_select(db, table, attname, att):
    try:
        connection = database.connect(
        user = dbUser,
        password = dbPass,
        host='localhost',
        db=db
        )
        cursor = connection.cursor(buffered=True)
        statement = """SELECT * FROM {table_name} where {att_name} like (%s)""".format(table_name=table, att_name=attname)
        data = (table, att)
        cursor.execute(statement, data)
        rows = cursor.fetchall()
        return rows
    except database.Error as e:
        print(f" remove {e}")
