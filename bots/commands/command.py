"""
Defining Bots commands
Author: João Fonseca
Date: 14 July 2022
"""

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


class Show(XiPatoComplexCommand):

    def __init__(self,bot):
        super().__init__(bot,'show',
        '''The 'show' command shows stored ads.
        It follows the following syntax: show [type] [limit] [order] [order_type]''',
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

    def show_info(self):
        num_adds = len(self.bot.ads)
        unseen_ads = len(self.bot.get_unseen_ads())
        message = "== ADS ==\n"
        message+='Total:\t{}\n'.format(num_adds)
        message+='Unseen:\t{}\n'.format(unseen_ads)
        message+='\nUse \'help\' for HELP'
        self.send_message(message)

    def execute(self, subcs_sep):
        flags = self.parse(subcs_sep)
        if flags!=[]:
            ads = self.bot.ads
            ascending = flags[3]==''
            ads_num = 3 if flags[1]=='' else int(flags[1])
            if flags[0]=='info':
                self.show_info()
            else:
                ads = self.get_ads_by_show_type(flags[0])
                if len(ads)>0:
                    ads = self.get_sorted_ads(ads,flags[2],not(ascending))[:ads_num]
                    message = ''
                    for ad in ads:
                        self.bot.send_message(str(ad))
                else:
                    self.bot.send_message('Ads Not Found :(')


    def get_ads_by_show_type(self,type,ads):
        if type == 'all' :
            return ads
        elif type == 'unseen' or type=='':   #DEFAULT
            return list(filter(lambda x:not(x.seen),ads))

    def get_sorted_ads(self, ads, sort_key, reverse):
        if sort_key == 'return' or sort_key=='':  #DEFAULT
            return ads.sort(key=lambda x:x.get_return(), reverse=reverse)
        elif sort_key == 'roi':
            return ads.sort(key=lambda x:x.get_roi(), reverse=reverse)
        elif sort_key == 'price':
            return ads.sort(key=lambda x:x.price, reverse=reverse)


class Help(XiPatoComplexCommand):

    def __init__(self,bot):
        bot_commands = list(map(lambda x:x.name, bot.get_commands(no_help=True)))
        super().__init__(bot,'help',
        '''If you need help with some commands, send help <command>.
        Below are the commands available:''',
        commands=bot_commands)
        
    def execute(self, flags):
        help_flag = flags[0]
        bot_commands = self.bot.get_commands(no_help=True)
        mess = ''
        for com in bot_commands:
            if com.name == help_flag:
                mess = com.get_doc()
                break
        if mess == '':
            self.bot.send_message(mess)
        else:
            self.bot.send_message('Command Not Found :(')
        

    
    

    

    



