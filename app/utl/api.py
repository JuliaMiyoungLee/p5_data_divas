from flask import Flask, session, render_template, request, redirect
import requests 
import json 

def search(foodName):
    k = "DEMO_KEY"
    url = f"https://api.nal.usda.gov/fdc/v1/foods/list?api_key={k}&query={foodName}"
    data = requests.get(url)
    all = json.loads(data.text)
    foods = []
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
                    print(calories_per_100g)
            foods.append({"id":food["fdcId"],"brand":food['brandOwner'], "description":food["description"], "protein":protein, "fat":fat, "carbs":carbs, "calories per 100g": calories_per_100g})
        else:
            for index in range(len(food["foodNutrients"])):
                if food["foodNutrients"][index]["number"] == '203':
                    protein = food["foodNutrients"][index]["amount"]
                if food["foodNutrients"][index]["number"] == '204':
                    fat = food["foodNutrients"][index]["amount"]
                if food["foodNutrients"][index]["number"] == '205':
                    carbs = food["foodNutrients"][index]["amount"]
            foods.append({"id":food["fdcId"],"brand":None, "description":food["description"], "protein":protein, "fat":fat, "carbs":carbs})
    return foods