__author__ = 'pwidqssg'

import re
import xml.etree.ElementTree as ET
from caddies.objects import *
from caddies.builder import Builder

class USReader:

    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = ET.parse(self.filepath)
        self.builder = Builder()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        pass
        #os.unlink(self.filepath)

    def readInstance(self):
        self.instance = instance.Instance(id=1, agency= 'uk.us')
        self.instance.instrument = self.tree.find('.//module/rm_properties/label').text

    def readQuestion(self, module, xml_q, parent= None):
        literal = xml_q.find('qt_properties/text')
        if literal != None:
            textid = xml_q.get('name').replace(module+'.','',1)

            decimal = xml_q.find('qt_properties/decimals')
            options = xml_q.findall('qt_properties/options/option')

            if (decimal == None and len(options) == 0):
                self.builder.addStatement(textid, literal.text)
            else:
                question = self.builder.newQuestion(textid, literal.text)

                instr = xml_q.find('qt_properties/help')
                if instr != None:
                    instr = instr.text.strip()
                    if instr != '':
                        question.instruction = instr

                if decimal != None:
                    range = xml_q.find('qt_properties/range')
                    if range != None:
                        max = range.get('max')
                        min = range.get('min')
                        question.add_numeric(textid, 'Integer' if str(decimal.text) == '0' else 'Float', min, max)

                for option in options:
                    opt_text = option.find('text').text.strip()
                    if opt_text == None or opt_text == "":
                        opt_text = option.find('label').text.strip()
                    question.add_code(option.get('value'), opt_text)

                self.builder.submitQuestion(question, parent)

    def readCondition(self, module, xml_c, parent = None):
        logic = xml_c.find('if/condition').text
        text = xml_c.find('if/sd_properties/label').text

        logic = logic.replace('=','==').replace('<>','!=')[1:-1]
        logic_chunks = re.split('([^\w\.]+)', logic)
        textid = logic_chunks[0].split('.')[0]
        temp = []
        for chunk in logic_chunks:
            chunk = chunk.strip()
            if re.match('^[\w]+$', chunk) != None:
                found = False
                for qc in self.builder.cc_question:
                    if qc.textid == 'qc_' + chunk:
                        temp.append('qc_' + chunk)
                        found = True
                        break
                if not found:
                    temp.append(chunk)
            elif chunk == '':
                pass
            else:
                temp.append(chunk.replace('|','||').replace('&','&&'))
        logic_chunks = temp

        logic_expressions = []
        logic_expressions.append([])
        while len(logic_chunks) > 0:
            chunk = logic_chunks.pop(0)
            if chunk == '||' or chunk == '&&':
                logic_expressions.append(chunk)
                logic_expressions.append([])

            else:
                logic_expressions[-1].append(chunk)

        for i in range(len(logic_expressions)):
            if isinstance(logic_expressions[i], list):
                if len(logic_expressions[i]) == 1 and i > 1:
                    logic_expressions[i] = [logic_expressions[i-2][0],
                                            logic_expressions[i-2][1],
                                            logic_expressions[i][0]]

        logic_expressions = [x for x in logic_expressions if isinstance(x, basestring) or ((isinstance(x, list) and (x[0][:3] == 'qc_' or x[2][:3] == 'qc_')))]

        i = 0
        while i < len(logic_expressions):
            if isinstance(logic_expressions[i], basestring):
                if i == 0 or i+1 >= len(logic_expressions):
                    logic_expressions.pop(i)
                    continue
                if not isinstance(logic_expressions[i-1], list) or not isinstance(logic_expressions[i+1], list):
                    logic_expressions.pop(i)
                    continue
            i += 1

        for expr in logic_expressions:
            if (isinstance(expr, basestring)): continue
            if (expr[0][:3] == 'qc_' and expr[2][:3] == 'qc_'): continue
            if (expr[0][:3] == 'qc_'):
                qref = expr[0]
                val = expr[2]
            else:
                qref = expr[2]
                val = expr[0]

            for quest in self.builder._submitted_questions:
                if 'qc_' + quest.textid == qref:
                    if len(quest.codes) > 0:
                        pass
                    elif len([x for x in quest.rd if x['type'] == 'Text']):
                        val = '"' + val + '"'
                    elif len([x for x in quest.rd if x['type'] == 'Integer' or x['type'] == 'Float']):
                        val = "'" + val + "'"
            expr[0] = qref
            expr[2] = val

        logic_expressions = [' '.join(x) if isinstance(x, list) else x for x in logic_expressions]
        logic = ' '.join(logic_expressions)

        text = 'If ' + text + ' [' + logic + ']'

        cond = self.builder.addCondition(textid, text, parent)

        for xml_elem in  xml_c.find('if/specification_elements'):
            self.readElement(module, xml_elem, cond)

    def readElement(self, module, element, parent=None):
        if element.tag == 'question':
            self.readQuestion(module, element, parent)
        elif element.tag == 'branch':
            self.readCondition(module, element, parent)

    def readQRE(self):
        module = self.tree.find('.//specification_elements/module').get('name')

        for xml_elem in self.tree.find('.//module/specification_elements/dataout/specification_elements'):
            self.readElement(module, xml_elem)

        return self.builder