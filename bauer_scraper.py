from typing import List
from bs4 import BeautifulSoup
from time import sleep
import requests

from scraper import scrape
from product import Product
from public import getLinksFromATags


def getButtonsLinks(url:str) -> List[str]:
    print('***Getting Button Links***')
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    a_tags = soup.select('.tlacidlo')
    links = getLinksFromATags(a_tags)

    return links


def getProductLinks(url:str) -> List[str]:
    print('***Getting Product Links***')
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    a_tags = soup.select('a.product-image')
    links = getLinksFromATags(a_tags)

    # Scrape All Pages
    pagesLinks = list(set(getLinksFromATags(soup.select('div.pages > ol > li > a'))))
    
    if len(pagesLinks) != 0:
        for pageLink in pagesLinks:
            sleep(1)
            response = requests.get(pageLink, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')

            a_tags = soup.select('a.product-image')
            links += getLinksFromATags(a_tags)

    return links


def scrapeProducts(productLinks:List[str], alreadySraped) -> List:
    print('***Scraping Products***')
    products = []
    for productLink in productLinks:
        if not productLink in alreadySraped:
            sleep(1)
            products += scrape(productLink)

    return products



def scrapeBauer(url:str) -> List[Product]:
    print('***SCRAPING BAUER***')
    products = []
    alreadySraped = []
    # Scrape Landing Page For Category Links
    sleep(1)
    linksFromLandingPage = getButtonsLinks(url)
    # Scrape Category For Product Links and For SHOW ALL Buttons
    for linkFromLandingPage in linksFromLandingPage:
        sleep(1)
        productLinks = getProductLinks(linkFromLandingPage)
        # Scrape Products On This Page
        products += scrapeProducts(productLinks, alreadySraped)
        alreadySraped += productLinks
        # Scrape SHOW ALL Buttons
        showAllButtonsLinks = getButtonsLinks(linkFromLandingPage)
        for showAllButtonLink in showAllButtonsLinks:
            productLinks = getProductLinks(showAllButtonLink)
            products += scrapeProducts(productLinks, alreadySraped)
    
    return products





# Testing
def testing():
    print(scrapeBauer('https://www.bauerhockey.sk/brankar/ladovy-hokej'))