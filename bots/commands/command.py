"""
Defining Bots commands
Author: João Fonseca
Date: 14 July 2022
"""

import requests

class XiPatoCommand:

    def __init__(self, bot, name, descr):
        self.bot = bot
        self.name = name.lower()
        self.descr = descr

    def get_doc(self):
        doc = '== {} ==\n'.format(self.name.upper())
        doc += (self.descr)
        return doc



class XiPatoComplexCommand(XiPatoCommand):

    def __init__(self, bot, name, descr, **subcs):
        super().__init__(bot, name, descr)
        self.subcs = subcs

    def set_subcs(self,**subcs):
        self.subcs = subcs

    def set_subc(self, subc, *vals):
        self.subcs[subc] = list(vals)

    def update_subc(self, subc, *vals):
        self.subcs[subc] += list(vals)

    def get_doc(self):
        doc = (super().get_doc() +'\n\n')
        for subc in self.subcs.keys():
            doc += subc + '\n'
            for val in self.subcs[subc]:
                doc += '- {}\n'.format(val)
            doc += '\n'
        return doc

    def parse(self, subcs_sep):
        raise NotImplementedError

    def execute(self, flags):
        raise NotImplementedError





class HelpCommand(XiPatoComplexCommand):

    def __init__(self,bot):
        super().__init__(bot,'help',
        'If you need help with some commands, send help <command>.\nBelow are the commands available:',
        commands=[])
        
    def update_commands(self):
        bot_commands = list(map(lambda x:x.name, self.bot.get_commands(no_help=True)))
        self.subcs['commands'] = bot_commands

    def execute(self, subcs_sep):
        if subcs_sep!=[]:
            help_flag = subcs_sep[0]
            bot_commands = self.bot.get_commands(no_help=True)
            mess = ''
            for com in bot_commands:
                if com.name == help_flag:
                    mess = com.get_doc()
                    break
            if mess != '':
                return mess
            else:
                return 'Command Not Found :('
        else:
            return self.get_doc()

class StopCommand(XiPatoCommand):

    def __init__(self,bot):
        super().__init__(bot,'stop',
        '''Stops the Bot''')
        
    def execute(self, subcs_sep):
        #Make sure not to reread messages sent at the same time as stop 
        requests.get(self.bot.url+'getUpdates',params={'offset':self.bot.update_id},headers=self.bot.headers)
        return 'stop'

class AdsCommand(XiPatoComplexCommand):

    def __init__(self,bot):
        super().__init__(bot,'ads',
        'The \'ads\' command shows stored ads.\nIt follows the following syntax:\nads [type] [limit] [order] [order_type]',
        type=['unseen','all','info'],
        limit=['any natural number'],
        order=['return','roi','price'],
        order_type=['-a','-d'])

    def parse(self, subcs_sep):
        flags_ordered = ['']*4 #type,limir,order,order_type
        for element in subcs_sep:
            if element in ('all','info','unseen'):
                flags_ordered[0] = element
            elif element.isdigit():
                flags_ordered[1] = element
            elif element in ('price','roi','return'):
                flags_ordered[2] = element
            elif element=='-d':
                flags_ordered[3] = element
            else: #incorrect value
                return []
        return flags_ordered

    def ads_info(self):
        num_adds = len(self.bot.ads)
        unseen_ads = len(list(map(lambda x : not(x.seen),self.bot.ads)))
        message = "== ADS INFO ==\n"
        message+='Total:\t{}\n'.format(num_adds)
        message+='Unseen:\t{}\n'.format(unseen_ads)
        message+='\nUse \'help\' for HELP'
        return message

    def execute(self, subcs_sep):
        flags = self.parse(subcs_sep)
        if flags!=[]:
            ads = self.bot.ads
            ascending = flags[3]==''
            ads_num = 3 if flags[1]=='' else int(flags[1])
            if flags[0]=='info':
                return self.ads_info()
            else:
                ads = self.get_ads_by_type(flags[0])
                if len(ads)>0:
                    ads = self.get_sorted_ads(ads,flags[2],not(ascending))[:ads_num]
                    message = ''
                    for ad in ads:
                        #exception, does not return the msg, sends it
                        self.bot.send_message(str(ad))
                    return ''
                else:
                    return 'Ads Not Found :('


    def get_ads_by_type(self,type):
        if type == 'all' :
            return self.bot.ads
        elif type == 'unseen' or type=='':   #DEFAULT
            return list(filter(lambda x:not(x.seen),self.bot.ads))

    def get_sorted_ads(self, ads, sort_key, reverse):
        if sort_key == 'return' or sort_key=='':  #DEFAULT
            return sorted(ads, key=lambda x:x.get_return(), reverse=reverse)
        elif sort_key == 'roi':
            return sorted(ads,key=lambda x:x.get_roi(), reverse=reverse)
        elif sort_key == 'price':
            return sorted(ads,key=lambda x:x.price, reverse=reverse)

class UpCommand(XiPatoComplexCommand):

    def __init__(self,bot):
        super().__init__(bot,'up',
        'Makes the Bot run in Up Time for <time> minutes\nIt follows the following syntax:\nup [time]',
        time=['any natural number'])

    def execute(self, subcs_sep):
        if subcs_sep!=[] and subcs_sep[0].isdigit():
            up_flag = int(subcs_sep[0])
            self.bot.sleep_data.start_uptime(up_flag)
            if up_flag>0:
                return 'Up Time for {} minutes'.format(up_flag)
        return ''


class ShowCommand(XiPatoComplexCommand):

    def __init__(self,bot):
        super().__init__(bot,'show',
        'Shows information about the bot\nIt follows the following syntax:\nshow [info]',
        info=['sleep'])

    def execute(self, subcs_sep):
        if subcs_sep!=[] and subcs_sep[0] in self.subcs['info']:
            show_flag = subcs_sep[0]
            if show_flag == 'sleep':
                return self.bot.sleep_data.get_sleep_settings()
        return ''


            

    
    

    

    



