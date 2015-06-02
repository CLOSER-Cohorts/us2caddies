__author__ = 'pwidqssg'

import us2caddies as us2c
#from Tkinter import *
import os

"""
class Application(Frame):
    def __init__(self, master=None):
        master.wm_title("Convert to Caddies")
        Frame.__init__(self, master, width=400, height=200)
        self.pack()

root = Tk()
window = Application(master=root)
window.mainloop()
root.destroy()

"""
app = us2c.us2c()

app.setup_terminal_args()
app.add_file_path(os.path.dirname(__file__) + '/in_full.xml')
app.load()
app.write()

