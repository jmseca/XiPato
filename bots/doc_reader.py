

from email import message


class DocReader:
    '''
    Reads doc files
    Warning, doc files must be in the same dir as the doc reader
    '''

    def __init__(self,file):
        self.file = file
        
    

class XiPatoDocReader(DocReader):

    def __init__(self, file):
        super().__init__(file)

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

        
            

