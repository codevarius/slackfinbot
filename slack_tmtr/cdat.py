'''
Script produces date formated with dots 
'''

from datetime import datetime as dtime

def getFormatedDate():
    date = dtime.now()
    day = str(date.day).zfill(2) if str(date.day).__len__() == 1 else str(date.day)
    month = str(date.month).zfill(2) if str(date.month).__len__() == 1 else str(date.month) 
    d = ''.join([day,'.',month,'.',str(date.year)])
    return d
    