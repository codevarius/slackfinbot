from subprocess import Popen
import os
import multiprocessing

'''
Script runs endless loop creating bot.py again as subprocess each time it collapses
'''

def setserv():
    os.system('cd js_parts')
    os.system('python -m http.server') 

def startBot():
    #start restart loop for bot
    filename = 'bot.py'
    while True:
        print("\nStarting " + filename)
        p = Popen("python " + filename, shell=True)
        p.wait()

if __name__ == '__main__':
    proc = multiprocessing.Process(name='proc', target=setserv)
    proc2 = multiprocessing.Process(name='proc2', target=startBot)
    proc.start()
    proc2.start()
                                    