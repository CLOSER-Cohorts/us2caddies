__author__ = 'pwidqssg'

from base import CaddiesObject

class QgridRda(CaddiesObject):
    def __init__(self, id, question_grid_id = None, code_id = None, response_domain_all_id = None):
        self.id = id
        self.question_grid_id = question_grid_id
        self.code_id = code_id
        self.response_domain_all_id = response_domain_all_id