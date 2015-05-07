__author__ = 'pwidqssg'

from base import CaddiesObject

class ResponseDomainText(CaddiesObject):
    def __init__(self, id, maxlen = None, label = ''):
        self.id = id
        self.maxlen = maxlen
        self.label = label