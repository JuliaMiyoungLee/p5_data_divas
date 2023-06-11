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
    return foods

def search_exercise(exerciseName):
    query = exerciseName.capitalize()
    print(query)
    query2 = exerciseName.lower()
    print(query2)
    url = "https://raw.githubusercontent.com/annafang30/exercise_stats/main/exercise_stats.json" 
    data2 = requests.get(url)
    all = json.loads(data2.text)
    exercises = []
    conversion = 0; 
    names = [] 
    for exercise in all: 
        # grabs just the names
        names.append(exercise["Activity, Exercise or Sport (1 hour)"])
    for index in range(len(names)):
        if query in names[index]:
            # grabs the name and the calories burned per kg (then converted to pounds and cut after 3rd decimal) 
            conversion = round(float(all[index]["Calories per kg"]) * 2.20462, 3)
            exercises.append({"exercise":all[index]["Activity, Exercise or Sport (1 hour)"],"calories":conversion})
        if query2 in names[index]:
            conversion = round(float(all[index]["Calories per kg"]) * 2.20462, 3)
            exercises.append({"exercise":all[index]["Activity, Exercise or Sport (1 hour)"],"calories":conversion})
    print(exercises)
    return exercises 
    
    

    
