from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

def initial_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_data():
    browser = initial_browser()

    data_set = {}

    #Scrape Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')
    webpageitems = soup.find_all('div', class_="card-body")[1].text

    #Scrape JPL site
    img_url = 'https://spaceimages-mars.com/image/featured/mars3.jpg'
    browser.visit(img_url)
    img_html=browser.html
    soup_2=bs(html,'html.parser')
    main_url = soup_2.find('img', class_='fancybox-image')['src']
    mainimage_url = 'https://spaceimages-mars.com/'+main_url

    #Scrape Mars Facts
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)
    facts_html=browser.html
    soup_3=bs(facts_html,'html.parser')
    webpageitems = soup_3.find_all('div', class_="card-body")[1].text
    fact_table = pd.read_html(facts_url)
    fact_tabledf = fact_table[1]
    fact_tabledf.columns = ['Descriptor','Fact']
    html_table = fact_tabledf.to_html("table.html", border="1",justify="left")

    #Scrape Mars Hemispheres Data
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    soup_4=bs(hemispheres_html,'html.parser')
    hemisphere_image_urls = []
    items=soup_4.find ('div', class_='result-list')
    hemispheres=items.find_all('div',{'class':'item'})
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + end_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup=bs(html_hemispheres, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title,"img_url": hemispheres_url + image_url})
browser.quit()

