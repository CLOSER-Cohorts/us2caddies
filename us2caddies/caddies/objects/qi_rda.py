__author__ = 'pwidqssg'

from base import CaddiesObject

class QiRda(CaddiesObject):
    def __init__(self, id, question_item_id = None, response_domain_all_id = None):
        self.id = id
        self.question_item_id = question_item_id
        self.response_domain_all_id = response_domain_all_id