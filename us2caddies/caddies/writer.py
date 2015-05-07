__author__ = 'pwidqssg'

import os
from objects.base import CaddiesObject

class Writer:
    def __init__(self, output = None):
        self.out = None
        if not output == None:
            if isinstance(output, basestring):
                self.out = open(output, 'w')
            elif isinstance(output, file):
                self.out = output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        if isinstance(self.out, file):
            self.out.close()

    def writeSQL(self, obj, update = False, f = None):
        out = self.getOutput(f)

        out.write(self.getSQL(obj, update))

    def getSQL(self, obj, update = False):

        table_name = obj.get_table_name()
        sql_1st_str = ''
        sql_2nd_str = ''
        for prop, val in obj.__dict__.iteritems():
            if prop.startswith('_'): continue
            if not val: continue
            if update:
                if not prop == 'id':
                    sql_1st_str += prop + '="' + str(val) + '",'
                else:
                    sql_2nd_str = 'id=' + str(val) + ','
            else:
                sql_1st_str += prop + ','
                sql_2nd_str += '"' + str(val) + '",'

        sql_1st_str = sql_1st_str[:-1]
        sql_2nd_str = sql_2nd_str[:-1]

        if update:
            return 'UPDATE ' + table_name + ' SET ' + sql_1st_str + ' WHERE ' + sql_2nd_str + ';\n'
        else:
            return 'INSERT INTO ' + table_name + ' (' + sql_1st_str + ') VALUES (' + sql_2nd_str + ');\n'

    def getOutput(self, f):
        if f == None:
            out = self.out
        else:
            out = f
        if not isinstance(out, file):
            raise IOError('No output file specified for caddies.Writer write function')
        return out