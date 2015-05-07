__author__ = 'pwidqssg'

from base import CaddiesObject

class ResponseUnit(CaddiesObject):
    def __init__(self, id, text = ''):
        self.id = id
        self.text = text