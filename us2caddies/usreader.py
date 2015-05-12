__author__ = 'pwidqssg'

import os
import xml.etree.ElementTree as ET
from caddies.objects import *
from caddies.builder import Builder

class USReader:

    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = ET.parse(self.filepath)

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

    def readQRE(self):
        builder = Builder()
        module = self.tree.find('.//specification_elements/module').get('name')
        for xml_q in self.tree.findall('.//module/specification_elements/dataout/specification_elements/question'):
            literal = xml_q.find('qt_properties/text')
            if literal != None:
                textid = xml_q.get('name').lstrip(module+'.')
                question = builder.newQuestion(textid, self.scrubString(literal.text))

                decimal = xml_q.find('qt_properties/decimals')
                if decimal != None:
                    range = xml_q.find('qt_properties/range')
                    if range != None:
                        max = range.get('max')
                        min = range.get('min')
                        question.add_numeric(textid, 'Integer' if str(decimal.text) == '0' else 'Float', min, max)

                options = xml_q.findall('qt_properties/options/option')
                for option in options:
                    question.add_code(option.get('value'), self.scrubString(option.find('text').text))

                builder.submitQuestion(question)

        print "Builder created " + str(len(builder.question_item)) + " question items."
        return builder

    def scrubString(self, input):
        output = input.replace('\n',' ').replace('\r',' ')
        return ' '.join(output.split())