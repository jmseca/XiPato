
class NoCarBrandException(Exception):

    def __init__(self, message):
        self.message = f'Car Brand not found in "{message}"'
        super().__init__(self.message)

class NoAdTitleException(Exception):
    def __init__(self,url):
        super().__init__(f'Add "{url}" doesnt have Title!')

class NoPriceException(Exception):

    def __init__(self, url):
        super().__init__(f'Add "{url}" doesnt have Price!')

class NoKmsException(Exception):

    def __init__(self, url):
        super().__init__(f'Add "{url}" doesnt have Kms!')

class NoYearException(Exception):

    def __init__(self, url):
        super().__init__(f'Add "{url}" doesnt have Year!')

