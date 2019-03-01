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
    news_p = bsoup.find('div', class_='rollover_description_inner').text
    news_title = bsoup.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text

# Accessing JPL's Featured Space Image page

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

# Scraping the browser into soup and use soup to find the full resolution image of mars
# Saving image url to a variable `featured_image_url`

    new_html = browser.html
    bsoup = bs(new_html, 'html.parser')
    image = bsoup.find('img', class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url


# - From the [Mars Weather twitter](https://twitter.com/marswxreport?lang=en) account scrape the latest Mars weather tweet from the page.
# - Save the tweet text for the weather report.


    twt_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(twt_url)
    new_html = browser.html
    bsoup = bs(new_html, 'html.parser')
    twt_rslt = bsoup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    
# Acessing next tweet from the twitter url

    twt_weather = twt_rslt[1].text
    twt_weather_twt = twt_weather.replace('pic.twitter.com/WlR4gr8gpC','')


# Adding the weather data 

    mars_weather = twt_weather_twt

# mars facts

    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)

# Creating data frame

    grab = pd.read_html(url3)
    fact_df = pd.DataFrame(grab[0])
    fact_df = fact_df.rename(columns={0:'Description',1: 'Values'})
    fact_df = fact_df.set_index('Description')
    df_to_html = fact_df.to_html(classes='mars_scrape_info')
    df_to_html = df_to_html.replace("\n"," ")


# Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1 =target&v1=Mars"
    browser.visit(url4)

    new_html = browser.html
    bsoup = bs(new_html, 'html.parser')
    
    image_mars = []

    for item in range(4):
        time.sleep(1)
        images = browser.find_by_tag('h3')
        images[item].click()
        new_html = browser.html
        bsoup = bs(new_html, 'html.parser')
        newContent = bsoup.find("img", class_="wide-image")["src"]
        img_title = bsoup.find("h2", class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ newContent
        img_dict = {"title":img_title,"img_url":img_url}
        image_mars.append(img_dict)
        browser.back()
    

# Adding to dictionary

    mars_data = {
        'News_Title': news_title,
        'News_Heading': news_p,
        'Feature_Image': featured_image_url,
        'Weather': mars_weather,
        'Facts': df_to_html,
        'Hemisphere': image_mars
    }

    browser.quit()
    
    return mars_data
