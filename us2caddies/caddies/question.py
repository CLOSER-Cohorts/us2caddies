__author__ = 'pwidqssg'

from objects import cc_question
from objects import question_grid
from objects.question_item import QuestionItem
from objects import cc_question_universe
from objects import instruction
from objects import qi_rda
from objects import qgrid_rda
from objects import category
from objects import code
from objects import code_scheme
from objects import response_domain_all
from objects import response_domain_code
from objects import response_domain_datetime
from objects import response_domain_numeric
from objects import response_domain_text
from objects import response_unit
from objects import universe

class Question:
    def __init__(self, textid, literal, type='QuestionItem'):
        self.textid = textid
        self.literal = literal
        self.type = type
        self.codes = []
        self.rd = []
        self.instruction = None

        self.X = []
        self.Y = []

    def add_code(self, val, text):
        self.codes.append({'cs_value': val, 'category': text})

    def add_X_code(self, text):
        self.X.append({'label': text})
        return self.X[-1]

    def add_Y_code(self, text):
        self.Y.append({'label': text})
        return self.Y[-1]

    def add_text(self, name, maxlen = None):
        self.rd.append({'type': 'Text' ,'label': name})
        if not maxlen == None:
            self.rd[-1]['maxlen'] = maxlen

    def add_numeric(self, name, type='Integer', min_val=None, max_val=None):
        self.rd.append({'label': name, 'type': type})
        if not min_val == None:
            self.rd[-1]['min'] = min_val
        if not max_val == None:
            self.rd[-1]['min'] = max_val

    def add_datetime(self, name, type='Date', format=''):
        self.rd.append({'label': name, 'type': type, 'format': format})

    def add_instruction(self, text):
        self.instruction = text

    def get_built_objects(self):
        if self.type == 'QuestionItem':
            obj = {}
            obj['question_item'] = QuestionItem(id=0, textid='qi_'+self.textid, )
        elif self.type == 'QuestionGrid':
            pass
        else:
            raise StandardError('Unknown Caddies question type')