__author__ = 'pwidqssg'

from base import CaddiesObject

class Code(CaddiesObject):
    def __init__(self, id, code_scheme_id = None, category_id = None, cs_value = '', cs_order = None):
        self.id = id
        self.code_scheme_id = code_scheme_id
        self.category_id = category_id
        self.cs_value = cs_value
        self.cs_order = cs_order