import sqlite3
from service.botdata_reader import BotDataReader
from werkzeug.security import generate_password_hash


connection = sqlite3.connect('database.db', check_same_thread=False)


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO pre_header (full_name, content) VALUES (?, ?)",
            ('DEFAULT_PREHEADER', 'You are the best consultant')
            )

bot_reader = BotDataReader()
for third_bot in bot_reader.json_data:
    cur.execute("INSERT INTO third_bot (bot_name, token, callback_url) VALUES (?, ?, ?)",
            (bot_reader.json_data[third_bot]['bot_name'], 
             bot_reader.json_data[third_bot]['token'], 
             bot_reader.json_data[third_bot]['callback_url'])
            )


connection.commit()
connection.close()