
class NoCarBrandException(Exception):

    def __init__(self, message):
        self.message = f'Car Brand not found in "{message}"'
        super().__init__(self.message)

class NoAdTitleException(Exception):
    def __init__(self,url):
        super().__init__(f'Add "{url}" doesnt have Title!')
