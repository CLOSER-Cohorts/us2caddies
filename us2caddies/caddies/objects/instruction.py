__author__ = 'pwidqssg'

from base import CaddiesObject

class Instruction(CaddiesObject):
    def __init__(self, id, instruction_text = ''):
        self.id = id
        self.instruction_text = instruction_text