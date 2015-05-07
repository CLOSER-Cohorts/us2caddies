__author__ = 'pwidqssg'

from base import CaddiesObject

class QuestionGird(CaddiesObject):
    def __init__(self, id, textid = '', literal = '', intent = '', vertical_codelist_id = None,
                 vertical_roster_rows = None, vertical_roster_label = '', horizontal_codelist_id = None,
                 corner_label = '', instruction_id = None):
        self.id = id
        self.textid = textid
        self.literal = literal
        self.intent = intent
        self.vertical_codelist_id = vertical_codelist_id
        self.vertical_roster_rows = vertical_roster_rows
        self.vertical_roster_label = vertical_roster_label
        self.horizontal_codelist_id = horizontal_codelist_id
        self.corner_label = corner_label
        self.instruction_id = instruction_id