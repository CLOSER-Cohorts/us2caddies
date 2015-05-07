__author__ = 'pwidqssg'

from base import CaddiesObject

class ResponseDomainDatetime(CaddiesObject):
    def __init__(self, id, datetime_type_id = None, label = '', format = ''):
        self.id = id
        self.datetime_type_id = datetime_type_id
        self.label = label
        self.format = format