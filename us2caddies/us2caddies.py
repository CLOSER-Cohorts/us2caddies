__author__ = 'pwidqssg'

import argparse
import os
from usreader import USReader
from caddies.writer import Writer

class us2c:
    def __init__(self):
        self.filepaths = []
        self.files = []
        self.QREs = []
        self.outfiles =[]

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
                            type=argparse.FileType('r')
                            )
        parser.add_argument('--results',
                            dest='results',
                            action='store_true',
                            help='Display the results of the conversion after completion'
                            )
        args = parser.parse_args()
        if not args.infilename == None:
            self.filepaths.append(args.infilename.name)
        if args.results:
            self.results = True
        else:
            self.results = False

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
            self.QREs.append({'in':filepath})
            self.QREs[-1]['out'] = os.path.abspath(filepath).rsplit('.')[0] + '.sql'
            with USReader(filepath) as reader:
                reader.readInstance()
                self.QREs[-1]['instance'] = reader.instance
                self.QREs[-1]['build'] = reader.readQRE()

    def write(self):
        for QRE in self.QREs:
            with Writer(QRE['out']) as wrtr:
                wrtr.writeSQL(QRE['instance'], update=True)
                wrtr.write(QRE['build'])

            if self.results:
                print '=== ' + QRE['instance'].instrument + ' ==='
                QRE['build'].printStats()
