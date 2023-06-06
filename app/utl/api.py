from flask import Flask, session, render_template, request, redirect
import requests 
import json 

# pulling code from 20_restapi

def tester_description(x):
    k = "DEMO_KEY"
    data = requests.get(url = f"https://api.nal.usda.gov/fdc/v1/foods/list?api_key={k}")
    all = json.loads(data.text)
    nutrition = all[1]["foodNutrients"][0]
    print(nutrition)
    # protein = all[x]["foodNutrients"][0] 
    # fats = all[x]["foodNutrients"][1] 
    # carbs = all[x]["foodNutrients"][2] 
    print(len(nutrition))
   
def search(foodName):
    k = "DEMO_KEY"
    url = f"https://api.nal.usda.gov/fdc/v1/foods/list?api_key={k}&query={foodName}"
    data = requests.get(url)
    all = json.loads(data.text)
    foods = []
    for food in all:
        if food["dataType"] == "Branded":
            foods.append({"id":food["fdcId"],"brand":food['brandOwner'], "description":food["description"]})
        else:
            foods.append({"id":food["fdcId"],"brand":"none", "description":food["description"]})
    return foods