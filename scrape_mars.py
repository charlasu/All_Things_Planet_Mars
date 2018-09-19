#THIS IS THE SCRAPE FILE ... I need to clean up directory and file names!!!!


# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo
from splinter import Browser
import requests
import time
#DON'T NEED: from selenium import webdriver

# Initialize chromedriver
#get_ipython().system('which chromedriver')
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# Define scrape function
def scrape():
    browser = init_browser()
    # create mars_data dict to insert into mongoDB
    MarsUpdate = {}

#browser.quit()

# # Scrape News Headlines from NASA

    # Scrape content from Nasa's Mars news site
    url = "https://mars.nasa.gov/news/"

    browser.visit(url)

    html = browser.html

    soup1 = bs(html, 'html.parser')

    news_update = soup1.find('div', class_ = 'list_text')
    news_update

    news_date = news_update.find('div', class_="list_date").text

    news_headline = news_update.find('div', class_="content_title").text

    news_teaser = news_update.find('div', class_="article_teaser_body").text


    MarsUpdate={'news_date': news_date,
               'news_headline': news_headline,
               'news_teaser': news_teaser,
               }

    print(news_date)
    print(news_headline)
    print(news_teaser)


    # # Scrape Images from JPL

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)

    html = browser.html
        
    soup = bs(html, 'html.parser')

    img = soup.find('div', class_='carousel_items')
    img = img.findChild()
    img = img.findAll()
    img = img[0]
    img = img.find('a', class_="button fancybox")
    img = img.attrs['data-fancybox-href']

    MarsUpdate['featureImage'] = img

    #{'feat':img}

    #MarsUpdate


    # # Scrape Weather from Twitter

    url = "https://twitter.com/marswxreport?lang=en"

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')



    #find the div BEFORE you find the paragraph class!!!!! + .get_text() as a splinter command
    #save HTML as a multiline variable with triple quotes
    weather = soup.find('div', class_ = 'js-tweet-text-container')
    # weather = soup_3.find('p', class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    weather
    #for weather in mars_weather:
        
        #print(weather.text)

    MarsUpdate['mars_weather'] = weather

    #MarsUpdate


    # # Scrape Factoids from Space Facts

    url = "https://space-facts.com/mars/"

    fact_table = pd.read_html(url)
    fact_table

    type(fact_table)


    mars_facts_df = fact_table[0]
    mars_facts_df.columns = ["Fact Descriptor", "Value"]
    mars_facts_df.head()

    html_mars_facts = mars_facts_df.to_html()
    html_mars_facts


    MarsUpdate['mars_facts'] = mars_facts_df

    #MarsUpdate


    # # Hemisphere Images from USGS

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    hemispheres = ['Cerberus Hemisphere Enhanced',
                  'Schiaparelli Hemisphere Enhanced',
                  'Syrtis Major Hemisphere Enhanced',
                  'Valles Marineris Hemisphere Enhanced']
    links = []

    # [  { title: '', url: '' },  ]
    for hemisphere in hemispheres:
       browser.visit(url)
       time.sleep(5)
       print(f'chrome driver visiting url {url}')
       browser.click_link_by_partial_text(hemisphere)
       time.sleep(5)
       highresMars_html = browser.html
       soup = bs(highresMars_html, "html.parser")
       time.sleep(5)
       image_url_hemisphere = soup.find('div', class_='downloads').a['href']
       image_dict = {}
       image_dict['url'] = image_url_hemisphere
       image_dict['title'] = hemisphere
       links.append(image_dict)

    MarsUpdate['hemisphere_images'] = image_dict

  # MarsUpdate

  #list of the different hemisphere
  #empty list of links
  #pull out of jupyternb, indent then Scrape()function then 

def test():
    return {
        "news_headline": "NASA News Test Healdine",
        "news_teaser": "NASA teaser test text.",
        "img": "featured JPL img", 
        "weather": "Test weather from Twitter",
        "mars_facts": "<table><tr><td>Cool fact 1</td><td>Fact fact fact fact fact</td></tr><tr><td>Cool fact 1</td><td>Fact fact fact fact fact</td></tr><tr><td>Cool fact 1</td><td>Fact fact fact fact fact</td></tr><tr><td>Cool fact 1</td><td>Fact fact fact fact fact</td></tr><tr><td>Cool fact 1</td><td>Fact fact fact fact fact</td></tr></table>"
    }
# For debugging purposes only - when we run "python scrape_mars.py"
if __name__ == "__main__":
    scrape()
