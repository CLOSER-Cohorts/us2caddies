__author__ = 'pwidqssg'

import re
import xml.etree.ElementTree as ET

from caddies.builder import Builder
from caddies.objects import *


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
        # os.unlink(self.filepath)

    def extractText(self, node):
        return "".join(node.itertext())

    def readInstance(self):
        self.instance = instance.Instance(id=1, agency='uk.us')
        self.instance.instrument = self.tree.find('.//specification//sd_properties/label').text

    def readQuestion(self, module, xml_q, parent=None):
        literal = xml_q.find('qt_properties/text')
        if literal != None:

            textid = xml_q.get('name').replace('.', '_', 1)

            decimal = xml_q.find('qt_properties/decimals')
            options = xml_q.findall('qt_properties/options/option')

            if (decimal == None and len(options) == 0):
                self.builder.addStatement(textid, self.extractText(literal))
            else:
                question = self.builder.newQuestion(textid, self.extractText(literal))

                instr = xml_q.find('qt_properties/help')
                if instr != None:
                    instr = self.extractText(instr).strip()
                    if instr != '':
                        question.instruction = instr

                if decimal != None:
                    range = xml_q.find('qt_properties/range')
                    if range != None:
                        max = range.get('max')
                        min = range.get('min')
                        question.add_numeric(textid, 'Integer' if self.extractText(decimal) == '0' else 'Float', min,
                                             max)

                for option in options:
                    opt_text = self.extractText(option.find('text'))
                    if opt_text == None or opt_text.strip() == "":
                        opt_text = self.extractText(option.find('label'))
                    question.add_code(option.get('value'), opt_text.strip())

                self.builder.submitQuestion(question, parent)

    def readCondition(self, module, xml_c, parent=None):
        condition = xml_c.find('if/condition')
        if condition == None:
            logic = ""
        else:
            logic = self.extractText(condition)
        label = xml_c.find('if/sd_properties/label')
        if label == None:
            text = "NO CONDITION TEXT"
        else:
            text = self.extractText(label)

        try:
            if logic[:1] == '[' and logic[-1:] == ']':
                logic = logic[1:-1]

            logic = logic.replace('&lt;', '<').replace('&gt;', '>')

            logic_chunks = re.split('([^\w\.])', logic)

            textid = logic_chunks[0].split('.')[0]
            temp = []
            for chunk in logic_chunks:
                chunk = chunk.strip().lower()
                if re.match('^[\w]+$', chunk) != None:
                    found = False
                    for qc in self.builder.cc_question:
                        if qc.textid[-1 * len(chunk):] == chunk:
                            temp.append('qc_' + chunk)
                            found = True
                            break
                    if not found:
                        temp.append(chunk.replace('or', '||').replace('and', '&&'))
                elif chunk == '':
                    pass
                else:
                    temp.append(chunk.replace('|', '||').replace(',', '||').replace('&', '&&'))
            logic_chunks = temp

            logic_expressions = []
            logic_expressions.append([])
            while len(logic_chunks) > 0:
                chunk = logic_chunks.pop(0)
                if chunk == '||' or chunk == '&&' or chunk == '(' or chunk == ')':
                    logic_expressions.append(chunk)
                    logic_expressions.append([])
                elif chunk == '<':
                    if len(logic_chunks) > 0 and logic_chunks[0] == '>':
                        logic_chunks.pop(0)
                        logic_expressions[-1].append('!=')
                    else:
                        logic_expressions[-1].append(chunk)
                else:
                    logic_expressions[-1].append(chunk)

            temp_logic_expressions = []
            for expression in logic_expressions:
                if isinstance(expression, list):
                    if len(expression) > 0:
                        temp_logic_expressions.append(expression)
                else:
                    temp_logic_expressions.append(expression)
            logic_expressions = temp_logic_expressions

            for i in range(len(logic_expressions)):
                if isinstance(logic_expressions[i], list):
                    if len(logic_expressions[i]) == 1 and i > 1:
                        logic_expressions[i] = [logic_expressions[i - 2][0],
                                                logic_expressions[i - 2][1],
                                                logic_expressions[i][0]]

            logic_expressions = [x for x in logic_expressions if isinstance(x, basestring) or (
                (isinstance(x, list) and (x[0][:3] == 'qc_' or x[2][:3] == 'qc_')))]

            i = 0
            while i < len(logic_expressions):
                if isinstance(logic_expressions[i], basestring):
                    if i == 0 or i + 1 >= len(logic_expressions):
                        logic_expressions.pop(i)
                        continue
                    if not isinstance(logic_expressions[i - 1], list) or not isinstance(logic_expressions[i + 1], list):
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

            logic = logic.replace('=', '==').replace('!==', '!=')
        except:
            logic = ''
        text = 'If ' + text + ' [' + logic + ']'

        cond = self.builder.addCondition(textid, text, parent)

        for xml_elem in xml_c.find('if/specification_elements'):
            self.readElement(module, xml_elem, cond)

    def readModule(self, xml_m, parent=None):
        seq = self.builder.addSequence(self.extractText(xml_m.find('rm_properties/label')), parent)

        for xml_elem in xml_m.find('specification_elements'):
            self.readElement(xml_m.get('name'), xml_elem, seq)

    def readDataout(self, module, xml_d, parent=None):
        label = xml_d.find('sd_properties/label')
        pass_down = parent

        if label != None:
            seq = self.builder.addSequence(self.extractText(xml_d.find('sd_properties/label')), parent)
            pass_down = seq

        for xml_elem in xml_d.find('specification_elements'):
            self.readElement(module, xml_elem, pass_down)

    def readSection(self, module, xml_s, parent=None):
        seq = self.builder.addSequence(self.extractText(xml_s.find('sd_properties/label')), parent)

        for xml_elem in xml_s.find('specification_elements'):
            self.readElement(module, xml_elem, seq)

    def readLoop(self, module, xml_l, parent=None):
        loop = self.builder.addLoop('default', '_var', loop_while=xml_l.get('args'), parent=parent)

        for xml_elem in xml_l.find('specification_elements'):
            self.readElement(module, xml_elem, loop)

    def readElement(self, module, element, parent=None):
        if element.tag == 'question':
            self.readQuestion(module, element, parent)
        elif element.tag == 'branch':
            self.readCondition(module, element, parent)
        elif element.tag == 'module':
            self.readModule(element, parent)
        elif element.tag == 'dataout':
            self.readDataout(module, element, parent)
        elif element.tag == 'section':
            self.readSection(module, element, parent)
        elif element.tag == 'loop':
            self.readLoop(module, element, parent)

    def readQRE(self):
        first_module_parent = self.tree.find('.//module/..')
        for xml_elem in list(first_module_parent):
            self.readElement('', xml_elem)

        module = self.tree.find('.//specification_elements/module').get('name')

        # for xml_elem in self.tree.find('.//module/specification_elements/dataout/specification_elements'):
        #    self.readElement(module, xml_elem)

        return self.builder
