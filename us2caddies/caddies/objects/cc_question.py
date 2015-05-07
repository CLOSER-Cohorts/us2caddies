__author__ = 'pwidqssg'

from base import CaddiesObject

class CcQuestion(CaddiesObject):
    def __init__(self, id, textid = '', question_reference_id = None, response_unit_id = None, question_reference_type = ''):
        self.id = id
        self.textid = textid
        self.question_reference_id = question_reference_id
        self.response_unit_id = response_unit_id
        self.question_reference_type = question_reference_type