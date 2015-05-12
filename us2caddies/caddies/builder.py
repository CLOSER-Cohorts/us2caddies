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
from objects.response_domain_all import ResponseDomainAll
from objects.response_domain_code import ResponseDomainCode
from objects.response_domain_datetime import ResponseDomainDatetime
from objects.response_domain_numeric import ResponseDomainNumeric
from objects.response_domain_text import ResponseDomainText
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
        #self.instance = None
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

    def buildRDC(self, codes, textid):
        self.code_scheme.append(
            CodeScheme(
                len(self.code_scheme)+1,
                'cs_q' + textid
            )
        )
        cs_id = self.code_scheme[-1].id
        order = 0
        for qcode in codes:
            order += 1
            cat_id = None
            for category in self.categories:
                if qcode['category'] == category.label:
                    cat_id = category.id
                    break
            if cat_id == None:
                self.categories.append(
                    Category(
                        len(self.categories)+1,
                        qcode['category']
                    )
                )
                cat_id = self.categories[-1].id

            self.code.append(
                Code(
                    len(self.code)+1,
                    cs_id,
                    cat_id,
                    qcode['cs_value'],
                    order
                )
            )

        self.response_domain_code.append(
            ResponseDomainCode(
                len(self.response_domain_code)+1,
                cs_id
            )
        )
        rdc_id = self.response_domain_code[-1].id
        self.response_domain_all.append(
            ResponseDomainAll(
                len(self.response_domain_all)+1,
                3,
                rdc_id,
                'ResponseDomainCode'
            )
        )
        return self.response_domain_all[-1].id

    def buildRDs(self, rds):
        rdas = []
        for rd in rds:
            if rd['type'] == 'Text':
                self.response_domain_text.append(
                    ResponseDomainText(
                        id = len(self.response_domain_text)+1,
                        maxlen = rd['maxlen'],
                        label = rd['label']
                    )
                )
                self.response_domain_all.append(
                    ResponseDomainAll(
                        id = len(self.response_domain_all)+1,
                        response_domain_type_id = 1,
                        domain_id = self.response_domain_text[-1].id,
                        domain_type = 'ResponseDomainText'
                    )
                )
                rdas.append(self.response_domain_all[-1].id)
            elif rd['type'] == 'Integer' or rd['type'] == 'Float':
                self.response_domain_numeric.append(
                    ResponseDomainNumeric(
                        id = len(self.response_domain_numeric)+1,
                        numeric_type_id = 1 if rd['type'] == 'Integer' else 2,
                        min = rd['min'],
                        max = rd['max'],
                        label = rd['label']
                    )
                )
                self.response_domain_all.append(
                    ResponseDomainAll(
                        id = len(self.response_domain_all)+1,
                        response_domain_type_id = 2,
                        domain_id = self.response_domain_numeric[-1].id,
                        domain_type = 'ResponseDomainNumeric'
                    )
                )
                rdas.append(self.response_domain_all[-1].id)
            elif rd.type == 'Date' or rd.type == 'Time' or rd.type == 'Duration':
                self.response_domain_datetime.append(
                    ResponseDomainDatetime(
                        id = len(self.response_domain_datetime)+1,
                        datetime_type_id = 1 if rd.type == 'Date' else 2 if rd.type == 'Time' else 3,
                        format = rd['format'],
                        label = rd['label']
                    )
                )
                self.response_domain_all.append(
                    ResponseDomainAll(
                        id = len(self.response_domain_all)+1,
                        response_domain_type_id = 4,
                        domain_id = self.response_domain_datetime[-1].id,
                        domain_type = 'ResponseDomainDatetime'
                    )
                )
                rdas.append(self.response_domain_all[-1].id)
            else:
                Exception('Response domain type not recognised.')

        return rdas

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
            cad_question = self.question_item[-1]

            #Add response domains
            rda_ids = []
            if len(question.codes) > 0:
                rda_ids.append(self.buildRDC(question.codes, question.textid))

            if len(question.rd) > 0:
                rda_ids = rda_ids + self.buildRDs(question.rd)

            for rda_id in rda_ids:
                self.qi_rda.append(QiRda(len(self.qi_rda)+1, cad_question.id, rda_id))

        elif question.type == 'QuestionGrid':
            self.question_grid.append(
                QuestionGird(
                    len(self.question_grid)+1,
                    textid='qg_'+question.textid,
                    literal=question.literal
                )
            )
            cad_question = self.question_grid[-1]

            #TODO: Add question grid specific code to builder
        else:
            raise Exception('Question type is not recognised.')

        #Attach instruction
        cad_question.instruction_id = instr_id