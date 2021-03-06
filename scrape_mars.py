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

# def init_browser():
#     executable_path = {'executable_path':'chromedriver'}
#     return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # browser = init_browser()
    mars_data_dict = {}

    # mars news code
    # connect to URL
    nasa_url = 'https://mars.nasa.gov/news/'
    driver.get(nasa_url)
    # browser.visit(nasa_url)
    # set up parser
    # html = browser.html
    html = driver.page_source
    soup = bs(html, 'lxml')
    # soup = bs(html, 'html.parser')
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
    driver.get(image_url)

    html = driver.page_source
    soup_img = bs(html, 'lxml')

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
    mars_comparison_html = mars_comparison.to_html()
    mars_comparison_html.replace('\n','')


    # mars hemisphere data 
    astrogeo_url = 'https://astrogeology.usgs.gov'
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    driver.get(hemi_url)
    hemi_html = driver.page_source
    soup_geo = bs(hemi_html, 'lxml')
    # use beautiful soup to find all data for each hemisphere
    hemisphere_path = soup_geo.find('div', class_='collapsible results')
    hemisphere_data = hemisphere_path.find_all('div', class_='item')

    #make an empty list for the urls

    hemisphere_url_list = []

    #loop through the data for each hemisphere to scrape the target data
    #title is under h3 in the inspect pane
    for h in hemisphere_data:
    #     title
        title =h.find('h3').text
    #     image link
        hemis = h.find('div', class_= "description")
        hemi_link = hemis.a['href']
        driver.get(astrogeo_url + hemi_link)    
        html = driver.page_source
        soup_hemi = bs(html, 'lxml')   
        img_path = soup_hemi.find('div', class_='downloads')
        img_url = img_path.find('li').a['href']

        # make dictionary for title and url
        hemi_dict = {}
        hemi_dict['title'] = title
        hemi_dict['img_url'] = img_url
        hemisphere_url_list.append(hemi_dict)
    

    mars_data_dict = {
        "news_title": news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_comparison_html" : mars_comparison_html,
        "hemisphere_url_list" : hemisphere_url_list

    }



    driver.close()
    return mars_data_dict
    

if __name__ == "__main__":
    print(scrape_info() )