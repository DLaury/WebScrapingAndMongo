from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html using mongo DB
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)


# Route to trigger scrape function
@app.route("/scrape")
def scraper():
    
    mars_data = mongo.db.mars_data

    # Run the scrape function
    mars_info = scrape_mars.scrape()

    # Update the database with mars_data
    mars_data.update({}, mars_info, upsert=True)
    
    # Go back to the home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
