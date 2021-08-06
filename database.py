import sqlite3


connection = sqlite3.connect('database.db')

cursor = connection.cursor()


cursor.execute('''select id from links
where message_id = 6


''')
if(cursor.fetchone() != None):
    res = (cursor.fetchone())[0]
    print(res)

