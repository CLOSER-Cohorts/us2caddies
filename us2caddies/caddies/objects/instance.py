__author__ = 'pwidqssg'

from base import CaddiesObject

class Instance(CaddiesObject):
    def __init__(self, id, agency = '', version = '', instance='', inst_citation='', resource_package = '',
                 rp_citation = '', purpose = '', purpose_text = '', cc_scheme = '', category_scheme = '',
                 question_scheme = '', ddata_collection = '', instrument = '', top_sequence = ''):
        self.id = id
        self.agency = agency
        self.version = version
        self.instance = instance
        self.inst_citation = inst_citation
        self.resource_package = resource_package
        self.rp_citation = rp_citation
        self.purpose = purpose
        self.purpose_text = purpose_text
        self.cc_scheme = cc_scheme
        self.category_scheme = category_scheme
        self.question_scheme = question_scheme
        self.ddata_collection = ddata_collection
        self.instrument = instrument
        self.top_sequence = top_sequence