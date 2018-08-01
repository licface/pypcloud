#-*- encoding: utf-8 -*-
#encoding: utf-8
VERSION = "0.1"
import colorama
import termcolor
import inspect
import random
import socket
import cmdw
import os
import sys
import datetime
from make_colors import make_colors
import colorama
import configparser
colorama.init(True)
MAX_WIDTH = cmdw.getWidth()
DEBUG = False
if DEBUG == 1 or DEBUG == '1':
    DEBUG = True
elif DEBUG == 0 or DEBUG == '0':
    DEBUG = False
if os.getenv('DEBUG') == 1 or os.getenv('DEBUG') == '1':
    DEBUG = True
if os.getenv('DEBUG') == 0 or os.getenv('DEBUG') == '0':
    DEBUG = False
if isinstance(DEBUG, str):
    DEBUG = bool(DEBUG.title())
DEBUG_SERVER = os.getenv('DEBUG_SERVER')
if DEBUG_SERVER == 1 or DEBUG_SERVER == '1':
    DEBUG_SERVER = True
if DEBUG_SERVER == 0 or DEBUG_SERVER == '0':
    DEBUG_SERVER = False
if DEBUG_SERVER == "True" or DEBUG_SERVER == True:
    DEBUG_SERVER = True
DEBUGGER_SERVER = ['192.168.100.100:50001']
if os.getenv('DEBUGGER_SERVER'):
    if ";" in os.getenv('DEBUGGER_SERVER'):
        DEBUGGER_SERVER = os.getenv('DEBUGGER_SERVER').strip().split(";")
    else:
        DEBUGGER_SERVER = [os.getenv('DEBUGGER_SERVER')]

FILENAME = ''
if os.getenv('DEBUG_FILENAME'):
    FILENAME = os.getenv('DEBUG_FILENAME')
CONFIG_NAME = os.path.join(os.path.dirname(__file__), 'debug.ini')

import traceback
# if 'win' in sys.platform:
#     def excepthook(type, value, tb):
#         traceback.format_exc(etype = type, value = value, tb = tb)
        
#     sys.excepthook = excepthook


class debugger(object):
    
    global VERSION
    VERSION = "0.1"
    
    def __init__(self, defname = None, debug = None, filename = None, **kwargs):
        super(debugger, self)
        self.DEBUG = debug
        self.FILENAME = filename
        if DEBUG:
            self.DEBUG = DEBUG
        if FILENAME:
            self.FILENAME = FILENAME
        #print "self.FILENAME =", self.FILENAME
        if os.getenv('DEBUG') and os.getenv('DEBUG') == 1 or os.getenv('DEBUG') and os.getenv('DEBUG') == '1' or os.getenv('DEBUG') and os.getenv('DEBUG') == True or os.getenv('DEBUG') and os.getenv('DEBUG') == "True":
            self.DEBUG = True
        #print "self.DEBUG =", self.DEBUG
        #self.printlist(defname, debug, **kwargs)
        
    def version(cls):
        print "version:", VERSION
        
    version = classmethod(version)
        
    def get_config_file(self, filename='', verbosity=None):
        global CONFIG_NAME
        if filename == '':
            if CONFIG_NAME != '':
                filename = CONFIG_NAME
            # else:
            #     return WindowsError('No Config file found !')
    
        if os.path.isfile(os.path.join(os.getcwd(), filename)):
            #print "FILENAME ZZZ=", f
            CONFIG_NAME = os.path.join(os.getcwd(), filename)
            if verbosity:
                print os.path.join(os.getcwd(), filename)
            return os.path.join(os.getcwd(), filename)
        elif os.path.isfile(filename):
            CONFIG_NAME = filename
            if verbosity:
                print os.path.abspath(CONFIG_NAME)
            return filename
        elif os.path.isfile(os.path.join(os.path.dirname(__file__), filename)):
            CONFIG_NAME = os.path.join(os.path.dirname(__file__), filename)
            if verbosity:
                print os.path.join(os.path.dirname(__file__), filename)
            return os.path.join(os.path.dirname(__file__), filename)
        elif os.path.isfile(CONFIG_NAME):
            if verbosity:
                print os.path.abspath(CONFIG_NAME)
            return CONFIG_NAME
        elif os.path.isfile(os.path.join(os.path.dirname(__file__), CONFIG_NAME)):
            if verbosity:
                print os.path.join(os.path.dirname(__file__), CONFIG_NAME)
            return os.path.join(os.path.dirname(__file__), CONFIG_NAME)
        else:
            fcfg = os.path.join(os.path.dirname(__file__), CONFIG_NAME)
            f = open(fcfg, 'w')
            f.close()
            filecfg = fcfg
            if verbosity:
                print "CREATE:", os.path.abspath(filecfg)
            return filecfg
    
        
    def read_config(self, section, option, filename='', verbosity=None): #format result: [aaa.bbb.ccc.ddd, eee.fff.ggg.hhh, qqq.xxx.yyy.zzz]
        """
            option: section, option, filename=''
            format result: [aaa.bbb.ccc.ddd, eee.fff.ggg.hhh, qqq.xxx.yyy.zzz]
            
        """
        filename = get_config_file(filename, verbosity)
        data = []
        cfg = ConfigParser.RawConfigParser(allow_no_value=True, dict_type=MultiOrderedDict) 
        cfg.read(filename)
        cfg = cfg.get(section, option)
        if not cfg == None:
            for i in cfg:
                if "," in i:
                    d1 = str(i).split(",")
                    for j in d1:
                        data.append(str(j).strip())
                else:
                    data.append(i)
            return data
        else:
            return None    
    
    def debug_server_client(self, msg, server_host = '127.0.0.1', port = 50001):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if DEBUGGER_SERVER:
            for i in DEBUGGER_SERVER:
                if ":" in i:
                    host, port = str(i).strip().split(":")
                    port = int(port.strip())
                    host = host.strip()
                else:
                    host = i.strip()
                s.sendto(msg, (host, port))
                s.close()
            
    def setDebug(self, debug):
        self.DEBUG = debug

    def printlist(self, defname = None, debug = None, filename = '', linenumbers = '', **kwargs):
        #print "DEBUG_SERVER =", DEBUG_SERVER
        #print "linenumbers=", linenumbers
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
        if 'win' in sys.platform:
            color_random_1 = [colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX]
        else:
            color_random_1 = [colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA]
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
            #defname = defname + " [" + str(inspect.stack()[0][2]) + "] "
            formatlist = termcolor.colored(datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f'), 'white') + " " + termcolor.colored(defname + arrow, 'white', 'on_red') + formatlist + " " + "[" + str(filename) + "]" + linenumbers
        else:
            defname = str(inspect.stack()[1][3])
            line_number =  " [" + termcolor.colored(str(inspect.stack()[1][2]), 'white', 'on_cyan') + "] "
            if filename == None:
                filename = sys.argv[0]
                #filename = inspect.stack()[2][3]
                #frame = inspect.stack()[1]
                #module = inspect.getmodule(frame[0])
                #filename = module.__file__
                #f = sys._current_frames().values()[0]
                #filename = f.f_back.f_globals['__file__']
            formatlist = termcolor.colored(datetime.datetime.strftime(datetime.datetime.now(), '%Y:%m:%d~%H:%M:%S:%f'), 'white') + " " + termcolor.colored(defname + arrow, 'white', 'on_red') + formatlist + " " + "[" + str(filename) + " [" + termcolor.colored(str(inspect.stack()[1][2]), 'white', 'on_cyan') + "] " + line_number
        if debug:
            print formatlist
        if DEBUG_SERVER:
            self.debug_server_client(formatlist)
        #if debug_server:
            #self.debug_server_client(formatlist)        
        return formatlist
    
def debug_server_client(msg, server_host = '127.0.0.1', port = 50001):
    global CONFIG_NAME
    try:
        if read_config('DEBUGGER', 'HOST', CONFIG_NAME):
            DEBUG_SERVER = read_config('DEBUGGER', 'HOST', CONFIG_NAME)
    except:
        pass
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if DEBUGGER_SERVER:
        for i in DEBUGGER_SERVER:
            if ":" in i:
                host, port = str(i).strip().split(":")
                port = int(port.strip())
                host = host.strip()
            else:
                host = i.strip()
            s.sendto(msg, (host, port))
            s.close()

def serve(host = '0.0.0.0', port = 50001):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print make_colors("BIND: ", 'white', 'green') + make_colors(host, 'white', 'red', attrs= ['bold']) + ":" + make_colors(str(port), 'white', 'yellow', attrs= ['bold'])
    while 1:
        msg = s.recv(65565)
        if msg:
            print msg
            print "=" * (MAX_WIDTH - 3)

def debug(defname = None, debug = None, debug_server = False, line_number = '', **kwargs):
    if DEBUG_SERVER:
        debug_server = True
    if not defname:
        #print "inspect.stack =", inspect.stack()[1][2]
        defname = inspect.stack()[1][3]
        line_number =  " [" + termcolor.colored(str(inspect.stack()[1][2]), 'white', 'on_cyan') + "] "
        #defname = str(inspect.stack()[1][3]) + " [" + str(inspect.stack()[1][2]) + "] "
    c = debugger(defname, debug)
    msg = c.printlist(defname, debug, linenumbers = line_number, **kwargs)
    
    #if DEBUG_SERVER:
        #debug_server_client(msg)
    #if debug_server:
        #debug_server_client(msg)
        
def usage():
    import argparse
    parser = argparse.ArgumentParser(description= 'run debugger as server receive debug text default port is 50001', version= "1.0", formatter_class= argparse.RawTextHelpFormatter)
    parser.add_argument('-b', '--host', action = 'store', help = 'Bind / listen ip address, default all network device: 0.0.0.0', default = '0.0.0.0', type = str)
    parser.add_argument('-p', '--port', action = 'store', help = 'Bind / listen port number, default is 50001', default = 50001, type = int)
    if len(sys.argv) == 1:
        print "\n"
        parser.print_help()
        try:
            args = parser.parse_args()
            serve(args.host, args.port)
        except KeyboardInterrupt:
            sys.exit()
    else:
        try:
            args = parser.parse_args()
            serve(args.host, args.port)
        except KeyboardInterrupt:
            sys.exit()

if __name__ == '__main__':
    pid = os.getpid()
    print "PID:", pid
    usage()
