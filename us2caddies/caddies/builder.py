__author__ = 'pwidqssg'

from question import Question
from objects.cc_question import CcQuestion
from objects.question_grid import QuestionGird
from objects.question_item import QuestionItem
from objects.cc_question_universe import CcQuestionUniverse
from objects.instruction import Instruction
from objects.qi_rda import QiRda
from objects.qgrid_rda import QgridRda
from objects.category import Category
from objects.code import Code
from objects.code_scheme import CodeScheme
from objects import response_domain_all
from objects import response_domain_code
from objects import response_domain_datetime
from objects import response_domain_numeric
from objects import response_domain_text
from objects import response_unit
from objects import universe

class Builder:
    def __init__(self):
        self.categories = []
        self.cc_all = []
        self.cc_ifthenelse = []
        self.cc_loop = []
        self.cc_question = []
        self.cc_question_universe = []
        self.cc_sequence = []
        self.cc_statement = []
        self.code = []
        self.code_scheme = []
        self.instance = None
        self.instruction = []
        self.qgrid_rda = []
        self.qi_rda = []
        self.question_grid = []
        self.question_item = []
        self.response_domain_all = []
        self.response_domain_code = []
        self.response_domain_datetime = []
        self.response_domain_numeric = []
        self.response_domain_text = []
        self.response_unit = []
        self.universe = []

    def newQuestion(self, textid, literal, type='QuestionItem'):
        return Question(textid, literal, type)

    def submitQuestion(self, question):
        #Instruction
        if question.instruction != None:
            instr_id = None
            for instr in self.instruction:
                if instr.instruction_text == question.instruction:
                    instr_id = instr.id
                    break
            if instr_id == None:
                self.instruction.append(Instruction(len(self.instruction)+1, question.instruction))
                instr_id = self.instruction[-1].id
        else:
            instr_id = None

        #Question Item/Grid
        if question.type == 'QuestionItem':
            self.question_item.append(
                QuestionItem(
                    len(self.question_item)+1,
                    textid='qi_'+question.textid,
                    literal=question.literal
                )
            )
            question = self.question_item[-1]
        elif question.type == 'QuestionGrid':
            self.question_grid.append(
                QuestionGird(
                    len(self.question_grid)+1,
                    textid='qg_'+question.textid,
                    literal=question.literal
                )
            )
            #TODO: Add question grid specific code to builder
            question = self.question_grid[-1]
        else:
            raise Exception('Question type is not recognised.')

        #Attach instruction
        question.instruction_id = instr_id

        #Add response domains
        if len(question.codes) > 0:
            self.code_scheme.append(CodeScheme(len(self.code_scheme)+1, 'cs_q' + question.textid))
            cs_id = self.code_scheme[-1].id
            for qcode in question.codes:
                cat_id = None
                for category in self.categories:
                    if qcode['category'] == category.label:
                        cat_id = category.id
                        break
                if cat_id == None:
                    self.categories.append(Category(len(self.categories)+1, qcode['category']))
                    cat_id = self.categories[-1].id
