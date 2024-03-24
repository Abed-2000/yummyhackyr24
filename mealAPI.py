import requests as req
import re

def getFullMealData(mealID):
    url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i="
    endpoint = url + str(mealID)
    res = req.get(endpoint)
    return res.json()

def getMealName(mealID):
    json = getFullMealData(mealID)
    if json['meals']:
        str_meal = json['meals'][0]['strMeal']
        return str_meal
    else:
        print("Meal not found.")

def getMealCategory(mealID):
    json = getFullMealData(mealID)
    if json['meals']:
        strCategory = json['meals'][0]['strCategory']
        return strCategory
    else:
        print("Meal not found.")

def getMealArea(mealID):
    json = getFullMealData(mealID)
    if json['meals']:
        strArea = json['meals'][0]['strArea']
        return strArea
    else:
        print("Meal not found.")        

def getMealThumb(mealID):
    json = getFullMealData(mealID)
    if json['meals']:
        strMealThumb = json['meals'][0]['strMealThumb']
        return strMealThumb
    else:
        print("Thumbnail not found.")

def getInstructions(mealID):
    json = getFullMealData(mealID)
    if json['meals']:
        strInstructions = json['meals'][0]['strInstructions']
        return strInstructions
    else:
        print("Instructions not found.")

def getYoutube(mealID):
    json = getFullMealData(mealID)
    if json['meals']:
        strYoutube = json['meals'][0]['strYoutube']
        return strYoutube
    else:
        print("Instructions not found.")

def extract_youtube_id(url):
    match = re.search(r'(?<=v=)[^&]+', url)
    if match:
        return match.group(0)
    else:
        return None

def getIngredients(mealID):
    json = getFullMealData(mealID)
    if json['meals']:
        ingredientList = []
        for i in range(20):
            ingredient = json['meals'][0]['strIngredient'+ str(i+1)]
            if ingredient == "" or ingredient is None:
                continue
            ingredientList.append(ingredient)
        return ingredientList
    else:
        print("Ingredients not found.")

def getMeasurements(mealID):
    json = getFullMealData(mealID)
    if json['meals']:
        measurementList = []
        for i in range(20):
            measurement = json['meals'][0]['strMeasure'+ str(i+1)]
            if measurement == "" or measurement is None:
                continue
            measurementList.append(measurement)
        return measurementList
    else:
        print("Measurements not found.")

def searchMealsByName(query):
    url = 'https://www.themealdb.com/api/json/v1/1/search.php?s='
    endpoint = url + query
    res = req.get(endpoint).json()
    return res

def getMealsByCategory(query):
    url = "http://www.themealdb.com/api/json/v1/1/filter.php?c="
    endpoint = url + str(query)
    res = req.get(endpoint)
    return res.json()

def getMealCategories():
    url = "http://www.themealdb.com/api/json/v1/1/categories.php"
    try:
        res = req.get(url)
        res.raise_for_status()
        categories_data = res.json()
        category_list = []
        for category_data in categories_data['categories']:
            category_name = category_data['strCategory']
            category_list.append(category_name)
        return category_list
    except req.exceptions.RequestException as e:
        print("Failed to fetch categories:", e)
        return []
