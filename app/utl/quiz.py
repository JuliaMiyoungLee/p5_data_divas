import sqlite3
DB_FILE = "DB_FILE.db"

def update(keys, values, username):
    query = "UPDATE users SET "
    for i in range(len(keys)):
        query += keys[i] + " = " + values[i] + ","
    query = query[:-2]
    query += " WHERE username = " + username + ";"
    print(query)
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    c.execute(query)
