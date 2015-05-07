__author__ = 'pwidqssg'

from base import CaddiesObject

class CodeScheme(CaddiesObject):
    def __init__(self, id, label = ''):
        self.id = id
        self.label = label