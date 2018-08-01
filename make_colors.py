import sys

def make_colors(string, foreground = '', background = '', attrs = '', color_type = 'termcolor'):
    """
        attributes termcolor [attrs]:
        ============ ======= ==== ========= ========== ======= =========
        Terminal     bold    dark underline blink      reverse concealed
        ------------ ------- ---- --------- ---------- ------- ---------
        xterm        yes     no   yes       bold       yes     yes
        linux        yes     yes  bold      yes        yes     no
        rxvt         yes     no   yes       bold/black yes     no
        dtterm       yes     yes  yes       reverse    yes     yes
        teraterm     reverse no   yes       rev/red    yes     no
        aixterm      normal  no   yes       no         yes     yes
        PuTTY        color   no   yes       no         yes     no
        Windows      no      no   no        no         yes     no
        Cygwin SSH   yes     no   color     color      color   yes
        Mac Terminal yes     no   yes       yes        yes     yes
        ============ ======= ==== ========= ========== ======= =========
    """
    if foreground == None or foreground == "None":
        return string
    if not background:
        background = ''
    if not foreground:
        foreground = ''
    if not attrs:
        attrs = []                

    def set_colorama(foreground = foreground, background = background):
        try:
            import colorama
            colorama.init(True, wrap= True)
            if sys.platform == 'win32':
                colors_fore = {
                    "white": colorama.Fore.WHITE,
                    "black": colorama.Fore.BLACK,
                    "blue": colorama.Fore.BLUE,
                    "cyan": colorama.Fore.CYAN,
                    "green": colorama.Fore.GREEN,
                    "red": colorama.Fore.RED,
                    "magenta": colorama.Fore.MAGENTA,
                    "yellow": colorama.Fore.YELLOW,
                    "lightwhite": colorama.Fore.LIGHTWHITE_EX,
                    "lightblack": colorama.Fore.LIGHTBLACK_EX,
                    "lightblue": colorama.Fore.LIGHTBLUE_EX,
                    "lightcyan": colorama.Fore.LIGHTCYAN_EX,
                    "lightgreen": colorama.Fore.LIGHTGREEN_EX,
                    "lightred": colorama.Fore.LIGHTRED_EX,
                    "lightmagenta": colorama.Fore.LIGHTMAGENTA_EX,
                    "lightyellow": colorama.Fore.LIGHTYELLOW_EX,                    
                }
                
                colors_back = {
                    'white': colorama.Back.WHITE,
                    'black': colorama.Back.BLACK,
                    'blue': colorama.Back.BLUE,
                    'cyan': colorama.Back.CYAN,
                    'green': colorama.Back.GREEN,
                    'red': colorama.Back.RED,
                    'magenta': colorama.Back.MAGENTA,
                    'yellow': colorama.Back.YELLOW,
                    'lightwhite': colorama.Back.LIGHTWHITE_EX,
                    'lightblack': colorama.Back.LIGHTBLACK_EX,
                    'lightblue': colorama.Back.LIGHTBLUE_EX,
                    'lightcyan': colorama.Back.LIGHTCYAN_EX,
                    'lightgreen': colorama.Back.LIGHTGREEN_EX,
                    'lightred': colorama.Back.LIGHTRED_EX,
                    'lightmagenta': colorama.Back.LIGHTMAGENTA_EX,
                    'lightyellow': colorama.Back.LIGHTYELLOW_EX,                    
                }
            else:
                colors_fore = {
                    "white": colorama.Fore.WHITE,
                    "black": colorama.Fore.BLACK,
                    "blue": colorama.Fore.BLUE,
                    "cyan": colorama.Fore.CYAN,
                    "green": colorama.Fore.GREEN,
                    "red": colorama.Fore.RED,
                    "magenta": colorama.Fore.MAGENTA,
                    "yellow": colorama.Fore.YELLOW,
                    "lightwhite": colorama.Fore.white,
                    "lightblack": colorama.Fore.black,
                    "lightblue": colorama.Fore.blue,
                    "lightcyan": colorama.Fore.cyan,
                    "lightgreen": colorama.Fore.green,
                    "lightred": colorama.Fore.red,
                    "lightmagenta": colorama.Fore.magenta,
                    "lightyellow": colorama.Fore.yellow,                    
                }
                
                colors_back = {
                    'white': colorama.Back.WHITE,
                    'black': colorama.Back.BLACK,
                    'blue': colorama.Back.BLUE,
                    'cyan': colorama.Back.CYAN,
                    'green': colorama.Back.GREEN,
                    'red': colorama.Back.RED,
                    'magenta': colorama.Back.MAGENTA,
                    'yellow': colorama.Back.YELLOW,
                    "lightwhite": colorama.Fore.white,
                    "lightblack": colorama.Fore.black,
                    "lightblue": colorama.Fore.blue,
                    "lightcyan": colorama.Fore.cyan,
                    "lightgreen": colorama.Fore.green,
                    "lightred": colorama.Fore.red,
                    "lightmagenta": colorama.Fore.magenta,
                    "lightyellow": colorama.Fore.yellow,
                }
            
            foreground1 = colors_fore.get(str(foreground))
            background1 = colors_back.get(str(background))
            if not foreground1:
                foreground1 = ''
            if not background1:
                background1 = ''
            if foreground == None or background == "None":
                return string
            colorama.reinit()
            return foreground1 + background1 + string 
        except ImportError:
            print 'NO MODULE NAME: "colorama"'
            return string
        colorama.init()

    def set_termcolor(foreground = foreground, background = background, attrs = attrs):        
        try:
            import termcolor
            try:
                import colorama
                colorama.init(True, wrap= True)
            except ImportError:
                print "NO colorama module !"
            
            #termcolor.RESET = True
            
            colors_fore = {
                    'white': 'white',
                    'grey': 'grey', 
                    'blue': 'blue', 
                    'cyan': 'cyan', 
                    'green': 'green', 
                    'red': 'red', 
                    'magenta': 'magenta', 
                    'yellow': 'yellow',
                    "lightwhite": 'white',
                    "lightblack": 'grey',
                    "lightblue": 'blue',
                    "lightcyan": 'cyan',
                    "lightgreen": 'green',
                    "lightred": 'red',
                    "lightmagenta": 'magenta',
                    "lightyellow": 'yellow',                                        
            }
            
            colors_back = {
                    'white': 'on_white',
                    'grey': 'on_grey', 
                    'blue': 'on_blue', 
                    'cyan': 'on_cyan', 
                    'green': 'on_green', 
                    'red': 'on_red', 
                    'magenta': 'on_magenta', 
                    'yellow': 'on_yellow',
                    "lightwhite": 'on_white',
                    "lightblack": 'on_grey',
                    "lightblue": 'on_blue',
                    "lightcyan": 'on_cyan',
                    "lightgreen": 'on_green',
                    "lightred": 'on_red',
                    "lightmagenta": 'on_magenta',
                    "lightyellow": 'on_yellow',                                        
            }
            if 'light'in foreground or 'light' in background:
                if attrs:
                    if not 'bold' in attrs:
                        attrs.append('bold')
                else:
                    attrs = ['bold']
            if not foreground or foreground == "None" or foreground == "none":
                return string
            if foreground:
                termcolor.RESET
                return termcolor.colored(string, colors_fore.get(str(foreground).strip()), colors_back.get(str(background).strip()), attrs)
            if not foreground:
                return string
        except ImportError:
            print 'NO MODULE NAME: "termcolor'
            return string
        termcolor.RESET
            
    if color_type == 'colorama':
        try:
            a = set_colorama()
            #print "a =", a
            return a
        except:
            b =  set_termcolor()
            #print "b =", b
            return b
    elif color_type == 'termcolor':
        try:
            c =  set_termcolor()
            #print "c =", c
            return c
        except:
            d = set_colorama()
            #print "d =", d
            return d

    