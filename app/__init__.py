from flask import Flask, render_template, session, request, redirect 
import sqlite3
import requests
import utl.database as data_tables 
import flask
import utl.api as api_funcs
from datetime import date as dates
import utl.calendar as calendify
import utl.algorithm as algo_funcs

app = Flask(__name__)
app.secret_key = 'imthreesecondsawayfromgivingup'
db = sqlite3.connect("DB_FILE.db")
c = db.cursor()

data_tables.setup() 
#c.execute("DROP TABLE IF EXISTS users")
#c.execute("DROP TABLE IF EXISTS foods")

@app.route("/",  methods=['GET', 'POST'])
def intro():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def registration(): 
    # register options
    if (len(request.form) > 0):
        if (data_tables.existence(request.form['username']) == False):
            data_tables.register_me(request.form["username"], request.form["password"])
            return redirect("/login")
        else:
            return redirect("/register")
    # render template
    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login(): 
    if (len(request.form) > 0): 
        if (data_tables.existence(request.form['username']) == True):
            if(data_tables.log_me_in(request.form['username'], request.form['password']) == True):
                session["username"] = request.form["username"] 
                session["password"] = request.form["password"]
                if data_tables.quizzed(session["username"]) > 0:
                    today = dates.today().strftime("%m-%d-%Y")
                    return redirect(f"/dashboard/{today}")
                return redirect("/quiz")
            else:
                return render_template("login.html", ErrorMessage="Username does not match password")
                # pop up? 
        else:
            return render_template("login.html", ErrorMessage="Username not found")
    # # render template
    return render_template("login.html")

@app.route("/home")
def home():
    date = dates.today().strftime("%m-%d-%Y")
    return redirect(f"/dashboard/{date}")

@app.route("/profile", methods=['GET', 'POST'])
def profilePage():
    ref = data_tables.get_user(session["username"])
    fem = None
    male = None
    if (ref[2]=="female"):
        female = "selected"
    else:
        male = "selected"
        
    user = session["username"]
    weight = ref[4] # Done
    height = ref[5] # Done
    age = ref[6] # Done
    fitness_level = ref[7] # Done
    goal = ref[3] # Done
    # lose
    # maintain
    # gain
    lose = None
    maintain = None
    gain = None
    if (goal == "lose"):
        lose = "selected"
    elif (goal == "maintain"):
        maintain = "selected"
    else:
        gain = "selected"

    sedentary = None
    lightly_active = None
    moderately_active = None
    very_active = None
    extremely_active = None
    
    if fitness_level == 1:
        sedentary = "selected"
    elif fitness_level == 2:
        lightly_active = "selected"
    elif fitness_level == 3:
        moderately_active = "selected"
    elif fitness_level == 4:
        very_active = "selected"
    elif fitness_level == 5:
        extremely_active = "selected"
    
    # fitness level is done
    
    

    return render_template("profile.html", user=user,lose = lose, gain = gain, maintain = maintain, sedentary=sedentary, lightlyactive=lightly_active, moderatelyactive=moderately_active,veryactive = very_active, extremelyactive = extremely_active, data=ref, male=male, fem=fem, weight=weight, height=height, age=age, goal=goal)

@app.route("/updateProfile", methods=['GET', 'POST'])
def updateProfile():
    if flask.request.method == "POST":
        None
        gender = request.form["gender"]
        weight = request.form["weight"]
        height = request.form["height"]
        age = request.form["age"]
        fitness_level = request.form["fitness_level"]
        goal = request.form["goal"]
        user_bmr = algo_funcs.bmr(gender, int(height), int(weight),int(age))
        user_amr = algo_funcs.amr(fitness_level, user_bmr)
        cal = algo_funcs.calories(goal,user_amr)
        today = dates.today().strftime('%m-%d-%Y')
        data_tables.update_weight(session["username"], weight, today)
        data_tables.update_user_values(session["username"], session["password"],gender, goal,weight,height,age,fitness_level,calorie_goal=cal)

    return redirect("/profile")

def get_cals(lst):
    cals = 0
    for i in lst:
        cals += i[-3]
    return cals
        

@app.route("/dashboard/<date>", methods=['GET', 'POST'])
def dash(date): 
    if flask.request.method == "POST":
        # If user searches for something, returns page with list of foods from the search
        # blank search or ' ' results in display of a selection from ALL items -> simply checking length causes case exeption errors

        # first search option 
        if ("food_search" in request.form):
            if(request.form["food_search"] != None):
                return render_template("addFood.html", data=api_funcs.search(request.form["food_search"]), search=request.form["food_search"], date1=date)
        # second search option
        if("exercise_search" in request.form): 
            if(request.form["exercise_search"] != None): 
                return render_template("workouts.html", data=api_funcs.search_exercise(request.form["exercise_search"]), search=request.form["exercise_search"], date1=date)
    else:
        user = session["username"]
        weight = data_tables.get_user(user)[4]
        today = dates.today().strftime('%m-%d-%Y')
        # user calorie display 
        calories = data_tables.adjust_calories(user)
        #date and food/exercise displays
        dateDisplay = calendify.get_date_fancy(date)
        breakfasts = data_tables.get_breakfast(user, date)
        total_breakfast_calories = get_cals(breakfasts)
        lunchs = data_tables.get_lunch(user, date)
        total_lunch_calories = get_cals(lunchs)
        dinners = data_tables.get_dinner(user, date)
        total_dinner_calories = get_cals(dinners)
        snacks = data_tables.get_snack(user, date)
        total_snack_calories = get_cals(snacks)
        
        add_cats = 0
        if total_breakfast_calories > 0:
            add_cats += 1
            
        if total_lunch_calories > 0:
            add_cats += 1
            
        if total_dinner_calories > 0:
            add_cats += 1
            
        if total_snack_calories > 0:
            add_cats += 1
            
        if add_cats == 0:
            add_cats = 4
        elif (add_cats < 4):
            add_cats = 4 - add_cats
        
        calorieG = calories
        calories -= (total_breakfast_calories + total_lunch_calories + total_dinner_calories + total_snack_calories)
        
        if total_breakfast_calories == 0:
            total_breakfast_calories = "Calories Available: " + str(int(calories / add_cats))
        else:
            total_breakfast_calories = "Total Calories: " + str(total_breakfast_calories)
        
        if total_lunch_calories == 0:
            total_lunch_calories = "Calories Available: " + str(int(calories / add_cats))
        else:
            total_lunch_calories = "Total Calories: " + str(total_lunch_calories)
            
        if total_dinner_calories == 0:
            total_dinner_calories = "Calories Available: " + str(int(calories / add_cats))
        else:
            total_dinner_calories = "Total Calories: " + str(total_dinner_calories)
            
        if total_snack_calories == 0:
            total_snack_calories = "Calories Available: " + str(int(calories / add_cats))
        else:
            total_snack_calories = "Total Calories: " + str(total_snack_calories)
        
        
        exercises = data_tables.get_exercises(user, date)
        return render_template("dashboard.html", calorie_goal = calorieG, calorie_tracker = calories, breakfastData=breakfasts, breakfast_tracker = total_breakfast_calories, lunch_tracker = total_lunch_calories, dinner_tracker = total_dinner_calories, snacks_tracker = total_snack_calories, lunchData=lunchs, dinnerData=dinners, snackData=snacks, exercises=exercises, date=dateDisplay, date1=date, today=today, weight=weight)


@app.route("/profile")
def profile(): 
    return render_template("profile.html")

@app.route("/quiz", methods=['GET', 'POST'])
def quiz_me(): 
    # if form submitted 
    if flask.request.method == "GET":
        return render_template("quiz.html")
    else:
        # Updates the users table with inputted info
        username = flask.session["username"]
        gender = request.form["gender"]
        goal = request.form["goal"]
        weight = str(request.form["weight"])
        height = str(request.form["height"])
        age = str(request.form["age"])
        fit_lvl = request.form["fitness_level"]
        user_bmr = algo_funcs.bmr(gender, int(height), int(weight),int(age))
        user_amr = algo_funcs.amr(fit_lvl, user_bmr)
        cal = algo_funcs.calories(goal,user_amr)
        today = dates.today().strftime("%m-%d-%Y")
        data_tables.update_weight(username, weight, today, cal)
        data_tables.update_quiz(keys=["gender", "goal", "weight", "height", "age","fitness_level"], values=[gender, goal, weight, height, age, fit_lvl], username=username)
        return redirect(f'/dashboard/{today}')#, calorie=amr_value)
    
@app.route("/addFoods", methods=["GET", "POST"])
def addFood():
    today = dates.today().strftime("%m-%d-%Y")
    if flask.request.method == "POST":
        user = flask.session["username"]
        name = request.form["name"]
        brand = request.form["brand"]
        id = request.form["id"]
        protein = request.form["protein"]
        fat = request.form["fat"]
        carbs = request.form["carbs"]
        calories = request.form["calories"]
        foodType = request.form["foodType"]
        quantity = request.form["gramValue"]
        calories = int(float(calories)) * int(quantity) / 100
        data_tables.add_food([user, name, brand, id, protein, fat, carbs, calories, foodType])
        return redirect(f"/dashboard/{today}")
    return render_template("addFood.html")

@app.route("/addExercise", methods=["GET", "POST"])
def addExercise():
    today = dates.today().strftime("%m-%d-%Y")
    if flask.request.method == "POST":
        user = flask.session["username"]
        weight = data_tables.get_weight(user)
        name = request.form["name"]
        reps = request.form["reps"]
        cals = float(request.form["cals"]) * float(reps) / 60 * float(weight)
        data_tables.add_exercise([user, name, cals, reps])
        return redirect(f"/dashboard/{today}")
    return render_template("workouts.html")

# Delete button should only appear if current date is the same as displayed date
@app.route("/delete", methods=["POST"])
def delete_food():
    today = dates.today().strftime("%m-%d-%Y")
    foodId = request.form["id"]
    foodType = request.form["foodType"]
    calories = request.form["cals"]
    data_tables.delete_food(session["username"], foodId, foodType, calories, today)
    return redirect(f"/dashboard/{today}")

@app.route("/deleteExercise", methods=["POST"])
def delete_exercise():
    today = dates.today().strftime("%m-%d-%Y")
    name = request.form["name"]
    data_tables.delete_exercise(session["username"], name, today)
    return redirect(f"/dashboard/{today}")

@app.route("/goBack/<date>")
def go_back(date):
    newDate = calendify.get_before(date)
    return redirect(f"/dashboard/{newDate}")

@app.route("/goForward/<date>")
def go_forward(date):
    newDate = calendify.get_after(date)
    return redirect(f"/dashboard/{newDate}")

@app.route("/updateWeight", methods=["POST"])
def updateWeight():
    user = session["username"]
    weight = request.form["weight"]
    today = dates.today().strftime("%m-%d-%Y")
    user_info = data_tables.get_user(user)
    gender = user_info[2]
    height = user_info[5]
    age = user_info[6]
    fitness_level = user_info[7]
    goal = user_info[3]
    user_bmr = algo_funcs.bmr(gender, int(height), int(weight),int(age))
    user_amr = algo_funcs.amr(fitness_level, user_bmr)
    cal = algo_funcs.calories(goal,user_amr)
    data_tables.update_weight(user, weight, today, cal)
    return redirect(f"/dashboard/{today}")

@app.route("/logout")
def logout(): 
    session.pop("username")
    session.pop("password")
    return redirect("/")

if __name__ == "__main__": 
    app.debug = True
    app.run()