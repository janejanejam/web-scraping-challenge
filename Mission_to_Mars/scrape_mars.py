# Import libraries and dependancies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def news_scrape():
    # Connect function init_browser
    browser = init_browser()
    
    # Set URL to scrape
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    
    # Add time delay
    time.sleep(3)

    # Scrape page into Soup
    news_html = browser.html
    news_soup = bs(news_html, "html5lib")

    # Find latest news title and paragraph
    news_article = news_soup.find_all("div", class_="list_text")[0]

    news_title = news_article.find("div", class_="content_title").text

    news_text = news_article.find("div", class_ ="article_teaser_body").text

    # Close the browser after scraping
    browser.quit()
    
    # Return dictionary of data for database
    return {"news_title": news_title, "news_text": news_text}
    
def image_scrape():
    # Connect function init_browser
    browser = init_browser()
    
    # Set URL to scrape
    image_search = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_search)

    # Click on "FULL IMAGE"
    browser.click_link_by_partial_text("FULL IMAGE")

    # Click on "more info"
    browser.click_link_by_partial_text("more info")

    # Scrape page into Soup
    image_html = browser.html
    image_soup = bs(image_html, "html5lib")

    # Find featured image url
    image_url = image_soup.find("figure", class_="lede").find("a")["href"]
    image_full_url = "https://www.jpl.nasa.gov" + image_url

    # Close the browser after scraping
    browser.quit()
    
    # Return dictionary of data for database
    return {"image_url": image_full_url}

def weather_scrape():
    # Connect function init_browser
    browser = init_browser()
    
    # Set URL to scrape
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    # Add time delay
    time.sleep(5)

    # Scrape page into Soup
    weather_html = browser.html
    weather_soup = bs(weather_html, "html5lib")

    # Find latest news title and paragraph
    weather_art = weather_soup.find_all("article", role="article")[0]
    weather_text = weather_art.find_all("span")[4].text

    # Close the browser after scraping
    browser.quit()
    
    # Return dictionary of data for database
    return {"weather_text": weather_text}

def mars_facts():
    # Set URL variable
    facts_url = "https://space-facts.com/mars/"
    
    # Use Pandas to read html
    table = pd.read_html(facts_url)
    
    # Set variable for table
    fact_table = table[0]
    
    # Set column names
    fact_table.columns = ['Description', 'Value']
    
    # Set index
    fact_table = fact_table.set_index('Description')
    
    # Convert table back to html
    fact_table = fact_table.to_html()
    
    return fact_table

def hemi_scrape():
    # Connect function init_browser
    browser = init_browser()
    
    # Set URL to scrape
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    # Scrape page into Soup
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, "html5lib")
    
    # Find all items with image 
    items = hemi_soup.find_all("div", class_='item')
    
    # Create empty list to append with results from loop
    hemi_list = []

    # Set variable for main url
    main_url = 'https://astrogeology.usgs.gov/'

    # Start loop through items
    for item in items:
        
        # Find hemi title
        hemi_title = item.find("h3").text
        
        # Find url to hemi page
        hi_url = item.find("a")["href"]
        
        # Visit url to scrape
        browser.visit(main_url + hi_url)
        
        # Scrape page into Soup
        hi_html = browser.html
        hi_soup = bs(hi_html, "html5lib")
        
        # Find high res image url
        hemi_image = hi_soup.find("div", class_="wide-image-wrapper").find("img", class_='wide-image')["src"]
        
        # Append list with results as dictionary
        hemi_list.append({"title": hemi_title, "hemi_image": main_url + hemi_image})
    
    # Close the browser after scraping
    browser.quit()
    
    # Return dictionary of data for database
    return hemi_list
