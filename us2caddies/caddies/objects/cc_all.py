__author__ = 'pwidqssg'

from base import CaddiesObject

class CcAll(CaddiesObject):
    def __init__(self, id, construct_type = '', construct_id = None, parent_id = None, position = None, ifbranch = 'f'):
        self.id = id
        self.construct_type = construct_type
        self.construct_id = construct_id
        self.parent_id = parent_id
        self.position = position
        self.ifbranch = ifbranch
        self._order_counter = 0

    def get_parent_order(self):
        self.order_counter += 1
        return self.order_counter