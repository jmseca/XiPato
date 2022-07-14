"""
Useful function
Author: João Fonseca
Date: 15 July 2022
"""

import re

def remove_many_spaces(str):
    '''
    Removes double, triple,... spaces in a string
    '''
    return re.sub(' +',' ',str)

