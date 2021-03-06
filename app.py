from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection


mongo = PyMongo(app, uri="mongodb://localhost:27017/app_name")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # # Find one record of data from the mongo database
    mars_data_dict= mongo.db.collection.find_one() 
    print(mars_data_dict.keys())
    # # Return template and data
    return render_template("index.html", mars=mars_data_dict)
    


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # data = scrape.scrape_info()
    
    # use mongo update to upsert data
    # mars_data_dict = mongo.db.mars_data_dict
    mars_data = scrape_mars.scrape_info()
    mongo.db.collection.update({}, mars_data, upsert=True)


    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
