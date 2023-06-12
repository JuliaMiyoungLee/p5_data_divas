import sqlite3
from datetime import date
import utl.algorithm as algo_funcs
DB_FILE = "DB_FILE.db"

# User Registry and Login
def setup(): 
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor() 
    c.execute("CREATE TABLE IF NOT EXISTS users(username text, password text, gender text, goal text, weight integer,height integer, age integer, fitness_level integer, calorie_goal integer);")
    c.execute("CREATE TABLE IF NOT EXISTS foods(username text, name text, brand text, id integer, protein text, fat text, carbs text, calories integer, foodType text, timestamp text);")
    c.execute("CREATE TABLE IF NOT EXISTS exercises(username text, name text, cals text, reps integer, timestamp text);")
    c.execute("CREATE TABLE IF NOT EXISTS weights(username text, weight text, timestamp text);")
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
    c.execute("insert INTO users VALUES(?, ? ,NULL, NULL, NULL, NULL, NULL, NULL, NULL)", [username, password,])
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

def update_weight(username, weight, timestamp):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = f"INSERT INTO weights VALUES ('{username}', '{weight}', '{timestamp}')"
    c.execute(query)
    query = f"UPDATE users SET weight = '{weight}' WHERE username = '{username}'"
    c.execute(query)
    db.commit() 
    db.close()

def get_user(username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor() 
    info = c.execute(f"SELECT * FROM users WHERE username='{username}'")
    results = info.fetchall()
    db.commit() 
    db.close() 
    return results[0]
        
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

# # fluid calorie display  
def calculate(username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    info = c.execute(query)
    results = info.fetchall()
    print(results)
    gender = results[0][2]
    goal = results[0][3]
    weight = results[0][4]
    height = results[0][5]
    age = results[0][6]
    fitness_level = results[0][7]
    user_bmr = algo_funcs.bmr(gender, height, weight,age)
    user_amr = algo_funcs.amr(fitness_level, user_bmr)
    result = algo_funcs.calories(goal,user_amr)
    db.commit() 
    db.close() 
    return result

def get_weight(username):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "SELECT weight FROM users WHERE username = '" + username + "'"
    info = c.execute(query)
    results = info.fetchall()
    results = results[0][0]
    db.commit() 
    db.close() 
    return results

def adjust_calories(username):
    val = calculate(username)
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    c.execute("UPDATE users SET calorie_goal = ? WHERE username = ?", (val, username))
    count = c.execute("SELECT calorie_goal FROM users WHERE username = '" + username + "'")
    data = count.fetchall()
    cal = data[0][0]
    db.commit()
    db.close() 
    return cal 

# Updates Food tables
def add_food(values):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "INSERT INTO foods ("
    query += "username, name, brand, id, protein, fat, carbs, calories, foodType, timestamp) VALUES ("
    for value in values:
        if type(value) is str:
            query += f"'{value}', "
        else:
            query += f"{value}, "
    query += " '" + date.today().strftime("%m-%d-%Y") + "')"
    c.execute(query)
    db.commit() 
    db.close()

def get_breakfast(username, date):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = f"SELECT * FROM foods WHERE username = '{username}' AND foodType = 'breakfast' AND timestamp = '{date}'"
    info = c.execute(query)
    foods = info.fetchall()
    db.commit() 
    db.close()
    return foods

def get_lunch(username, date):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = f"SELECT * FROM foods WHERE username = '{username}' AND foodType = 'lunch' AND timestamp = '{date}'"
    info = c.execute(query)
    foods = info.fetchall()
    db.commit() 
    db.close()
    return foods

def get_dinner(username, date):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = f"SELECT * FROM foods WHERE username = '{username}' AND foodType = 'dinner' AND timestamp = '{date}'"
    info = c.execute(query)
    foods = info.fetchall()
    db.commit() 
    db.close()
    return foods

def get_snack(username, date):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = f"SELECT * FROM foods WHERE username = '{username}' AND foodType = 'snack' AND timestamp = '{date}'"
    info = c.execute(query)
    foods = info.fetchall()
    db.commit() 
    db.close()
    return foods


def delete_food(username, foodId, foodType, date):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = f"DELETE FROM foods WHERE username = '{username}' AND id = {foodId} AND foodType = '{foodType}' AND timestamp = '{date}'"
    print(query)
    c.execute(query)
    db.commit() 
    db.close()

# Exercise functions
def add_exercise(values):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = "INSERT INTO exercises ("
    query += "username, name, cals, reps, timestamp) VALUES ("
    for value in values:
        if type(value) is str:
            query += f"'{value}', "
        else:
            query += f"{value}, "
    query += " '" + date.today().strftime("%m-%d-%Y") + "')"
    c.execute(query)
    db.commit() 
    db.close()

def get_exercises(username, date):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = f"SELECT * FROM exercises WHERE username = '{username}' AND timestamp = '{date}'"
    info = c.execute(query)
    foods = info.fetchall()
    db.commit() 
    db.close()
    return foods

def delete_exercise(username, name, timestamp):
    db = sqlite3.connect("DB_FILE.db")
    c = db.cursor()
    query = f"DELETE FROM exercises WHERE username = '{username}' AND name = '{name}' AND timestamp = '{timestamp}'"
    print(query)
    c.execute(query)
    db.commit() 
    db.close()