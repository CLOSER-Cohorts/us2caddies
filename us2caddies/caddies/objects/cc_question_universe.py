__author__ = 'pwidqssg'

from base import CaddiesObject

class CcQuestionUniverse(CaddiesObject):
    def __init__(self, id, cc_question_id = None, universe_id = None):
        self.id = id
        self.cc_question_id = cc_question_id
        self.universe_id = universe_id