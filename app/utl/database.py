import sqlite3
from datetime import date
DB_FILE = "DB_FILE.db"

# User Registry and Login
def setup(): 
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor() 
    # c.execute("CREATE TABLE IF NOT EXISTS users(username text, password text);")
    c.execute("CREATE TABLE IF NOT EXISTS users(username text, password text, gender text, goal text, weight integer,height integer, age integer, fitness_level integer);")
    c.execute("CREATE TABLE IF NOT EXISTS foods(username text, name text, brand text, id integer, protein text, fat text, carbs text, calories integer, type text, timestamp text);")
    db.commit()
    db.close() 

def existence(username): 
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor() 
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    length = len(c.fetchall())
    if (length > 0): 
        return True 
    else: 
        return False 
    
def register_me(username, password): 
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor() 
    # insert the user into db 
    c.execute("insert INTO users VALUES(?, ? ,NULL, NULL, NULL, NULL, NULL, NULL)", [username, password,])
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

# User Updates with Quiz
def update_quiz(keys, values, username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "UPDATE users SET "
    for i in range(len(keys)):
        print(keys)
        if(i==0 or i ==1):
            query += keys[i] + " = '" + values[i] + "', "
        else: 
            query += keys[i] + " = " + values[i] + ", "
    query = query[:-2]
    query += " WHERE username = '" + username + "';"
    print(query)
    c.execute(query)
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

# Updates Food tables
def add_food(values):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "INSERT INTO foods ("
    query += "username, name, brand, id, protein, fat, carbs, calories, type, timestamp) VALUES ("
    for value in values:
        if type(value) is str:
            query += f"'{value}', "
        else:
            query += f"{value}, "
    query += " '" + date.today().strftime("%b-%d-%Y") + "')"
    c.execute(query)
    db.commit() 
    db.close()

def get_breakfast(username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "SELECT * FROM foods WHERE username = '" + username + "' AND type = 'breakfast'"
    info = c.execute(query)
    foods = info.fetchall()
    db.commit() 
    db.close()
    return foods

def get_lunch(username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "SELECT * FROM foods WHERE username = '" + username + "' AND type = 'lunch'"
    info = c.execute(query)
    foods = info.fetchall()
    db.commit() 
    db.close()
    return foods

def get_dinner(username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "SELECT * FROM foods WHERE username = '" + username + "' AND type = 'dinner'"
    info = c.execute(query)
    foods = info.fetchall()
    db.commit() 
    db.close()
    return foods

def get_snack(username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "SELECT * FROM foods WHERE username = '" + username + "' AND type = 'snack'"
    info = c.execute(query)
    foods = info.fetchall()
    db.commit() 
    db.close()
    return foods

def delete_food(username, foodId):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = f"DELETE FROM foods WHERE username = '{username}' AND id = {foodId}"
    print(query)
    c.execute(query)
    db.commit() 
    db.close()