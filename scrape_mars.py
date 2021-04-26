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

    # exclude the print code because it will be returned by the scrape at the end





    driver.close()
    return return_data
    

if __name__ == "__main__":
    print(scrape_info() )