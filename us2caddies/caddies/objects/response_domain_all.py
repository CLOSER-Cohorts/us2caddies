__author__ = 'pwidqssg'

from base import CaddiesObject

class ResponseDomainAll(CaddiesObject):
    def __init__(self, id, response_domain_type_id = None, domain_id = None, domain_type = ''):
        self.id = id
        self.response_domain_type_id = response_domain_type_id
        self.domain_id = domain_id
        self.domain_type = domain_type