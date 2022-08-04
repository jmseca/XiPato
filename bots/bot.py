"""
Defining Bots classes
Author: João Fonseca
Date: 12 July 2022
"""

import time
import requests
from .ads import *
from .commands.command import *
from .classex import *
from .utils import *


class TelBot:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def __init__(self, api_key, sleep_settings):
        self.api_key = api_key
        self.sleep_data = sleep_settings
        self.update_id = 0
        self.url = 'https://api.telegram.org/bot{}/'.format(self.api_key)
        self.commands = [HelpCommand(self), StopCommand(self)]
        self.commands[0].update_commands()

    def add_commands(self, *new_commands):
        self.commands += new_commands
        self.commands[0].update_commands()

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
        high_update_id = 0
        res = False
        updates = []
        for result in results:
            res = True
            uid = result['update_id']
            chat_id = result['message']['chat']['id']
            if from_id=='all' or from_id==chat_id:
                message = result['message']['text']
                date = result['message']['date']
                updates += [[message,chat_id, date]]
            high_update_id = max(high_update_id,uid)
        if remove:
            self.update_id = (high_update_id+1) if res else self.update_id
        return updates


    def get_updates(self,remove=True,from_id='all'):
        '''
        Checks for new upgrades (new messages)
        updates: list with the following elements: [text, chat_id, date]
        Can only see updates for all or for one (does not support "some ids")
        '''
        updates = []
        url = self.url+'getUpdates'
        params = {'offset':self.update_id}
        response = requests.get(url, params=params ,headers=TelBot.headers).json()
        if response['ok']:
            updates = self.parse_bot_updates(response['result'],remove,from_id)
        return updates

    def execute_request(self, message):
        message_sep = remove_many_spaces(message).split(' ')
        command = message_sep[0].lower()
        msg = ''
        for com in self.commands:
            if com.name == command:
                msg = com.execute(message_sep[1:])
                break
        return msg


    def sleep(self):
        time.sleep(abs(self.sleep_data.get_current_sleep()))

    def send_response(self, msg_from_bot,chat_id):
        stop = False
        if msg_from_bot != '':
            if msg_from_bot == 'stop':
                stop = True
                self.send_message('Bot Stopped',chat_id)
            else:
                self.send_message(msg_from_bot,chat_id)
        return stop


    def polling(self,remove=True,from_id='all'):
        stop = False
        while not(stop):
            #try:
            update = []
            updates = self.get_updates(remove,from_id)
            for update in updates:
                message = update[0]
                # Not using id [1] nor time [2]
                msg_from_bot = self.execute_request(message)
                stop = self.send_response(msg_from_bot,update[1])
                if stop:
                    break
                
                
            '''except: 
                print('Algo deu erro')
                if update!=[]:
                    try:
                        self.send_message('An Exception Occurred',update[1])
                    except:
                        pass
                        #write in log
                else:
                    pass
                    #write in log'''
            if not(stop):
                self.sleep()
        

    



class PrivateTelBot(TelBot):

    def __init__(self, api_key, sleep_settings, client_id):
        super().__init__(api_key,sleep_settings)
        self.client_id = client_id

    def send_message(self, message):
        return super().send_message(message,self.client_id)

    def polling(self, remove=True):
        self.send_message('Bot Started')
        super().polling(remove, self.client_id)
        self.send_message('Bot Stopped')

    def sleep(self):
        sleep_now = self.sleep_data.get_current_sleep()
        if sleep_now < 0: #Up Time is Over
            self.send_message('Up Time is Over')
        time.sleep(abs(sleep_now))

    def send_response(self, msg_from_bot,chat_id):
        stop = False
        if msg_from_bot != '':
            if msg_from_bot == 'stop':
                stop = True
            else:
                self.send_message(msg_from_bot)
        return stop


class XiPatoBot(PrivateTelBot):
    """
    CAUTION: All commands must have a function called <command_name>_command
    Otherwise, the help documentation will not function properly
    """
     

    def __init__(self, api_key, client_id):
        super().__init__(api_key, XiPatoDefaultSleep(), client_id)
        self.ads = []
        self.add_commands(UpCommand(self),ShowCommand(self),AdsCommand(self))
        
        self.add_new_ad('abc',1000,0.5)
        self.add_new_ad('abd',2000,0.4)
        self.add_new_ad('abf',700,1.2)
        self.add_new_ad('abg',1200,0.8)
        self.add_new_ad('abh',1100,0.6)
        self.add_new_ad('abj',1050,0.55)
            

    def add_new_ad(self,url,price,roi):
        self.ads += [CarAd(url,price,roi)]
        #TO DO: Inform the user off new ads


    

    
