import os
import mysql.connector as database
from dotenv import load_dotenv

load_dotenv()
dbUser = os.getenv('MARIAUSER')
dbPass = os.getenv('MARIAPASS')

async def sql_remove(db, table, attname, att):
    try:
        connection = database.connect(
        user = dbUser,
        password = dbPass,
        host='localhost',
        db=db
        )
        cursor = connection.cursor(buffered=True)
        statement = """Delete from {table_name} WHERE {att_name} = (%s)""".format(table_name=table, att_name=attname)
        data = (att,)
        cursor.execute(statement,data)
        connection.commit()
        print("{} removed from {}".format(att, table))

    except database.Error as e:
        print(f" remove {e}")