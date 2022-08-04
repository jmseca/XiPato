
class CarAd:

    def __init__(self, site, brand='a'*20, model='b'*40 ,
        kms=10**6, url='c'*200, year=9999):
        '''
        The use of extra large values is needed, not to overflow the array of ads while writing "asyncly"
        '''
        self.site = site
        self.brand = brand
        self.model = model
        self.price = 10**6
        self.kms = kms
        self.url = url
        self.year = year

    def insert_info(self, brand, model, price, kms, year, url):
        self.brand = brand
        self.model = model
        self.price = price
        self.kms = kms
        self.year = year
        self.url = url