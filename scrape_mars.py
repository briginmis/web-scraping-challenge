# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd


def scrape():


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find_all("div", class_="content_title")[0].text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(news_title)
    print(news_p)


    browser.quit()

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # URL of page to be scraped
    images_url = "https://spaceimages-mars.com/"
    browser.visit(images_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    image = soup.find("img", class_ = "headerimage")

    featured_image_url = images_url + image.attrs["src"]

    print(featured_image_url)

    browser.quit()


    facts_url = "https://galaxyfacts-mars.com/"

    facts_table = pd.read_html(facts_url)
    facts_table


    mars_fact = facts_table[1]
    mars_fact = mars_fact.rename(columns={0:"Profile", 1:"Value"})
    mars_fact.set_index("Profile",inplace=True)
    mars_fact

    fact_table=mars_fact.to_html()
    fact_table


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # URL of page to be scraped
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    results = soup.find("div", class_="collapsible results")

    items = results.find_all("div", class_="item")


    for item in items:
        try:
            hem=item.find('div',class_='description')
            title=hem.h3.text
            # Extract image url
            hem_url=hem.a['href']
            browser.visit(hemispheres_url+hem_url)
            html=browser.html
            soup=BeautifulSoup(html,'html.parser')
            image_src=soup.find('li').a['href']
            if (title and image_src):
                # Print results
                print('-'*50)
                print(title)
                print(hemispheres_url+image_src)
            # Create dictionary for title and url
            hem_dict={
                'title':title,
                'image_url':(hemispheres_url+image_src)
            }
            hemisphere_image_urls.append(hem_dict)
        except Exception as e:
            print(e)

    browser.quit()

    hemisphere_image_urls

    # Create connection variable
    conn = 'mongodb://localhost:27017'

    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = client.Mars_db

    # Drops collection if available to remove duplicates
    db.details.drop()

    # Creates a collection in the database and inserts two documents
    mars_data = {
            "news_title":news_title,
            "news_p":news_p,
            "featured_image_url":featured_image_url,
            "fact_table":fact_table,
            "hemisphere_images":hemisphere_image_urls
            }
    
    return mars_data

