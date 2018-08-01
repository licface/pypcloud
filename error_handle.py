#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LICFACE --<licface@yahoo.com>
  Purpose: pyPCloud error handle project
  Created: 4/10/2018
"""

import os
import sys
import datetime
from make_colors import make_colors
import colorama
colorama.init(True)
import cmdw
MAX_WIDTH = cmdw.getWidth()
import random
import inspect

class error(object):
    def __init__(self):
        super(self, error)
        if FILENAME:
            self.FILENAME = FILENAME        
        
    def print_error(self, defname = None, debug = None, filename = '', **kwargs):
        #print "DEBUG_SERVER =", DEBUG_SERVER
        if DEBUG_SERVER:
            debug_server = True
            
        #if filename:
            #filename = "[" + filename + "]"        
        if not filename:
            filename = self.FILENAME
        #if filename:
            #filename = "[" + self.FILENAME + "]"
        
        if not debug:
            debug = self.DEBUG
        color_random_1 = [colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX]
        colorama.init()
        formatlist = ''
        arrow = colorama.Fore.YELLOW + ' -> '
        if not kwargs == {}:
            for i in kwargs:
                try:
                #formatlist += color_random_1[kwargs.keys().index(i)] + i + ": " + color_random_1[kwargs.keys().index(i)] + str(kwargs.get(i)) + arrow
                    formatlist += termcolor.colored((unicode(i) + ": "), 'white', 'on_blue') + color_random_1[kwargs.keys().index(i)] + str(kwargs.get(unicode(i))) + arrow
                except:
                    print "DEBUG ERROR !"
        else:
            formatlist += random.choice(color_random_1) + " start... " + arrow
        formatlist = formatlist[:-4]
        
        if defname:
            if filename == None:
                #frame = inspect.stack()[1]
                #module = inspect.getmodule(frame[0])
                #filename = module.__file__
                #filename = inspect.stack()[2][3]
                filename = sys.argv[0]
            formatlist = termcolor.colored(datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f'), 'white') + " " + termcolor.colored(defname + arrow, 'white', 'on_red') + formatlist + " " + "[" + str(filename) + "]"        
        else:
            defname = inspect.stack()[1][3]
            if filename == None:
                filename = sys.argv[0]
                #filename = inspect.stack()[2][3]
                #frame = inspect.stack()[1]
                #module = inspect.getmodule(frame[0])
                #filename = module.__file__
                #f = sys._current_frames().values()[0]
                #filename = f.f_back.f_globals['__file__']
            formatlist = termcolor.colored(datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f'), 'white') + " " + termcolor.colored(defname + arrow, 'white', 'on_red') + formatlist + " " + "[" + str(filename) + "]"        
        if debug:
            print formatlist
        if DEBUG_SERVER:
            self.debug_server_client(formatlist)
        #if debug_server:
            #self.debug_server_client(formatlist)        
        return formatlist
    
    def error_report(cls, defname = None, debug = None, filename = '', **kwargs):
        return cls.print_error(defname, debug, filename, **kwargs)
    error = classmethod(error_report)
    
if __name__ == '__main__':
    def test():
        error.error(data = 'BLACKID', debug= True)
    test()
    