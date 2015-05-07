__author__ = 'pwidqssg'

import argparse
import os
from usreader import USReader
from caddies.writer import Writer

class us2c:
    def __init__(self):
        self.filepaths = []
        self.files = []

    """ Specialist function for validating the given filename for the input
    file from the command line. If the file exists and is readable, the
    file object is returned."""
    def is_valid_file(parser, arg):
        if not os.path.exists(arg):
            parser.error('The file %s does not exist!'%arg)
        else:
            return open(arg,'r')    #return an open file handle

    def setup_terminal_args(self, parser = argparse.ArgumentParser()):
        parser.add_argument('-i',
                            dest='infilename',
                            required=False,
                            help='Input file to be converted',
                            metavar='FILE',
                            type=lambda x: self.is_valid_file(parser, x)
                            )
        args = parser.parse_args()
        if not args.infilename == None:
            self.filepaths.append(args.infilename)

    def add_file_path(self, filepath):
        if not isinstance(filepath, basestring):
            raise TypeError('add_file_path requires aa string')
        elif not os.path.exists(filepath):
            raise IOError('Not a valid file path')
        else:
            self.filepaths.append(filepath)

    def add_file_paths(self, filepaths):
        if not isinstance(filepaths, list):
            raise TypeError('add_file_paths requires an array of file paths')
        else:
            self.filepaths = self.filepaths + filepaths

    def load(self):
        for filepath in self.filepaths:
            with USReader(filepath) as reader:
                reader.readInstance()
                with Writer('test.sql') as wrtr:
                    wrtr.writeSQL(reader.instance, update=True)