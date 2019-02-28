# SCRAPE mars

import time
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time

# Replacing the path with machine's actual path to the chromedriver

def init_browser():

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

# Creating dictionary for scraped data

    mars_data = {}

# Accessing Nasa news on mars

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    new_html = browser.html

# Scraping the page into soup

    bsoup = bs(new_html, 'html.parser')

# Find the latest Mars news.

    article = bsoup.find("div", class_="list_text")
    news_p = bsoup.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text

# Adding date, title & summary to dictionary

    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p

# While chromedriver open, going to JPL's Featured Space Image page

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

# Scraping the browser into soup and use soup to find the full resolution image of mars
# Saving image url to a variable `featured_image_url`

    new_html = browser.html
    bsoup = bs(new_html, 'html.parser')
    image = bsoup.find('img', class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url

# Adding the featured image url to the dictionary

    mars_data["featured_image_url"] = featured_image_url


# - From the [Mars Weather twitter](https://twitter.com/marswxreport?lang=en) account scrape the latest Mars weather tweet from the page.
# - Save the tweet text for the weather report.


    twt_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(twt_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    twt = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    twt = twt.replace('pic.twitter.com/1msjBvhiu7','')

# Adding the weather data to dictionary

    mars_data["mars_weather"] = twt

# mars facts

    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)

    grab = pd.read_html(url3)
    mars_data = pd.DataFrame(grab[0])
    mars_data.columns = ['Mars','Data']
    mars_table = mars_data.set_index("Mars")
    marsdata = mars_table.to_html(classes='marsdata')
    marsdata = marsdata.replace('\n', ' ')

# Add the Mars facts table to the dictionary

    mars_data["mars_table"] = marsdata


# Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1 =target&v1=Mars"
    browser.visit(url4)

    new_html = browser.html
    bsoup = bs(new_html, 'html.parser')
    mars_hemisphere=[]

    for item in range(4):
        time.sleep(1)
        images = browser.find_by_tag('h3')
        images[item].click()
        new_html = browser.html
        bsoup = bs(new_html, 'html.parser')
        newContent = bsoup.find("img", class_="wide-image")["src"]
        img_title = bsoup.find("h2", class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ newContent
        dict_list = {"title":img_title,"img_url":img_url}
        mars_hemisphere.append(dict_list)
        browser.back()
    
#print(mars_hemisphere)

# Adding to dictionary

    # mars_data["mars_hemis"] = mars_hemisphere
# Return the dictionary
    return mars_data, mars_hemisphere
