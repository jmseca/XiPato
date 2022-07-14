"""
Defining Bots classes
Author: João Fonseca
Date: 12 July 2022
"""

import time
import requests
from ads import *
from classex import *
from utils import *


class TelBot:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def __init__(self, api_key,parser):
        self.api_key = api_key
        self.parser = parser
        self.updade_id = 0
        self.url = 'https://api.telegram.org/bot{}/'.format(self.api_key)
        self.commands = [Help(self)]

    def add_commands(self, *new_commands):
        self.commands += new_commands

    def get_commands(self, no_help=False):
        if no_help:
            return self.commands[1:] #assumes help is the [0]
        else: 
            return self.commands

    def send_message(self, message, client_id):
        url = self.url+'sendMessage'
        params = {"chat_id" : client_id, 'text': message}
        return requests.get(url,params = params ,headers=TelBot.headers).json()['ok']

    def parse_bot_updates(self, results, remove, from_id):
        high_update_id = self.update_id
        updates = []
        for result in results:
            uid = result['update_id']
            chat_id = result['message']['chat']['id']
            if from_id=='all' or from_id==chat_id:
                message = result['message']['message']
                date = result['message']['date']
                updates += [[message,chat_id, date]]
            if remove:
                high_update_id = max(high_update_id,uid)
        self.updade_id = high_update_id
        return updates


    def get_updates(self,remove=True,from_id='all'):
        '''
        Checks for new upgrades (new messages)
        updates: list with the following elements: [text, chat_id, date]
        Can only see updates for all or for one (does not support "some ids")
        '''
        updates = []
        url = self.url+'getUpdates'
        params = {'offset':self.upgrade_id}
        response = requests.get(url, params=params ,headers=TelBot.headers).json()
        if response['ok']:
            updates = self.parse_bot_updates(response['result'],remove,from_id)
        return updates

    def execute_request(self, message):
        message_sep = remove_many_spaces(message).split(' ')
        command = message_sep[0].lower()
        for com in self.commands:
            if com.name == command:
                com.execute(message_sep[1:])
                break


    def polling(self,remove=True,from_id='all'):
        while 1:
            try:
                updates = self.get_updates(remove,from_id)
                for update in updates:
                    message = update[0]
                    # Not using id [1] nor time [2]
                    self.execute_request(message)
            except NotImplementedError as e:
                raise e
            except:
                pass
            time.sleep(5)
            """Falta mudar este time para funcionar com as horas do dia"""

    



class PrivateTelBot(TelBot):

    def __init__(self, api_key, parser, client_id):
        super().__init__(api_key, parser)
        self.client_id = client_id

    def send_message(self, message):
        return super().send_message(message,self.client_id)

    def get_updates(self, remove=True):
        return super().get_updates(remove, self.client_id)


class XiPatoBot(PrivateTelBot):
    """
    CAUTION: All commands must have a function called <command_name>_command
    Otherwise, the help documentation will not function properly
    """


    def __init__(self, api_key, client_id):
        super().__init__(api_key, XiPatoParser(), client_id)
        self.reader = XiPatoDocReader('xipato_bot_docs.txt')
        self.ads = []
            

    def add_new_ad(self,url):
        self.ads = [CarAd(url)]


    

    
