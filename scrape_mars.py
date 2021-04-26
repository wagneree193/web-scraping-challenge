from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import requests
import os
import pandas as pd

from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path':'chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    browser = init_browser()
    mars_data_dict = {}

    # mars news code
    # connect to URL
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    # set up parser
    html = browser.html
    soup = bs(html, 'html.parser')
    #get most recent news article title and paragraph
    #calling 0th element ensures you will get the first title
    #go to the inspector pane on the web page to find the class for the header and the paragraph
    news_title = soup.find_all('div', class_='content_title')[0].text

    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # exclude the print command because it will be returned by the scrape at the end

    # space images code
    #JPL Mars Featured Image 
    jpl_url = 'https://www.jpl.nasa.gov'
    image_url = "https://www.jpl.nasa.gov/images?search=&category=Mars"
    browser.visit(image_url)

    html = browser.html
    soup_img = bs(html, 'html.parser')

    #get relative image path from the search page
    relative_url = soup_img.find_all('img')[2]["src"]
    #add search result to get the featured image path
    featured_image_url = image_url + relative_url
    # exclude print command

    # mars data table
    #Mars facts
    # scrape the fact table using pandas
    facts_url = 'https://space-facts.com/mars/'
    fact_table = pd.read_html(facts_url)
    
    mars_comparison = fact_table[1]
    mars_comparison_html.replace('\n','')

    # mars hemisphere data 
    astrogeo_url = 'https://astrogeology.usgs.gov'
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemi_url)
    hemi_html = browser.html
    soup_geo = bs(hemi_html, 'html.parser')




    driver.close()
    return mars_data_dict
    

if __name__ == "__main__":
    print(scrape_info() )