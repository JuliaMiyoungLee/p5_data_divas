from flask import Flask, render_template, session, request, redirect 
import sqlite3
import requests
import utl.database as data_tables 
import utl.quiz as quiz
import flask
import utl.api as api_funcs

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
                return redirect("/quiz")
            else:
                return redirect("/login")
                # pop up? 
    # # render template
    return render_template("login.html")

@app.route("/dashboard", methods=['GET', 'POST'])
def dash(): 
    if flask.request.method == "POST":
        # If user searches for something, returns page with list of foods from the search
        # blank search or ' ' results in display of a selection from ALL items -> simply checking length causes case exeption errors

        # first search 
        if ("food_search" in request.form):
            if(request.form["food_search"] != None):
                return render_template("addFood.html", data=api_funcs.search(request.form["food_search"]), search=request.form["food_search"])
        # second search 
        if("exercise_search" in request.form): 
            if(request.form["exercise_search"] != None): 
                return render_template("workouts.html")
    else:
        return render_template("dashboard.html")

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
        gender =  str(request.form["gender"])
        weight = str(request.form["weight"])
        height = str(request.form["height"])
        age = str(request.form["age"])
        fit_lvl = request.form["fitness_level"]
        print(username)
        print(age) 
        data_tables.update_quiz(keys=["gender","weight", "height", "age","fitness_level"], values=[gender,weight, height, age, fit_lvl], username=username)
        return redirect('/dashboard')

@app.route("/logout")
def logout(): 
    session.pop("username")
    session.pop("password")
    return redirect("/")

if __name__ == "__main__": 
    app.debug = True
    app.run()