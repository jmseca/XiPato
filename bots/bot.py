"""
Defining Bots classes
Author: João Fonseca
Date: 12 July 2022
"""


class TelBot:

    def __init__(self, api_key):
        self.api_key = api_key



class PrivateTelBot(TelBot):

    def __init__(self, api_key, client_id):
        super().__init__(api_key)
        self.client_id = client_id