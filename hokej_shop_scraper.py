from typing import List
from time import sleep
from product import Product

from scraper import scrape

def scrapeHokejShop(url:str) -> List[Product]:
    print('***SCRAPING HOKEJ SHOP***')
    products = []
    # Scrape Firt Page
    print('***Scrapinf Page Number (1)***')
    firstScrape = scrape(url)
    products += firstScrape[0]
    # Scrape Other Pages
    numberOfPages = firstScrape[1]
    i = 1
    while i < numberOfPages:
        print(f'***Scraping Page Number ({i + 1})***')
        sleep(1)
        newUrl = url + f'strana-{i+1}/'

        products += scrape(newUrl)[0]

        i += 1
    
    return products

# Testing
def testing():
    print(len(scrapeHokejShop('https://www.hokejshop.eu/hokejova-brankarska-vystroj/')))