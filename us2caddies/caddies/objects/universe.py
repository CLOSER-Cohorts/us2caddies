__author__ = 'pwidqssg'

from base import CaddiesObject

class Universe(CaddiesObject):
    def __init__(self, id, univ_text = ''):
        self.id = id
        self.univ_text = univ_text