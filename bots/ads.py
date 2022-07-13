class CarAd:
    id = 0
    def __init__(self,url):
        self.id = CarAd.id
        self.url = url
        self.seen = False
        self.send_message = False
        self.message_sent = False
        CarAd.id += 1

    def seen(self):
        self.seen = True

    