__author__ = 'pwidqssg'

from base import CaddiesObject

class CcLoop(CaddiesObject):
    def __init__(self, id, textid = '', loop_variable = '', initial_value = '', end_value = '', loop_while = ''):
        self.id = id
        self.textid = textid
        self.loop_variable = loop_variable
        self.initial_value = initial_value
        self.end_value = end_value
        self.loop_while = loop_while