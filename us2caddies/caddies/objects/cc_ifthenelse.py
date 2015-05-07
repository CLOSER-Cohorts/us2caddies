__author__ = 'pwidqssg'

from base import CaddiesObject

class CcIfthenelse(CaddiesObject):
    def __init__(self, id , textid = '', condition = ''):
        self.id = id
        self.textid = textid
        self.condition = condition