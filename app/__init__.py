from flask import Flask, render_template, session, request, redirect 
import sqlite3
import requests
import utl.database as data_tables 
import utl.quiz as quiz
import flask
# from api import * 

app = Flask(__name__)
app.secret_key = 'imthreesecondsawayfromgivingup'
db = sqlite3.connect("DB_FILE.db")
c = db.cursor()

data_tables.setup() 
#c.execute("DROP TABLE IF EXISTS users")

@app.route("/",  methods=['GET', 'POST'])
def intro():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def registration(): 
    # gotta make a log out button before implementing that whoops
    # if(len(session) > 0):
    #     return redirect("/dashboard")
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
    # gotta make a log out button before implementing that whoops
    # if(len(session) > 0):
    #     return redirect("/dashboard")
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
        username = flask.session["username"]
        weight = str(request.form["weight"])
        fit_lvl = request.form["fitness_level"]
        print(username)
        data_tables.update_quiz(keys=["weight", "fitness_level"], values=[weight, fit_lvl], username=username)
        return redirect('/dashboard')

@app.route("/logout")
def logout(): 
    session.pop("username")
    session.pop("password")
    return redirect("/login")

if __name__ == "__main__": 
    app.debug = True
    app.run()