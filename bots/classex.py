"""
Classex (auXiliar classes) for Xipato Bot
Author: João Fonseca
Date: 13 July 2022
"""

class XiPatoDocReader():

    def __init__(self, file):
        self.file = file

    def find_command(self, command, docs_pointer):
        found = False
        eof = False
        while not(found) or not(eof):
            new_line = docs_pointer.readline()
            if not new_line: #EOF
                eof = True
            else:
                read_command,lines = new_line.split(' ')
                lines = int(lines[:-1])
                if command.lower()==read_command.lower():
                    found = True
                else:
                    for l in range(lines):
                        docs_pointer.readline()
        return 0 if eof else lines

    def get_command(self, command):
        docs = open(self.file,'r')
        command_doc = ''
        lines = self.find_command(command, docs)
        for l in range(lines):
           command_doc += docs.readline
        return command_doc


class Parser:

    def __init__(self,sep,*commands):
        self.commands = list(commands)
        self.sep = sep

    def get_input_message(self, input):
        raise NotImplementedError

    def format_input(self, command, input_sep):
        raise NotImplementedError

    def parse_input(self, input):
        mess = self.get_input_message(input)
        input_sep = input.split(self.sep)
        if input_sep[0] in self.commands:
            return self.format_input(input_sep[0].lower,input_sep[1:])
        else:
            return [0,[]]


class XiPatoParser(Parser):

    """
    CAUTION! All commands must have the function parsec_<command_name>
    """

    def __init__(self):
        parse_commands = filter(lambda x:x[:6]=='parsec', dir(XiPatoParser))
        commands = list(map(lambda x:x.split('_')[1],parse_commands))
        super.__init__(' ',*commands)

    def get_input_message(self, input):
        return input[0]

    def parsec_show(self,input_sep):
        flags_ordered = ['']*4 #type,limir,order,order_type
        for element in input_sep:
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

    def parsec_help(self,input_sep):
        if input_sep != [] and input_sep[0] in self.commands:
            return [input_sep[0]]
        else: 
            return ['']


    def format_input(self,command, input_sep):
        input_str_list = [command]
        if command == 'show':
            add_to = self.parsec_show(input_sep)
        elif command == 'help':
            add_to = self.parsec_help(input_sep)
        #elif command == 'up':
        #    add_to = self.parsec_up(input_sep)
        
        if add_to==[]: #error spoted
            return [0,[]]
        else:
            input_str_list+= add_to
            return [len(input_str_list),input_str_list]

        
        

class DateSettings:

    def __init__(self, time):
        self.time = time



        
            

