from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import Scrape_mars
import json

# create instance of Flask app

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# Create to render index.html template

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data, mars_hemisphere = Scrape_mars.scrape()
    mars_hemi = mongo.db.mars_hemi
    # records = json.loads(mars_data.T.to_json()).values()
    # db.myCollection.insert(records)
    # mars.update(
    #     {}, mars_data.to_dict('records'),
    #     upsert=True
    #     )
    mongo.db.mars.drop()
    mongo.db.mars_hemi.drop()
    mars.insert_many(mars_data.to_dict('records'))
    mongo.db.mars_hemi.drop()
    mars_hemi.insert_many(mars_hemisphere)


    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)