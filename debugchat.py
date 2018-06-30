# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 09:33:43 2018

@author: Admin
"""

from chat_proc import *

activechat=True
print("KETIK 'q' untuk EXIT.")
while activechat:
    myinput=input(">")
    sequence(myinput,humanstate,botstate)
    if myinput=="q":
        activechat=False
