__author__ = 'pwidqssg'

from base import CaddiesObject

class QuestionItem(CaddiesObject):
    def __init__(self, id, textid = '', literal = '', intent = '', instruction_id = None):
        self.id = id
        self.textid = textid
        self.literal = literal
        self.intent = intent
        self.instruction_id = instruction_id