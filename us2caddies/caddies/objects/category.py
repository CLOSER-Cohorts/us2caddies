__author__ = 'pwidqssg'

from base import CaddiesObject

class Category(CaddiesObject):
    def __init__(self, id, label = ''):
        self.id = id
        self.label = label