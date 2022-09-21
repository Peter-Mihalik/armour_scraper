class Product:
    def __init__(self, name, link, price, img, description, category, site) -> None:
        self.name = name
        self.link = link
        self.price = price
        self.img = img
        self.description = description
        self.category = category
        self.site = site
    
    def printOut(self) -> None:
        print(self.name)
        print(self.link)
        print(self.price)
        print(self.img)
        print(self.description)
        print(self.category)
        print(self.site)