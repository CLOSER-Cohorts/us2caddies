__author__ = 'pwidqssg'

from base import CaddiesObject

class ResponseDomainCode(CaddiesObject):
    def __init__(self, id, code_scheme_id = None):
        self.id = id
        self.code_scheme_id = code_scheme_id