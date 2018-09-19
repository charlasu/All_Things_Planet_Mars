# Dependencies
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

#Initialize Flask
app = Flask(__name__)

#Initialize MongoDB
mongo = PyMongo(app) #, uri="mongodb://localhost:27017/surfing_app")

#Query MongoDB document and pass data into HTML file
@app.route('/')
def index():
    mars_website = mongo.db.mars_db.find_one()
    return render_template("index.html", mars_website=mars_website)

#Scrape the values and insert into document in the database
@app.route('/scrape')
def scrape():
    #Dictionary of scraped values
    data_dict = mars_scrapes.test()
    #data_dict = mars_scrapes.scrape()

    #Declare the db
    mars_scrapes = mongo.db.mars_db
    
    #Insert/update dict in db
    mars_db.update(
        {},
        data_dict,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)



