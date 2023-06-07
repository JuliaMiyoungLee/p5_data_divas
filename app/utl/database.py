import sqlite3
DB_FILE = "DB_FILE.db"

def setup(): 
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor() 
    # c.execute("CREATE TABLE IF NOT EXISTS users(username text, password text);")
    c.execute("CREATE TABLE IF NOT EXISTS users(username text, password text, gender text, weight integer,height integer, age integer, fitness_level integer);")
    c.execute("CREATE TABLE IF NOT EXISTS foods(username text, timestamp text, name text, serving size text, calories text, ingredients text, brand text, carbs integer, fat integer, protein integer);")
    print("table generated")
    db.commit()
    db.close() 

def existence(username): 
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor() 
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    length = len(c.fetchall())
    print("username_retrieved")
    if (length > 0): 
        return True 
    else: 
        return False 
    
def register_me(username, password): 
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor() 

    # insert the user into db 
    c.execute("insert INTO users VALUES(?, ? ,NULL, NULL, NULL, NULL, NULL)", [username, password,])
    db.commit()
    db.close() 


def log_me_in(username, password): 
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor() 
    #get password 
    info = c.execute("SELECT password FROM users WHERE username=?", (username,))
    results = info.fetchall()
    correct = results[0][0]
    #check
    if password == correct: 
        db.commit()
        db.close()
        return True 
    else: 
        db.commit()
        db.close()
        return False 
    
def update_quiz(keys, values, username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "UPDATE users SET "
    for i in range(len(keys)):
        if(i==0):
            query += keys[i] + " = '" + values[i] + "', "
        else: 
            query += keys[i] + " = " + values[i] + ", "
    query = query[:-2]
    query += " WHERE username = '" + username + "';"
    print(query)
    c.execute(query)
    print("table updated")
    db.commit() 
    db.close() 
        

def quizzed(username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    # Build query
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    print(query)
    info = c.execute(query)
    results = info.fetchall()
    gender = results[0][2]
    db.commit() 
    db.close() 
    if gender == None:
        return 0
    return 1

