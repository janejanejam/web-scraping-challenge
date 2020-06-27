from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars = mongo.db.mars

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars = mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars = mongo.db.mars

    mars_data = {}

    # Run the scrape function
    print("Start scraping")

    try:
        mars_data['news'] = scrape_mars.news_scrape()
    except Exception as e:
        print("Fail to scrape news")
        raise e

    try:
        mars_data['image'] = scrape_mars.image_scrape()
    except:
        print("Fail to scrape image")

    try:
        mars_data['weather'] = scrape_mars.weather_scrape()
    except:
        print("Fail to scrape weather")

    try:
        mars_data['facts'] = scrape_mars.mars_facts()
    except:
        print("Fail to scrape facts")

    try:
        mars_data['hemi'] = scrape_mars.hemi_scrape()
    except:
        print("Fail to scrape hemi")

    print("End scrape")

    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
