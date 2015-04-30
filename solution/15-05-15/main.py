#!/usr/bin/python
# -*- coding:utf-8 -*-

from tkinter import *
from windowvillo import *

root = Tk(className="Villo Manager")
root.resizable(width=False,height=False)
window = WindowVillo(root)
window.mainloop()
