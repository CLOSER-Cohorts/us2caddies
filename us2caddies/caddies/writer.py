__author__ = 'pwidqssg'

import datetime
from objects.base import CaddiesObject
from builder import Builder

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

    def write(self, obj, update = False, f = None):
        if isinstance(obj, Builder):
            for prop, val in obj.__dict__.iteritems():
                if prop.startswith('_'): continue
                for item in val:
                    self.writeSQL(item, update, f)
        elif isinstance(obj, CaddiesObject):
            self.writeSQL(obj, update, f)
        else:
            Exception('Cannot write this type of object')

    def writeSQL(self, obj, update = False, f = None):
        out = self.getOutput(f)

        out.write(self.getSQL(obj, update))

    def getSQL(self, obj, update = False):

        table_name = obj.get_table_name()
        sql_1st_str = ''
        sql_2nd_str = ''
        for prop, val in obj.__dict__.iteritems():
            if prop.startswith('_'): continue
            if val == None or val == "": continue
            if update:
                if not prop == 'id':
                    try:
                        num = float(val)
                        num = int(num) if num.is_integer() else num
                        sql_1st_str += prop + '=' + unicode(num) + ','
                    except ValueError:
                        sql_1st_str += prop + '="' + self.scrubString(val) + '",'
                else:
                    sql_2nd_str = 'id=' + unicode(val) + ','
            else:
                sql_1st_str += prop + ','
                try:
                    num = float(val)
                    num = int(num) if num.is_integer() else num
                    sql_2nd_str += '' + unicode(num) + ','
                except ValueError:
                    sql_2nd_str += '"' + self.scrubString(val) + '",'

        if update:
            sql_1st_str += 'updated_at="' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '",'
        else:
            sql_1st_str += 'created_at,updated_at,'
            sql_2nd_str += '"' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + \
                           '","' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '",'

        sql_1st_str = sql_1st_str[:-1]
        sql_2nd_str = sql_2nd_str[:-1]

        if update:
            return unicode('UPDATE ' + table_name + ' SET ' + sql_1st_str + ' WHERE ' + sql_2nd_str + ';\n').encode('ascii', 'xmlcharrefreplace')
        else:
            return unicode('INSERT INTO ' + table_name + ' (' + sql_1st_str + ') VALUES (' + sql_2nd_str + ');\n').encode('ascii', 'xmlcharrefreplace')

    def getOutput(self, f):
        if f == None:
            out = self.out
        else:
            out = f
        if not isinstance(out, file):
            raise IOError('No output file specified for caddies.Writer write function')
        return out

    def scrubString(self, input):
        output = input.replace('\n',' ').replace('\r',' ')
        return unicode(' '.join(output.split()))