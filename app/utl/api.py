from flask import Flask, session, render_template, request, redirect
import requests 
import json 

def search(foodName):
    k = "DEMO_KEY"
    url = f"https://api.nal.usda.gov/fdc/v1/foods/list?api_key={k}&query={foodName}"
    data = requests.get(url)
    all = json.loads(data.text)
    foods = []
    protein = 0
    fat = 0
    carbs = 0 
    calories_per_100g = 0
    for food in all:
        if food["dataType"] == "Branded": 
            for index in range(len(food["foodNutrients"])):
                if food["foodNutrients"][index]["number"] == '203':
                    protein = food["foodNutrients"][index]["amount"]
                if food["foodNutrients"][index]["number"] == '204':
                    fat = food["foodNutrients"][index]["amount"]
                if food["foodNutrients"][index]["number"] == '205':
                    carbs = food["foodNutrients"][index]["amount"]
                if food["foodNutrients"][index]["number"] == '208':
                    calories_per_100g= food["foodNutrients"][index]["amount"]
            foods.append({"id":food["fdcId"],"brand":food['brandOwner'], "description":food["description"], "protein":protein, "fat":fat, "carbs":carbs, "calories per 100g": calories_per_100g})
        else:
            for index in range(len(food["foodNutrients"])):
                if food["foodNutrients"][index]["number"] == '203':
                    protein = food["foodNutrients"][index]["amount"]
                if food["foodNutrients"][index]["number"] == '204':
                    fat = food["foodNutrients"][index]["amount"]
                if food["foodNutrients"][index]["number"] == '205':
                    carbs = food["foodNutrients"][index]["amount"]
                if food["foodNutrients"][index]["number"] == '208':
                    calories_per_100g= food["foodNutrients"][index]["amount"]
            foods.append({"id":food["fdcId"],"brand":None, "description":food["description"], "protein":protein, "fat":fat, "carbs":carbs, "calories per 100g": calories_per_100g})
    print(foods)
    return foods

def search_exercise(exerciseName):
    url = "https://raw.githubusercontent.com/annafang30/exercise_stats/main/exercise_stats.json" 
    data2 = requests.get(url)
    all = json.loads(data2.text)
    exercises = []
    names = [] 
    for exercise in all: 
        # grabs just the names
        names.append(exercise["Activity, Exercise or Sport (1 hour)"])
    for index in range(len(names)):
        if exerciseName in names[index]:
            # grabs the name and the calories burned per kg (have to convert into pounds ugh)
            exercises.append({all[index]["Activity, Exercise or Sport (1 hour)"]: exercise["Calories per kg"]})
    print(exercises)
    return exercises 
    # check if query is in database 
    
    

    
