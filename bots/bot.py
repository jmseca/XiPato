"""
Defining Bots classes
Author: João Fonseca
Date: 12 July 2022
"""

from click import command
import requests
from ads import *
from doc_reader import *


class TelBot:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def __init__(self, api_key):
        self.api_key = api_key
        self.updade_id = 0
        self.url = 'https://api.telegram.org/bot{}/'.format(self.api_key)

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



class PrivateTelBot(TelBot):

    def __init__(self, api_key, client_id):
        super().__init__(api_key)
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
        super().__init__(api_key,client_id)
        self.reader = XiPatoDocReader('xipato_bot_docs.txt')
        self.ads = []

    # COMMANDS DOCS

    def send_help(self):
        message = self.reader.get_command('help')
        commands = filter(lambda x:x[-7:]=='command', dir(XiPatoBot))
        for command in commands:
            message += (command.split('_')[0]+'\n')
        self.send_message(message)

    def send_show_help(self):
        message = self.reader.get_command('show')
        self.send_message(message)

    def send_ads_data(self):
        num_adds = len(self.ads)
        unseen_ads = self.get_unseen_ads()
        message = "== ADS ==\n"
        message+='Total:\t{}\n'.format(num_adds)
        message+='Unseen:\t{}\n'.format(unseen_ads)
        message+='\nUse \'help\' for HELP'
        self.send_message(message)

    # End Of commands documentation 


    def add_new_ad(self,url):
        self.ads = [CarAd(url)]


    

    
