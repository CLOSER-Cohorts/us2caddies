__author__ = 'pwidqssg'

from base import CaddiesObject

class CcStatement(CaddiesObject):
    def __init__(self, id, textid = '', statement_item = ''):
        self.id = id
        self.textid = textid
        self.statement_item = statement_item