from typing import List
from time import sleep
from product import Product

from scraper import scrape


def scrapeHokejovaVystroj(url: str) -> List[Product]:
    print('***SCRAPING HOKEJOVA VYSTROJ***')
    products = []
    # Scrape First Page and Get Nexts URL
    while url is not None:
        sleep(1)
        scraped = scrape(url)
        products += scraped[0]
        url = scraped[1]

    return products


# Testing
print(len(scrapeHokejovaVystroj(
    'https://www.hokejovavystroj.sk/hokejova-brankarska-vystroj')))
