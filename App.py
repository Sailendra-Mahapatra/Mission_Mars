from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Scrape_mars


# create instance of Flask app

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# Create to render index.html template

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Creating Scrape route, updating mongo data base


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    data = Scrape_mars.scrape()
    mars.update(
        {}, data, upsert=True
    )
    

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)