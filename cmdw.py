import os
import sys
# stdin handle is -10
# stdout handle is -11
# stderr handle is -12

def getSize():
    if os.name == 'nt':
    	from ctypes import windll, create_string_buffer
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

        if res:
            import struct
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
        else:
            sizex, sizey = 80, 25 # can't determine actual size - return default values
        return sizex, sizey
        # print sizex, sizey
    elif os.name == 'posix':
        from fcntl import ioctl
        from termios import TIOCGWINSZ
        from array import array
    
        winsize = array("H", [0] * 4)
        try:
            ioctl(sys.stdout.fileno(), TIOCGWINSZ, winsize)
        except IOError:
            pass
        # return (winsize[1], winsize[0])[0]
        return (winsize[1], winsize[0])
    return 80

def getWidth():
    return getSize()[0]

def getHeight():
    return getSize()[1]

if __name__ == '__main__':
    print getSize()
    sizex = getWidth()
    print "_"*int(sizex)
