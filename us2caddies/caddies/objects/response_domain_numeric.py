__author__ = 'pwidqssg'

from base import CaddiesObject

class ResponseDomainNumeric(CaddiesObject):
    def __init__(self, id, numeric_type_id = None, min = None, max = None):
        self.id = id
        self.numeric_type_id = numeric_type_id
        self.min = min
        self.max = max