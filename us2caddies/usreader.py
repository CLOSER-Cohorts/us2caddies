__author__ = 'pwidqssg'

import os
import xml.etree.ElementTree as ET
from caddies.objects import *

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

    def readConstructs(self):
        self.cc_alls = []
