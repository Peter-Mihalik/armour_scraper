from re import S
from time import sleep
from typing import List
from bs4 import BeautifulSoup
from numpy import append
import requests

from product import Product
from scraper import scrape
from public import getLinksFromATags


def getLinksFromLandingPage(url: str) -> List[str]:
    print('***Getting Links From Landing Page***')
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.select('.ShopContent > ul > li > a')
    links = getLinksFromATags(a_tags)

    return links


def scrapeElbe(url: str) -> List[Product]:
    print('***SCRAPING ELBE ***')
    products = []
    links = getLinksFromLandingPage(url)
    # Scrape First Page Of Products
    for link in links:
        # Sleep Before Every Scrape
        sleep(1)
        print('***Scraping Piece Of Equipment***')
        scrapedFirstPage = scrape(link)

        products += scrapedFirstPage[0]

        navLinks = scrapedFirstPage[1]
        # If There Are More Than One Pages Scrape Them
        if len(navLinks) != 0:
            for navLink in navLinks:
                # Sleep Before Every Scrape
                sleep(1)
                print('***Scraping Other Page***')
                scrapedOtherPage = scrape(navLink)
                products += scrapedOtherPage

    return products


# Testing
def testing():
    scrapeElbe('https://www.elbe.sk/e-shop/brankarska-vystroj/c-133.xhtml')
