import json
import mealAPI
import warehouseAPI
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    if 'user' in session:
        return render_template("about.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    else:
        return render_template("login.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            result = mealAPI.searchMealsByName(query)
            return render_template("search.html", data=result)
        else:
            return 'No query provided'
    else:
        return render_template("search.html")

@app.route("/recipe/<int:mealID>", methods=['GET'])
def show_recipe(mealID):
    if request.method == 'GET':
        name = mealAPI.getMealName(mealID)
        thumb = mealAPI.getMealThumb(mealID)
        area = mealAPI.getMealArea(mealID)
        category = mealAPI.getMealCategory(mealID)
        instructions = mealAPI.getInstructions(mealID)
        ingredients = mealAPI.getIngredients(mealID)
        measurements = mealAPI.getMeasurements(mealID)
        youtube_link = mealAPI.getYoutube(mealID)
        youtube_id = mealAPI.extract_youtube_id(youtube_link)
        youtube_embed_url = f"https://www.youtube.com/embed/{youtube_id}?autoplay=1&mute=1"
        
        ingredient_list = [{"ingredient": ing, "measurement": meas} for ing, meas in zip(ingredients, measurements)]

        data = {
            'id': mealID,
            'name': name,
            'thumb': thumb,
            'area': area,
            'category': category,
            'instructions': instructions,
            'ingredients': ingredient_list,
            'youtube': youtube_embed_url
        }
        
        return render_template("recipe.html", data=data)
    else:
        return render_template("search.html")

@app.route("/basket/<int:mealID>", methods=['GET', 'POST'])
def show_basket(mealID):
    if request.method == 'GET':
        id = mealID
        name = mealAPI.getMealName(mealID)
        thumb = mealAPI.getMealThumb(mealID)
        ingredients = mealAPI.getIngredients(mealID)
        
        data = {
            'id': int(id),
            'name': name,
            'thumb': thumb,
            'ingredients': ingredients
        }
        return render_template("basket.html", data=data)

@app.route("/recipes")
def allrecipes():
    categories = mealAPI.getMealCategories()
    return render_template("recipes.html", categories = categories)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000), debug=True)

