class CarAd:
    id = 0
    def __init__(self,url,price, roi):
        self.id = CarAd.id
        self.url = url
        self.seen = False
        self.send_message = False
        self.message_sent = False
        CarAd.id += 1
        self.price = price
        self.roi = roi


    def __str__(self):
        return "{}\nID:\t{}\n".format(self.url,self.id)


    def get_return(self):
        return self.price*(1+self.roi)-self.price

    def get_roi(self):
        return self.roi

    
    