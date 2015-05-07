__author__ = 'pwidqssg'

import us2caddies as us2c
import argparse
import os

app = us2c.us2c()

app.setup_terminal_args()
app.add_file_path(os.path.dirname(__file__) + '/in.xml')
app.load()


