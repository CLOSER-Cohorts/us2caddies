__author__ = 'pwidqssg'

import re

class CaddiesObject(object):

    def get_table_name(self):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower() + 's'