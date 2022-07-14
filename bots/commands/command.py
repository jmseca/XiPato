"""
Defining Bots commands
Author: João Fonseca
Date: 14 July 2022
"""

class XiPatoCommand:

    def __init__(self, name, descr):
        self.name = name.lower()
        self.descr = descr

    def get_doc(self):
        doc = '== {} ==\n'.format(self.name.upper())
        doc += (self.descr)
        return doc



class XiPatoComplexCommand(XiPatoCommand):

    def __init__(self, name, **subcs):
        super().__init__(name)
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

class Show(XiPatoComplexCommand):

    def __init__(self):
        super().__init__('show',
        type=['all','unseen','info'],
        limit=['any natural number'],
        order=['return','roi','price'],
        order_type=['-a','-d'])

    



