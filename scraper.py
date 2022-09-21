from re import A
from typing import List
from unicodedata import category
from numpy import append
import requests
from bs4 import BeautifulSoup

from product import Product
from public import getLinksFromATags, getSrcFromImgs


def deleteDuplicates(links: List[str]) -> List[str]:
    new = []
    i = 0
    while i < len(links):
        if i != 0:
            link = links[i].split('/')[-1]
            previousLink = links[i - 1].split('/')[-1]

            if link != previousLink:
                new.append(links[i])
        i += 1
    return new


def chooseCategory(name: str) -> str:
    if 'hokejka' in name:
        category = 'hokejka'
    elif 'prilba' in name:
        category = 'prilba'
    elif 'betóny' in name:
        category = 'betony'
    elif 'korčule' in name:
        category = 'korcule'
    elif 'vyražačka' in name or 'lapačka' in name:
        category = 'lapacka a vyrazacka'
    elif 'nohavice' in name:
        category = 'nohavice'
    elif 'vesta' in name:
        category = 'vesta'
    else:
        category = 'prislusenstvo'

    return category


def scrape(url) -> List:
    items = []
    response = requests.get(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    if 'elbe' in url:
        # Find out how many pages with products there are on the site
        pagesNav = soup.select('.ShopCategoryPages > ul > li > a')
        pagesNav = list(set(pagesNav))
        navLinks = getLinksFromATags(pagesNav)
        # Check witch site are we scraping - Diferent sites has diferent components
        # Get Basic Data About Products
        products = soup.select('div.ProductImage > a')
        prices = soup.find_all('span', itemprop='price')
        categories = soup.find_all('p', {'class': 'in-category'})
        for index, product in enumerate(products):
            link = product['href']
            print(f'***Scraping Product ({link})***')
            img = 'https://www.elbe.sk' + product.find('img')['src']
            title = product.find('img')['title']
            price = prices[index]
            category = categories[index]

            items.append(Product(title, link, price.text,
                         img, '', category.text, 'elbeSK'))
        return [items, navLinks]

    elif 'bauer' in url:
        # Scrape product page
        print(f'***Scraping Product ({url})***')
        name = soup.select_one('.product-namee').text
        try:
            # Have to select all and pick second beacause first one is logo
            img = soup.select('.col-sm-6 > img')[1]['src']
        except:
            # Some Products Dont Have Logo
            img = soup.select('.col-sm-6 > img')[0]['src']
        price = soup.select_one('span.price').text
        category = chooseCategory(name)

        items.append(Product(name, url, price, img, '', category, 'bauerSK'))

        return items
    elif 'hokejeshop' in url:
        # Get All Products
        products = soup.select('li.product_item')
        # Get Number Of Pages
        numberOfPages = int(soup.select('.page-list > li')[-2].text)
        # Scrape Info From Each Product
        for product in products:
            link = product.select_one('a.product-thumbnail')['href']
            print(f'***Scraping Product ({link})***')
            img = product.select_one('img')['src']
            name = product.select_one('h3.product-title').text
            price = product.select_one('span.price').text
            category = chooseCategory(name)

            items.append(Product(name, link, price, img,
                         '', category, 'hokej eshop sk'))

        return [items, numberOfPages]
    elif 'hokejshop' in url:
        # Gel All Products
        products = soup.select('div#products > div.product')
        # Get Number Of Pages
        try:
            numberOfPages = int(soup.select('.pagination > a')[-1].text)
        except:
            numberOfPages = 0
        # Scrape Each Product
        for product in products:
            link = 'https://www.hokejshop.eu' + \
                product.select_one('a.image')['href']
            print(f'***Scraping Product ({link})***')
            name = product.select_one('a.name').text.strip()
            img = product.select_one('a.image > img')['src']
            price = product.select_one('.price').text.strip()
            category = chooseCategory(name)

            items.append(Product(name, link, price, img,
                         '', category, 'hokej shop eu'))

        return [items, numberOfPages]
    elif 'hokejovavystroj' in url:
        products = soup.select('div.products__item')
        try:
            nextPage = 'https://www.hokejovavystroj.sk' + soup.select_one(
                'div.toolbar-b__action.toolbar-b__action--page.clearfix > ul > li.next > a')['href']
        except:
            nextPage = None
        for product in products:
            link = 'https://www.hokejovavystroj.sk' + \
                product.select_one('div.product-sm__name > h2 > a')['href']
            print(f'***Scraping Product ({link})***')
            name = product.select_one('div.product-sm__name').text.strip()
            try:
                price = product.select_one(
                    'div.product-sm__price--unit').text.strip()
            except:
                price = 'Navštíviť predajňu'
            img = 'https://www.hokejovavystroj.sk' + \
                product.select_one('.product-sm__img > a > img.image')['src']
            category = chooseCategory(name)
            items.append(Product(name, link, price, img, '',
                         category, 'hokejova vystroj sk'))

        return [items, nextPage]
    elif 'sportobchod' in url:
        products = soup.select('ul#productFilter-productList > li')

        for product in products:
            link = product.select_one('h3.title > a')['href']
            img = product.select_one('span.mainImage > img')['src']
            name = product.select_one('h3.title > span.name').text.strip()
            price = product.select_one('p.price > strong').text.strip()
            print(link, img, name, price)


# Testing
scrape('https://www.sportobchod.sk/hokejova-vystroj/brankar')
