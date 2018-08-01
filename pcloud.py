#!/usr/bin/python

from progressbar import Bar, ETA, Percentage, ProgressBar, AdaptiveETA, AdaptiveTransferSpeed
import requests
from bs4 import BeautifulSoup as bs
import global_config
import vping
import os
import sys
import time
import json
#import debug as debugger
from debug import * 
#debugger.DEBUG = os.getenv('DEBUG')
if 'win' in sys.platform:
    import msvcrt
    import idm
else:
    from getch import getch as msvcrt
#from treelib import Node, Tree
#import treelib
import configset
import datetime
import colorama
import termcolor
import wget
import cPickle
import random
import getpass
import inspect
import math
import clipboard
import urlparse
from make_colors import make_colors
import traceback
#import tracert

# print "PID                :", os.getpid()
if __name__ == '__main__':
    print "PID =", os.getpid()


class pcloud(object):

    def __init__(self, **kwargs):
        super(pcloud, self)
        
        #self.debug = False
        #if self.debug:
            #debugger.DEBUG = self.debug
        self.MASTER_URL = "https://api.pcloud.com/{0}&authexpire={1}&{2}"
        self.nlist = None
        if not self.MASTER_URL:
            self.MASTER_URL = self.getConfig('GLOBAL', 'MASTER_URL')
        debug(MASTER_URL=self.MASTER_URL)
        self.headers = {}
        self.cookies = {}
        self.params = {}
        self.proxy = kwargs.get('proxy')
        if not self.proxy:
            self.proxy = {}
        self.username = kwargs.get('username')
        if not self.username:
            self.username = self.getConfig('AUTH', 'username')
        debug(username=self.username)
        self.password = kwargs.get('password')
        if not self.password:
            self.password = self.getConfig('AUTH', 'password')
        debug(password=self.password)
        self.parent = kwargs.get('parent')
        if not self.parent:
            self.parent = self.getConfig('GLOBAL', 'parent')
        if not self.parent:
            self.parent = 'root'
        debug(parent=self.parent)
        self.islogin = False
        debug(islogin=self.islogin)
        self.auth = kwargs.get('auth')
        self.nopartial = kwargs.get('nopartial')
        self.authexpire = kwargs.get('authexpire')
        if not self.authexpire:
            self.authexpire = global_config.expire
        if not self.authexpire:
            self.getConfig('AUTH', 'expire')
        self.access_token = kwargs.get('access_token')
        self.authinactiveexpire = kwargs.get('authinactiveexpire')
        self.folderid = 0
        self.timeformat = ''
        self.filtermeta = ''
        self.filterfoldermeta = ''
        self.logout = kwargs.get('logout')
        self.progresshash = kwargs.get('progresshash')
        debug(logout1=self.logout)
        if not self.logout:
            self.logout = 1
        debug(logout2=self.logout)

    def getDebug(self):
        return self.debug

    def convert_size(self, size_bytes):
        if (size_bytes == 0):
            return '0B'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return '%s %s' % (s, size_name[i])

    def h_convert_size(self, sizes):
        from hurry.filesize import size, si
        return "{0} ~ {1}".format(size(sizes), size(sizes, system=si))

    def print_nav(self, auth, username=None, password=None):
        userdata = self.userInfo(auth, username, password, False)
        #debug(userdata = userdata, debug = True)
        user_email = userdata.get('email') + ", "
        used_quota = self.convert_size(userdata.get('usedquota'))
        #debug(used_quota = used_quota, debug= True)
        if len(used_quota) > 2:
            used_quota1 = float(used_quota[:-3])
        else:
            used_quota1 = int(used_quota[:-1])
        if float(used_quota1) > 5 and float(used_quota1) < 7:
            used_quota = termcolor.colored(str(used_quota), 'white', 'on_green', attrs= ['bold'])        
        if float(used_quota1) > 7 and float(used_quota1) < 9:
            used_quota = termcolor.colored(str(used_quota), 'red', 'on_yellow', attrs= ['bold', 'blink'])        
        if float((used_quota1)) > 9 and float(used_quota1) < 11:
            used_quota = termcolor.colored(str(used_quota), 'white', 'on_red', attrs= ['bold', 'blink'])
        quota = self.convert_size(userdata.get('quota')) + ", "
        colorama.init()
        try:
            print termcolor.colored("USERNAME: " + user_email + "USED QUOTA: " + used_quota  + ", "+ "QUOTA: " + quota, 'yellow', 'on_blue') + " [%s]" % os.getpid()
            print termcolor.colored("d = download, e = explore (b = back), r = rename, v = list recursive, f = create Folder, u = upload (file/url), m = remove, g = move, w = refresh (reload), z = register, t = login, q = exit, c = clear screen, C = copy download link only, or select number for direct download and for folder is go to folder", 'white', 'on_cyan', attrs= ['bold'])
            return ": "
        except:
            try:
                print make_colors("USERNAME: " + user_email + "USED QUOTA: " + used_quota  + ", "+ "QUOTA: " + quota + " [%s]" % os.getpid(), 'lightyellow', 'lightblack', color_type= 'colorama')
                print make_colors("d = download, e = explore (b = back), r = rename, v = list recursive, f = create Folder, u = upload (file/url), m = remove, g = move, w = refresh (reload), z = register, t = login, q = exit, c = clear screen, C = copy download link only, or select number for direct download and for folder is go to folder", 'white', 'cyan', attrs= ['bold'])
                return ": "
            except:
                print "USERNAME: " + user_email + "USED QUOTA: " + used_quota  + ", "+ "QUOTA: " + quota + " [%s]" % os.getpid()
                print "d = download, e = explore (b = back), r = rename, v = list recursive, f = create Folder, u = upload (file/url), m = remove, g = move, w = refresh (reload), z = register, t = login, q = exit, c = clear screen, C = copy download link only, or select number for direct download and for folder is go to folder"
                return ": "

    def printlist(self, defname=None, debug=None, **kwargs):
        if not debug:
            debug = self.getDebug()
        if sys.platform == 'win32':
            color_random_1 = [colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.LIGHTWHITE_EX, colorama.Fore.LIGHTCYAN_EX, colorama.Fore.LIGHTMAGENTA_EX]
        else:
            color_random_1 = [colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.WHITE, colorama.Fore.CYAN, colorama.Fore.MAGENTA]
        colorama.init()
        formatlist = ''
        arrow = colorama.Fore.YELLOW + ' -> '
        if not kwargs == {}:
            for i in kwargs:
                #formatlist += color_random_1[kwargs.keys().index(i)] + i + ": " + color_random_1[kwargs.keys().index(i)] + str(kwargs.get(i)) + arrow
                formatlist += termcolor.colored((i + ": "), 'white', 'on_blue') + color_random_1[
                    kwargs.keys().index(i)] + str(kwargs.get(i)) + arrow
        else:
            formatlist += random.choice(color_random_1) + " start... " + arrow
        formatlist = formatlist[:-4]

        if defname:
            formatlist = termcolor.colored(
                defname + arrow, 'white', 'on_red') + formatlist
        else:
            defname = inspect.stack()[1][3]
            formatlist = termcolor.colored(
                defname + arrow, 'white', 'on_red') + formatlist
        if debug:
            print formatlist
        return formatlist

    def makeList(self, alist, ncols, vertically=True, file=None):
        from distutils.version import StrictVersion  # pep 386
        import prettytable as ptt  # pip install prettytable
        import sys
        assert StrictVersion(ptt.__version__) >= StrictVersion(
            '0.7')  # for PrettyTable.vrules property
        L = alist
        nrows = - ((-len(L)) // ncols)
        ncols = - ((-len(L)) // nrows)
        t = ptt.PrettyTable([str(x) for x in range(ncols)])
        t.header = False
        t.align = 'l'
        t.hrules = ptt.NONE
        t.vrules = ptt.NONE
        r = nrows if vertically else ncols
        chunks = [L[i:i + r] for i in range(0, len(L), r)]
        chunks[-1].extend('' for i in range(r - len(chunks[-1])))
        if vertically:
            chunks = zip(*chunks)
        for c in chunks:
            t.add_row(c)
        print termcolor.colored(t, 'green')

    def printList(self, option, value, defname='', size=50):
        if defname:
            defname = defname + " -> "
        if option== 'size':
            value = self.sizeof(int(value))
        print defname + str(option) + ' ' * (size - len(str(option))) + ' = ' + str(value)

    def setHeaders(self, referer='https://www.pcloud.com', accept='application/json, text/javascript, */*; q=0.01', accept_encoding='gzip, deflate',  accept_language='en-US,en;q=0.5', content_length='', content_type='', cookie='', host='', origin='', user_agent='Mozilla/5.0 (Windows NT 10.0; rv:38.9) Gecko/20100101 Goanna/2.2 Firefox/38.9 PaleMoon/26.5.0', x_requested_with='', **kwargs):
        if origin == '':
            origin = referer
        header = {
            'Accept': accept,
            'Accept-Encoding':	accept_encoding,
            'Accept-Language': accept_language,
            'Host':	host,
            'Origin': origin,
            'Referer': referer,
            'User-Agent': user_agent,
        }
        if host:
            header.update({'Host': host, })
        if content_length:
            header.update({'Content-Length': content_length, })
        if content_type:
            header.update({'Content-Type': content_type, })
        if cookie:
            header.update({'Cookie': cookie, })
        # if origin:
            #header.update({'Origin': origin,})
        if x_requested_with:
            header.update({'x-requested-with': x_requested_with, })
        if kwargs:
            header.update(kwargs)
        self.headers = header
        return header

    def setParams(self, username=None, password=None, params=None, **kwargs):
        if username == None:
            username, password = self.setUserPass()
        if not params and not isinstance(param, dict):
            params = {}
        params.update(kwargs)
        if username and password:
            auth = self.getAuth(username, password)
            self.setAuth(auth)
        params.update({
            'username': username,
            'password': password,
            'authexpire': self.authexpire,
            'auth': '',
            #'getauth': 1,
        })
        return params

    def Request(self, url, rtype='get', headers=None, params=None, cookies=None, data=None, **cookies_update):
        if cookies != None:
            if cookies_update != {}:
                cookies.update(cookies_update)

        if rtype == 'get':
            a = requests.get(url, params=params,
                             headers=headers, cookies=cookies)
        elif rtype == 'post':
            a = requests.post(url, params=params, headers=headers,
                              cookies=cookies, data=data)

        def request():
            if rtype == 'get':
                a = requests.get(url, params=params,
                                 headers=headers, cookies=cookies)
            elif rtype == 'post':
                a = requests.post(url, params=params, headers=headers,
                                  cookies=cookies, data=data)
            return a
        request()
        if not a.ok:
            self.login()
            a = request()
        return a

    def getCurrentServer(self, headers=None):
        url_param = 'currentserver'
        #url_add = '&auth=' + self.getAuth()
        # if headers == None:
        #headers = self.setHeaders(referer='https://my.pcloud.com/',origin='https://my.pcloud.com', user_agent='Mozilla/5.0 (Windows NT 10.0; rv:38.9) Gecko/20100101 Goanna/2.2 Firefox/38.9 PaleMoon/26.5.0')
        #URL = self.MASTER_URL.format(url_param, self.authexpire, url_add)
        #URL = self.MASTER_URL.format(url_param, self.authexpire)
        # print "getCurrentServer -> URL =", URL
        #a = self.Request(URL, headers = headers)
        a = json.loads(self.getURL1('https://api.pcloud.com/' + url_param)[0])
        debug('getCurrentServer', a=str(a))
        return a

    def getCookies(self, url, params='', headers='', username=None, password=None):
        if username:
            params = self.setParams(username, password)
        if headers == '':
            headers = self.setHeaders(url)
        a = requests.get(url, params=params, headers=headers)
        b = a.cookies
        return b.get_dict()

    def setCookies(self, url="https://api.pcloud.com", username=None, password=None, **kwargs):
        '''
            url is previous url        
        '''
        cookies = {}
        debug(kwargs = kwargs)
        if username and password:
            auth = self.getAuth(username, password)
            self.setAuth(auth)
        else:
            auth = self.getAuth()
        cookies.update(kwargs)
        getcookies = self.getCookies(url, username=username, password=password)
        if getcookies:
            cookies.update(getcookies)
        cookies.update({'pcauth': auth, })
        return str(cookies)

    def setUserPass(self):
        import getpass
        if self.getConfig('AUTH', 'username'):
            username = self.getConfig('AUTH', 'username')
            if self.getConfig('AUTH', 'password'):
                password = self.getConfig('AUTH', 'password')
        if hasattr(config, 'USERNAME'):
            username = global_config.USERNAME
            self.username = username
            if hasattr(config, 'PASSWORD'):
                password = global_config.PASSWORD
                self.password = password
            else:
                password = getpass.getpass("Password: ")
                self.password = password
        else:
            if self.username == None:
                username = raw_input("Username: ")
                self.username = username
            if self.password == None:
                password = getpass.getpass("Password: ")
                self.password = password
        return username, password

    def getURL(self, url):
        '''
            check connection before with vping
        '''
        import urlparse
        # dest_addr = urlparse.urlparse(
        #     url).scheme + "://" + urlparse.urlparse(url).netloc
        dest_addr = urlparse.urlparse(url).netloc
        r_text = ''
        print "dest_addr =", dest_addr
        print "vping.vping(dest_addr) =", vping.vping(dest_addr)
        while True:
            if vping.vping(dest_addr):
                req = requests.get(url)
                r_text = req.text
                break
            else:
                print "False"
                time.sleep(1)
        return r_text

    def getURL1(self, url, params=None, rtype='get', data = None, proxy = None, stream = False):
        '''
            check after with while statement for OK
        '''
        if not proxy:
            proxy = {}
        if not params:
            params = {}
        if not proxy:
            proxy = {}
        if not proxy:
            proxy = self.proxy
        if not data:
            data = {}
        r_text = ''
        def get_url():
            if rtype == 'get':
                req = requests.get(url, params=params, proxies = proxy, stream = stream)
                debug(rtype = 'get', URL= str(req.url))
                cookies = req.cookies
                r_text = req.text
                return req, r_text, cookies
            elif rtype == 'post':
                req = requests.post(url, params=params, data = data, proxies = proxy, stream = stream)
                debug(rtype = 'post', URL= str(req.url))
                cookies = req.cookies
                r_text = req.text
                return req, r_text, cookies
        req, r_text, cookies = get_url()
        while True:
            if req.ok:
                #r_text = req.text
                break
            else:
                req, r_text, cookies = get_url()

        return r_text, cookies

    def getURL3(self, url, fullfilename, params=None, headers=None, proxy = None, stream = False):
        '''
            for files uploading
        '''
        if not headers:
            headers = {}
        if not params:
            params = {}
        if not proxy:
            proxy = {}
        if not proxy:
            proxy = self.proxy        
        files = {"form_input_field_name": open(fullfilename, "rb")}
        req = requests.post(url, params=params, headers=headers, files=files, proxies = proxy, stream = stream)
        r_text = ''
        while True:
            if req.ok:
                r_text = req.text
                break
        return r_text

    def getURL2(self, url, params=None, rtype='get', data=None, headers=None, proxy = None):
        '''
            direct return, no check it
        '''
        if not data:
            data = {}
        if not proxy:
            proxy = {}
        if not proxy:
            proxy = self.proxy        
        if rtype == 'get':
            req = requests.get(url, params=params, headers=headers, proxies = proxy)
        elif rtype == 'post':
            req = requests.post(url, params=params, data=data, headers=headers, proxies = proxy)
        r_text = req.text
        #debug('getURL2', req_text = req.text)
        return r_text

    def setURL(self, url='', addurl=''):
        authexpire = self.AuthExpire()
        if hasattr(global_config, 'MASTER_URL'):
            if hasattr(global_config, 'expire'):
                debug(code=2)
                debug(
                    global_config_MASTER_URL=global_config.MASTER_URL)
                # print "setURL -> global_config.MASTER_URL =", global_config.MASTER_URL
                # print "global_config.MASTER_URL.format(url, global_config.expire,
                # addurl) =", global_config.MASTER_URL.format(url,
                # global_config.expire, addurl)
                debug(global_config_expire=global_config.MASTER_URL.format(
                    url, global_config.expire, addurl))
                return global_config.MASTER_URL.format(url, global_config.expire, addurl)
            else:
                debug(code=2)
                return global_config.MASTER_URL.format(url, authexpire, addurl)
        elif self.MASTER_URL != "" or self.MASTER_URL != None:
            try:
                assert(self.MASTER_URL !=
                       None), "Please set global_config.py: MASTER_URL or self.MASTER_URL"
                debug(step=3)
                return self.MASTER_URL.format(url, authexpire, addurl)
            except AssertionError, e:
                e.args += ('DEF: setURL',
                           'LINE: 10, global_config.py [LINE: 3]', '15')
                raise
        else:
            debug(code=4)
            return False

    def login(self, username='', password='', print_list=True):
        data = {}
        if not username:
            username = self.username
        if not password:
            password = self.password
        if username == 'q' or password == 'q':
            sys.exit(0)
        debug(username=username)
        debug(password=password)
        if not username:
            if hasattr(global_config, 'USERNAME'):
                if global_config.USERNAME:
                    username = global_config.USERNAME
            if self.getConfig('AUTH', 'username'):
                username = self.getConfig('AUTH', 'username')
                #username = raw_input("USERNAME: ")
            if not username:
                username = raw_input("USERNAME: ")
        if password == '' or password == None:
            import getpass
            if hasattr(global_config, 'PASSWORD'):
                if global_config.PASSWORD:
                    password = global_config.PASSWORD
            if self.getConfig('AUTH', 'password'):
                password = self.getConfig('AUTH', 'username')
            if not password:
                password = getpass.getpass('PASSWORD: ')

        URL = self.setURL(
            'userinfo?getauth=1&username={0}&password={1}&logout={2}'.format(username, password, self.logout))
        #if not URL:
            #print termcolor.colored("REGISTERED", 'white', 'on_red')
        #debug(URL=URL, debug= True)
        data = json.loads(self.getURL1(URL)[0])
        #debug(data=data, debug= True)
        if data.get('auth'):
            self.auth = data.get('auth')
            configset.write_config('AUTH', 'auth', value=data.get('auth'))
            #debug(data_get_auth = data.get('auth'), debug = True)
            self.islogin = True
            self.userInfo(data.get('auth'), print_list=print_list)
            return data
        else:
            print termcolor.colored("INVALID USERNAME or PASSWORD !", 'white', 'on_red', attrs= ['blink']) + termcolor.colored(", PLEASE LOGIN AGAIN", 'white', 'on_cyan', attrs= ['bold'])
            return self.login(username, password, print_list = print_list)

    def getConfig(self, section, option):
        try:
            a = configset.read_config(section, option)
            return a
        except:
            configset.write_config(section, option)
            a = configset.read_config(section, option)
            debug(a = a, debug = True)
            return a
        if not a:
            if hasattr(global_config, option):
                a = getattr(global_config, option)
                return a
        return False

    # def getAuth(self, username='', password=''):
        #auth = self.login(username, password).get('auth')
        # return auth
    def getExpires(self, timestamp=1549875285, format_date='%d:%m:%Y %I:%M:%S', ftype=0):
        if ftype == 0:
            format_date = '%d:%m:%Y %I:%M:%S'
        elif ftype == 1:
            format_date = '%A, %B %d, %Y %I:%M:%S %p'
        now = datetime.datetime.now()
        tnow = time.mktime(now.timetuple())
        expired = False
        texpire = datetime.datetime.fromtimestamp(tnow).strftime(format_date)
        if format_date:
            x = datetime.datetime.fromtimestamp(
                timestamp).strftime(format_date)
            if texpire == x:
                expired = True
            if tnow > timestamp:
                expired = True
            if expired:
                print "Cookies is EXPIRED !, Please Login or Try Agains !"
                print "X =", x
                sys.exit(0)
            return x, expired
        else:
            x = datetime.datetime.fromtimestamp(
                timestamp).strftime('%d:%m:%Y %I:%M:%S')
            if texpire == x:
                expired = True
            if tnow > timestamp:
                expired = True
            if expired:
                print "Cookies is EXPIRED !, Please Login or Try Agains !"
                sys.ext(0)
            return x, expired

    def AUTH(self, auth=None, username=None, password=None, url=None):
        if auth:
            debug(if_auth='', auth=auth)
            if url:
                URL = self.setURL('{0}?auth={1}'.format(url, auth))
            else:
                URL = ''
        if self.auth:
            auth = self.auth
            debug(if_self_auth='', auth=self.auth)
            if url:
                URL = self.setURL('{0}?auth={1}'.format(url, auth))
            else:
                URL = ''
        if self.getAuth(auth, username, password):
            #debug(username = username, debug = True)
            auth = self.getAuth(auth, username, password)
            debug(if_getAuth='', auth=self.getAuth(
                auth, username, password))
            if url:
                URL = self.setURL('{0}?auth={1}'.format(url, auth))
            else:
                URL = ''
        if username and password:
            auth = self.login(username, password).get('auth')
            debug(if_username_password='')
            if url:
                URL = self.setURL(
                    '{0}?username={1}&password{2}'.format(url, username, password))
            else:
                URL = ''
        return auth, URL

    def setAuth(self, auth=None):
        if auth:
            configset.write_config('AUTH', 'auth', value=auth)
            self.auth = auth
            debug(self_auth = self.auth, debug = True)

    def AuthExpire(self, expire='63072000'):
        try:
            e = configset.read_config('AUTH', 'expire')
        except:
            configset.write_config('AUTH', 'expire', value='63072000')
            e = configset.read_config('AUTH', 'expire')
        self.authexpire = e
        return e

    def getAuth(self, auth=None, username=None, password=None):
        if not username:
            username = self.username
        if not password:
            password = self.password
        if auth:
            debug(auth_1=auth)
            return auth
        else:
            #debug(username = username, debug = True)
            auth = self.getConfig('AUTH', 'auth')
            if not auth:
                auth = self.login(username, password).get('auth')
            debug(auth_2=auth)
            return auth

    def listToken(self, auth=None, username=None, password=None):
        if auth == None:
            auth = self.getAuth(auth, username, password)
        URL = self.setURL('listtokens?auth={0}'.format(auth))
        data, cookies = json.loads(self.getURL1(URL))
        return data

    def userInfo(self, auth=None, username=None, password=None, print_list=True):
        #debug(username = username, debug= True)
        def filter_quota(used_quota):
            if len(used_quota) > 2:
                used_quota1 = float(used_quota[:-3])
            else:
                used_quota1 = int(used_quota[:-1])
            if float(used_quota1) > 5 and float(used_quota1) < 7:
                used_quota = termcolor.colored(str(used_quota), 'white', 'on_green', attrs= ['bold'])        
            if float(used_quota1) > 7 and float(used_quota1) < 9:
                used_quota = termcolor.colored(str(used_quota), 'red', 'on_yellow', attrs= ['bold', 'blink'])        
            if float((used_quota1)) > 9 and float(used_quota1) < 11:
                used_quota = termcolor.colored(str(used_quota), 'white', 'on_red', attrs= ['bold', 'blink'])
            debug(used_quota = used_quota)
            return used_quota
        if auth:
            URL = self.setURL('{0}?auth={1}'.format('userinfo', auth))
        else:
            auth, URL = self.AUTH(auth, username, password, 'userinfo')
        data, cookies = self.getURL1(URL)
        data = json.loads(data)
        if print_list:
            each_len_keys = []
            for i in data:
                each_len_keys.append(len(i))
            for i in data:
                if i == 'usedquota':
                    print "Used Quota" + " " * (max(each_len_keys) - len(i)) + ": " + "{0} | {1}".format(filter_quota(self.convert_size(data.get(i))), self.h_convert_size(data.get(i)))
                elif i == 'quota':
                    print "Quota" + " " * (max(each_len_keys) - len(i)) + " : " + "{0} | {1}".format(self.convert_size(data.get(i)), self.h_convert_size(data.get(i)))
                elif i == 'email':
                    print "Email" + " " * (max(each_len_keys) - len(i)) + " : " + make_colors(data.get(i), 'white', 'red', attrs= ['bold'])
                elif i == 'publiclinkquota':
                    print "Public Link Quota" + " " * ((max(each_len_keys) - len(i)) - 1) + ": " + "{0} | {1}".format(self.convert_size(data.get(i)), self.h_convert_size(data.get(i)))
                else:
                    print str(i).title() + " " * (max(each_len_keys) - len(i)) + " : " + str((data.get(i)))
        return data
    
    def userInfo1(self, username=None, password=None, print_list=True):
        #auth, URL = self.AUTH(auth, username, password, 'userinfo')
        authexpire = self.AuthExpire()
        url = '{0}?username={1}&password{2}'
        URL = global_config.MASTER_URL.format(url, authexpire, '')
        debug(URL = URL, debug = True)
        data, cookies = self.getURL1(URL)
        data = json.loads(data)
        if print_list:
            each_len_keys = []
            for i in data:
                each_len_keys.append(len(i))
            for i in data:
                if i == 'usedquota':
                    print "Used Quota" + " " * (max(each_len_keys) - len(i)) + ": " + "{0} | {1}".format(self.convert_size(data.get(i)), self.h_convert_size(data.get(i)))
                elif i == 'quota':
                    print "Quota" + " " * (max(each_len_keys) - len(i)) + " : " + "{0} | {1}".format(self.convert_size(data.get(i)), self.h_convert_size(data.get(i)))
                elif i == 'publiclinkquota':
                    print "Public Link Quota" + " " * ((max(each_len_keys) - len(i)) - 1) + ": " + "{0} | {1}".format(self.convert_size(data.get(i)), self.h_convert_size(data.get(i)))
                else:
                    print str(i).title() + " " * (max(each_len_keys) - len(i)) + " : " + str((data.get(i)))
        return data    

    def upload(self, fileorurl, path='/', folderid=0, username=None, password=None):
        # filepath = open(filepath, 'rb')
        assert (filepath != None), "Please Insert File Path upload to !"
        if username == None or password == None:
            try:
                username, password = self.setUserPass()
            except:
                username = self.username
                password = self.password
        # auth = self.getAuth(username, password)
        # URL = self.setURL('uploadfile?auth={0}&path={1}&folderid={2}&filename={3}'.format(auth, path, folderid, filepath))
        URL = self.setURL('uploadfile?username={0}&password={1}&path={2}&folderid={3}&filename={4}'.format(
            username, password, path, folderid, filepath))
        return json.loads(self.getURL1(URL)[0])

    def folderInfo(self, auth=None, username=None, password=None, excpt='contents'):
        data = self.listFolder(self.getAuth(
            auth, username, password), username=username, password=password)
        for i in data.get('metadata'):
            if i == excpt:
                pass
            else:
                debug(i, data.get(
                    'metadata').get(i), 'folderInfo', 30)

    def listFolder(self, auth=None, path='/', folderid='0', recursive=0, showdelete=0, nofiles=0, noshares=0, username=None, password=None):
        assert (path != None), "Please Insert Folder Path !"
        assert (folderid != None), "Folder ID is None !"
        if username != None and password != None:
            debug(username="None", password="None")
            self.username = username
            self.password = password
            URL = self.setURL('listfolder?username={0}&password={1}&path={2}&folderid={3}&recursive={4}&showdeleted={5}&nofiles={6}&noshares={7}'.format(
                username, password, path, folderid, recursive, showdelete, nofiles, noshares))
            return json.loads(self.getURL1(URL)[0])
        else:
            if auth:
                if self.auth:
                    debug(auth=self.AUTH(auth, username, password)[0])
                    URL = self.setURL('listfolder?auth={0}&path={1}&folderid={2}&recursive={3}&showdeleted={4}&nofiles={5}&noshares={6}'.format(
                        self.AUTH, path, folderid, recursive, showdelete, nofiles, noshares))
                    debug(URL=URL)
                else:
                    debug(auth_stmt='else', auth=self.AUTH(
                        auth, username, password)[0])
                    URL = self.setURL('listfolder?auth={0}&path={1}&folderid={2}&recursive={3}&showdeleted={4}&nofiles={5}&noshares={6}'.format(
                        auth, path, folderid, recursive, showdelete, nofiles, noshares))
                    debug(URL=URL)
                return json.loads(self.getURL1(URL)[0])
            elif self.getAuth(auth, username, password):
                debug(getAuth=str(self.getAuth))
                URL = self.setURL('listfolder?auth={0}&path={1}&folderid={2}&recursive={3}&showdeleted={4}&nofiles={5}&noshares={6}'.format(
                    self.getAuth(auth, username, password), path, folderid, recursive, showdelete, nofiles, noshares))
                debug(URL=URL)
                return json.loads(self.getURL1(URL)[0])
            else:
                print "Please login again !"
                sys.exit(0)

    def createFolder(self, foldername, folderid=0, auth=None, username=None, password=None):
        # https://api.pcloud.com/createfolder?folderid=0&name=BULETIN+AT-TAQWA&auth=lgdcGVZBz6KZ49nFAGzKOy4nluWXYLz4gBXA5XcV
        URL = 'https://api.pcloud.com/createfolder'
        #url = 'createfolder'
        #URL = self.setURL(url)
        params = {
            'folderid': folderid,
            'name': foldername,
            'auth': self.getAuth(auth, username, password),
        }

        contents, cookies = self.getURL1(URL, params)
        data = json.loads(contents)
        debug('createFolder', data=data)
        return data

    def movefile(self, fileid, tofolderid=0, toname=None, auth=None, username=None, password=None):
        # https://api.pcloud.com/createfolder?folderid=0&name=BULETIN+AT-TAQWA&auth=lgdcGVZBz6KZ49nFAGzKOy4nluWXYLz4gBXA5XcV
        URL = 'https://api.pcloud.com/renamefile'
        #url = 'createfolder'
        #URL = self.setURL(url)
        params = {
            'fileid': fileid,
            'tofolderid': tofolderid,
            'auth': self.getAuth(auth, username, password),
            'toname': toname,
        }

        contents, cookies = self.getURL1(URL, params)
        data = json.loads(contents)
        debug('movefile', data=data)
        return data

    def movefolder(self, folderid, tofolderid=0, toname=None, auth=None, username=None, password=None):
        # https://api.pcloud.com/createfolder?folderid=0&name=BULETIN+AT-TAQWA&auth=lgdcGVZBz6KZ49nFAGzKOy4nluWXYLz4gBXA5XcV
        URL = 'https://api.pcloud.com/renamefolder'
        #url = 'createfolder'
        #URL = self.setURL(url)
        params = {
            'folderid': folderid,
            'tofolderid': tofolderid,
            'auth': self.getAuth(auth, username, password),
            'toname': toname,
        }

        contents, cookies = self.getURL1(URL, params)
        data = json.loads(contents)
        debug('movefolder', data=data)
        return data

    def renameFile(self, newname, fileid, auth=None, username=None, password=None):
        # https://api.pcloud.com/renamefile?toname=CCleaner+5.28.6005+(All+Editions)+%2B+Keygen.zip&fileid=2429137537&auth=lgdcGVZBz6KZ49nFAGzKOy4nluWXYLz4gBXA5XcV
        debug(fileid = fileid)
        URL = 'https://api.pcloud.com/renamefile'
        #url = 'createfolder'
        #URL = self.setURL(url)
        params = {
            'toname': newname,
            'fileid': fileid,
            'auth': self.getAuth(auth, username, password),
        }

        contents, cookies = self.getURL1(URL, params)
        data = json.loads(contents)
        debug('renameFile', data=data)
        return data

    def changePass(self, oldpass, newpass, auth=None, username=None, password=None):
        # https://api.pcloud.com/changepassword
        URL = 'https://api.pcloud.com/changepassword'
        params = {
            'oldpassword': oldpass,
            'newpassword': newpass,
            'auth': self.getAuth(auth, username, password),
        }

        contents, cookies = self.getURL1(URL, params)
        data = json.loads(contents)
        debug(data=data)
        return data

    def build_dict(self, seq, key):
        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))
    
    def sizeof(self, num):
        for x in [' bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0    

    def getContents(self, auth=None, path='/', folderid='0', recursive=0, showdelete=0, nofiles=0, noshares=0, username=None, password=None, interactive=False, download_path=".", output=None, nlist=None, quite = False, no_print_list = False, q = None, input_method = ''):
        
        if nlist:
            self.nlist = nlist
        userdata = self.userInfo(auth, username, password, False)
        debug(userdata = userdata)
        if userdata.get('result'):
            debug(userdata_error = userdata.get('error'))
            debug(type_userdata_error = type(userdata.get('error')))
            if userdata.get('result') == 2000 or userdata.get('result') == '2000':
                self.islogin = False
                username = raw_input('LOGIN EMAIL[USERNAME]: ')
                password = getpass.getpass('LOGIN PASSWORD: ')
                auth = self.login(username, password).get('auth')
                if not username and not password:
                    username = None
                    password = None
                #return self.getContents(auth, '/', 0, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
        else:
            if userdata.get('result') != 1000:
                user_email = str(userdata.get('email')) + ", "
                used_quota = self.convert_size(userdata.get('usedquota')) + ", "
                quota = self.convert_size(userdata.get('quota')) + ", "

        def get_contents(auth=auth, path=pcloud, folderid=folderid, recursive=recursive, showdelete=showdelete, nofiles=nofiles, noshares=noshares, username=username, password=password, interactive=interactive, download_path=download_path, output=output):  #return list_name, list_sort, contents
            if self.listFolder(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password) == None:
                return self.getContents(auth, path, parentfolderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
            if self.listFolder(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password) == None:
                self.print_nav(auth, username, password)
            if self.listFolder(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password).get('metadata') == None:
                return self.getContents(auth, path, parentfolderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)            
            contents = self.listFolder(auth, path, folderid, recursive, showdelete,
                                       nofiles, noshares, username, password).get('metadata').get('contents')
            #debug(contents=contents, debug= True)
            if download_path == ".":
                download_path = os.getcwd()
            download_path = os.path.abspath(download_path)
            debug(download_path=download_path)
            n = 1
            list_name = []
            list_sort = {}
            for i in contents:
                # print "i =", i
                #list_name.append(str(n) + ". " + str(i.get('name')))
                list_sort.update({n: i, })
                
                if i.get('isFolder'):
                    # print str(n) + ".", i.get('name'), "[Folder]"
                    list_name.append(
                        str(n) + ". " + make_colors(i.get('name'), 'lightcyan', color_type= 'colorama') + " [" + make_colors("Folder", 'white', 'magenta', color_type= 'colorama') + "] ["+ "%s" % self.sizeof(i.get('size')) + "]")
                else:
                    # print str(n) + ".", i.get('name'), "[" +
                    # i.get('contenttype').split('/')[-1] + "]"
                    if i.get('contenttype') == None:
                        list_name.append(
                            str(n) + ". " + make_colors(i.get('name'), 'lightcyan', color_type= 'colorama') + " [" + make_colors("Folder", 'white', 'magenta', color_type= 'colorama') + "]")
                    else:
                        list_name.append(str(n) + ". " + make_colors(i.get('name'), 'lightblue') + " [" +
                                         make_colors(i.get('contenttype').split('/')[-1], 'red', 'yellow') + "] [" + make_colors("%s" % self.sizeof(i.get('size')), 'white', 'red') + "]")

                n += 1
            return list_name, list_sort, contents
        folderid = folderid
        parentfolderid = 0
        if nlist:
            nlist = int(nlist)
        else:
            nlist = 2
        # print "nlist =", nlist
        list_name, list_sort, contents = get_contents()
        if quite:
            return list_name, list_sort, contents
        if not no_print_list:
            if list_name:
                self.makeList(list_name, nlist)
            else:
                print termcolor.colored('NO DATA !', 'red', 'on_yellow', attrs= ['blink'])
            #else:
                #self.print_nav(auth, username, password)
        if input_method == 'msvcrt':
            self.print_nav(auth)
            p = msvcrt.getch()
        else:
            p = raw_input(self.print_nav(auth))
            p = str(p).strip()
        list_steps = {
            0: 0,
        }        
        while 1:
            if p != chr(27):
                if p == 'b':
                    #debug(list_steps_back_1 = list_steps, debug= True)
                    if not list_steps:
                        parentfolderid = 0
                        print make_colors('THIS IS ROOT', 'white', 'red')
                    else:
                        parentfolderid = list_steps.get(max(list_steps.keys()))
                        list_steps.pop(max(list_steps.keys()))
                    return self.getContents(auth, path, parentfolderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                    #debug(list_steps_back_2 = list_steps, debug= True)
                    #list_name, list_sort, contents = get_contents(
                        #folderid=parentfolderid)
                    #info_by_name = self.build_dict(contents, key="name")
                    #result = info_by_name[list_sort.get(int(q)).get('name')]
                    #parentfolderid = result.get('parentfolderid')
                    #self.makeList(list_name, nlist)
                    #self.print_nav(auth)
                    #p = msvcrt.getch()
                    #continue
                elif p == 'w':
                    break
                elif p == 'z':
                    username = raw_input('REGISTER EMAIL[USERNAME]: ')
                    password = getpass.getpass('REGISTER PASSWORD: ')
                    repassword = getpass.getpass('RETRY PASSWORD: ')
                    if password == repassword:
                        if username and password:
                            auth = self.register(username, password, print_user_info=False)
                        else:
                            username = None
                            password = None
                        return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                    else:
                        print make_colors("PASSWORD NOT MATCH !", 'white', 'red', attrs= ['bold', 'blink'])
                elif p == 's':
                    #save config
                    try:
                        self.setAuth(auth)
                        print make_colors('Save config ...', 'white', 'yellow', attrs= ['bold'])
                    except:
                        print make_colors('ERROR: Save config !', 'white', 'red', attrs= ['bold'])
                    
                    return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                
                elif p == 'i':
                    #change input method
                    qi = raw_input('Input Method [msvcrt or None[empty|just enter]: ')
                    #if str(qi).strip() and str(qi).strip().lower() == 'msvcrt':
                    return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite, input_method = str(qi).strip().lower())
                    
                elif p == 'c':
                    os.system('cls')
                    return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                elif p == 't':
                    username = raw_input('LOGIN EMAIL[USERNAME]: ')
                    password = getpass.getpass('LOGIN PASSWORD: ')
                    auth = self.login(username, password).get('auth')
                    if not username and not password:
                        username = None
                        password = None
                    return self.getContents(auth, '/', 0, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                elif p == 'e':
                    #debug(list_steps_ex_1 = list_steps, debug= True)
                    q = raw_input('Select number to explore:')
                    if str(q).isdigit():
                        info_by_name = self.build_dict(contents, key="name")
                        result = info_by_name[
                            list_sort.get(int(q)).get('name')]
                        folderid = result.get('folderid')
                        self.folderid = folderid
                        parentfolderid = result.get('parentfolderid')
                        list_steps.update({
                            max(list_steps.keys()) + 1: parentfolderid,
                        })
                        #debug(list_steps_ex_2 = list_steps, debug= True)
                        # debug(folderid = folderid, debug=True)
                        #list_name, list_sort, contents = get_contents(
                            #folderid=folderid)
                        # debug(content_explorer=content, debug=True)
                        #self.makeList(list_name, nlist)
                        #self.print_nav(auth)
                        #p = msvcrt.getch()
                        #continue
                        return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                    return self.getContents(auth, path, self.folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                elif p == 'u':
                    q = raw_input('Input File Path/Url:')
                    if q:
                        if "folder:" in q:
                            q = unichr(q).split('folder:')
                            url, folder_name = q
                            folder = self.mkdir(folder_name, username,
                                                password, folderid=self.folderid).get('folderid')
                        else:
                            folder = None
                            url = q
                        if os.path.isfile(q):
                            self.fileUploadStart(
                                url, auth, username, password, folder, progresshash=self.getHash())
                        else:
                            self.remoteUpload(url.strip(), auth, username, password,
                                              folder, progresshash=self.getHash())
                        #list_name, list_sort, contents = get_contents(
                            #folderid=folderid)
                        # debug(content_explorer=content, debug=True)
                        #self.makeList(list_name, nlist)
                        #self.print_nav(auth)
                        #p = msvcrt.getch()
                        #return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                    return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)                       

                elif p == 'g':
                    q = raw_input('Select number to move:')
                    if "," in q:
                        q0 = str(q).strip().split(",")
                        for i in q0:
                            if "a" in q0:
                                q1 = None
                            else:
                                q1 = raw_input('rename to [enter for pass]:')
                            f = raw_input('Select number move to [folder]:')
                            if str(i).isdigit():
                                info_by_name = self.build_dict(
                                    contents, key="name")
                                result = info_by_name[
                                    list_sort.get(int(i)).get('name')]
                                result2 = info_by_name[
                                    list_sort.get(int(f)).get('name')]
                                if result.get('isfolder'):
                                    folderid = result.get('folderid')
                                    if result2.get('isfolder'):
                                        tofolderid = result2.get('folderid')
                                        name0 = result.get('name')
                                        if q1:
                                            toname = q1
                                        else:
                                            toname = name0
                                    # movefolder(self, folderid, tofolderid=0,
                                    # toname = None, auth=None, username=None,
                                    # password=None):
                                    self.movefolder(
                                        folderid, tofolderid, toname, auth, username, password)
                                else:
                                    fileid = result.get('fileid')
                                    if result2.get('isfolder'):
                                        tofolderid = result2.get('folderid')
                                        name0 = result.get('name')
                                        if q1:
                                            toname = q1
                                        else:
                                            toname = name0
                                    self.movefile(
                                        fileid, tofolderid, toname, auth, username, password)

                    else:
                        q1 = raw_input('rename to [enter for pass]:')
                        f = raw_input('Select number move to [folder]:')
                        if str(q).isdigit():
                            info_by_name = self.build_dict(
                                contents, key="name")
                            result = info_by_name[
                                list_sort.get(int(q)).get('name')]
                            result2 = info_by_name[
                                list_sort.get(int(f)).get('name')]
                            if result.get('isfolder'):
                                folderid = result.get('folderid')
                                if result2.get('isfolder'):
                                    tofolderid = result2.get('folderid')
                                    name0 = result.get('name')
                                    if q1:
                                        toname = q1
                                    else:
                                        toname = name0
                                # movefolder(self, folderid, tofolderid=0,
                                # toname = None, auth=None, username=None,
                                # password=None):
                                self.movefolder(
                                    folderid, tofolderid, toname, auth, username, password)
                            else:
                                fileid = result.get('fileid')
                                if result2.get('isfolder'):
                                    tofolderid = result2.get('folderid')
                                    name0 = result.get('name')
                                    if q1:
                                        toname = q1
                                    else:
                                        toname = name0
                                self.movefile(fileid, tofolderid,
                                              toname, auth, username, password)
                        #self.folderid = folderid
                        #parentfolderid = result.get('parentfolderid')
                        # debug(folderid = folderid, debug=True)
                        list_name, list_sort, contents = get_contents(
                            folderid=self.folderid)
                        # debug(content_explorer=content, debug=True)
                        self.makeList(list_name, nlist)
                        self.print_nav(auth)
                        p = msvcrt.getch()
                        #continue
                    return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                elif p == 'C':
                    q = raw_input('Select number to copy download link:')
                    if "name:" in q:
                        q, output = str(q).split('name:')
                        q = q.strip()
                        output = str(output).strip()
                        if not os.path.isdir(output):
                            os.makedirs(output)
                    if str(q).isdigit():
                        info_by_name = self.build_dict(contents, key="name")
                        #debug('getcontents', list_sort = str(list_sort))
                        # print "getContents -> list_sort"
                        # print list_sort
                        # print "-" * 220
                        result = info_by_name[
                            list_sort.get(int(q)).get('name')]
                        # print "result ->", result
                        print "copy download link of", result.get('name'), '...'
                        data, cookies = self.getDownloadLink(result.get('id'), download_path = download_path)
                        download_url = 'https://' + \
                            data.get('hosts')[0] + data.get('path')
                        clipboard.copy(download_url)                        
                    return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)                
                elif p == 'd':
                    q = raw_input('Select number to download:')
                    if "name:" in q:
                        q, output = str(q).split('name:')
                        q = q.strip()
                        output = str(output).strip()
                        if not os.path.isdir(output):
                            os.makedirs(output)
                    if str(q).isdigit():
                        info_by_name = self.build_dict(contents, key="name")
                        #debug('getcontents', list_sort = str(list_sort))
                        # print "getContents -> list_sort"
                        # print list_sort
                        # print "-" * 220
                        result = info_by_name[
                            list_sort.get(int(q)).get('name')]
                        # print "result ->", result
                        if result.get('isfolder'):
                            name = result.get('name') + ".zip"
                            if name:
                                filename = name
                            else:
                                filename = output
                            print "download", filename, '...'
                            self.download_aszip(result.get('folderid'), auth, username, password, filename, debug= self.debug)
                            return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                        else:
                            print "download", result.get('name'), '...'
                            data, cookies = self.getDownloadLink(result.get('id'), download_path = download_path)
                            download_url = 'https://' + \
                                data.get('hosts')[0] + data.get('path')
                            if output:
                                self.download(
                                    download_url, download_path, output, cookies)
                            else:
                                self.download(
                                    download_url, download_path, cookies=cookies)
                            return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                    elif str(q) == 'a' or str(q) == 'all':
                        if "name:" in q:
                            q, output = str(q).split('name:')
                            q = q.strip()
                            output = str(output).strip()
                            if not os.path.isdir(output):
                                os.makedirs(output)
                        for x in list_sort:
                            result = info_by_name[list_sort.get(x).get('name')]                            
                            print "download", list_sort.get(x).get('name'), '...'
                            if result.get('isfolder'):
                                name = result.get('name') + ".zip"
                                if name:
                                    filename = name
                                else:
                                    filename = output
                                print "download", filename, '...'
                                self.download_aszip(result.get('folderid'), auth, username, password, filename, debug= self.debug)
                                #return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                            else:
                                data, cookies = self.getDownloadLink(
                                    list_sort.get(x).get('id'), download_path = download_path)
                                download_url = 'https://' + \
                                    data.get('hosts')[0] + data.get('path')
                                if output:
                                    self.download(
                                        download_url, download_path, output, cookies)
                                else:
                                    self.download(
                                        download_url, download_path, cookies=cookies)
                        return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                    elif "," in str(q):
                        q1 = str(q).strip().split(",")
                        for i in q1:
                            if "name:" in i:
                                q, output = str(q).split('name:')
                                q = q.strip()
                                output = str(output).strip()
                                if not os.path.isdir(output):
                                    os.makedirs(output)
                            if str(i).isdigit():
                                info_by_name = self.build_dict(
                                    contents, key="name")
                                #debug('getcontents', list_sort = str(list_sort))
                                # print "getContents -> list_sort"
                                # print list_sort
                                # print "-" * 220
                                result = info_by_name[
                                    list_sort.get(int(i)).get('name')]
                                if result.get('isfolder'):
                                    name = result.get('name') + ".zip"
                                    if name:
                                        filename = name
                                    else:
                                        filename = output
                                    print "download", filename, '...'
                                    self.download_aszip(result.get('folderid'), auth, username, password, filename, debug= self.debug)
                                    #return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                                else:
                                    print "download", result.get('name'), '...'
                                    data, cookies = self.getDownloadLink(
                                        result.get('id'), download_path = download_path)
                                    download_url = 'https://' + \
                                        data.get('hosts')[0] + data.get('path')
                                    if output:
                                        self.download(
                                            download_url, download_path, output, cookies)
                                    else:
                                        self.download(
                                            download_url, download_path, cookies=cookies)
                        return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                    elif " " in str(q):
                        q1 = str(q).strip().split(" ")
                        for i in q1:
                            if "name:" in i:
                                q, output = str(q).split('name:')
                                q = q.strip()
                                output = str(output).strip()
                                if not os.path.isdir(output):
                                    os.makedirs(output)
                            if str(i).isdigit():
                                info_by_name = self.build_dict(
                                                        contents, key="name")
                                #debug('getcontents', list_sort = str(list_sort))
                                # print "getContents -> list_sort"
                                # print list_sort
                                # print "-" * 220
                                result = info_by_name[
                                                        list_sort.get(int(i)).get('name')]
                                if result.get('isfolder'):
                                    name = result.get('name') + ".zip"
                                    if name:
                                        filename = name
                                    else:
                                        filename = output
                                    print "download", filename, '...'
                                    self.download_aszip(result.get('folderid'), auth, username, password, filename, debug= self.debug)
                                    #return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                                else:
                                    print "download", result.get('name'), '...'
                                    data, cookies = self.getDownloadLink(
                                                            result.get('id'), download_path = download_path)
                                    download_url = 'https://' + \
                                                            data.get('hosts')[0] + data.get('path')
                                    if output:
                                        self.download(
                                                                download_url, download_path, output, cookies)
                                    else:
                                        self.download(
                                                                download_url, download_path, cookies=cookies)
                        return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)                    
                elif p == 'r':
                    q1 = raw_input('Select Number: ')
                    newname = raw_input('New Name: ')
                    if q1 == 'q' or newname == 'q':
                        sys.exit(0)
                    if str(q1).isdigit():
                        info_by_name = self.build_dict(contents, key="name")
                        result = info_by_name[
                            list_sort.get(int(q1)).get('name')]
                        debug('getContents', p='r', result=result)
                        if result.get('isfolder'):
                            fid = result.get('folderid')
                        else:
                            fid = result.get('fileid')
                        debug('getContents', p='r', fid=fid)
                        auth = self.getAuth(auth, username, password)
                        self.renameFile(newname, fid, auth, username, password)
                    # self.getContents(auth, path, folderid, recursive, showdelete, nofiles,
                        # noshares, username, password, interactive,
                        # download_path, output)
                    return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)

                elif p == 'm':
                    q1 = raw_input('Select Number Delete/Remove to: ')
                    if str(q1).isdigit():
                        info_by_name = self.build_dict(contents, key="name")
                        result = info_by_name[
                            list_sort.get(int(q1)).get('name')]
                        debug('getContents', p='r', result=result)
                        auth = self.getAuth(auth, username, password)
                        if result.get('isfolder'):
                            fid = result.get('folderid')
                            debug('getContents', p='m', fid=fid)
                            self.delete(fid, auth=auth,
                                        username=username, password=password)
                        else:
                            fid = result.get('fileid')
                            debug('getContents', p='m', fid=fid)
                            self.delete(fileid=fid, auth=auth,
                                        username=username, password=password)
                    elif ',' in str(q1).strip():
                        q1 = str(q1).strip().split(',')
                        for i in q1:
                            i = str(i).strip()
                            info_by_name = self.build_dict(
                                contents, key="name")
                            result = info_by_name[
                                list_sort.get(int(i)).get('name')]
                            debug('getContents', p='m', result=result)
                            auth = self.getAuth(auth, username, password)
                            if result.get('isfolder'):
                                fid = result.get('folderid')
                                debug('getContents', p='m', fid=fid)
                                self.delete(fid, auth=auth, username=username,
                                            password=password)
                            else:
                                fid = result.get('fileid')
                                debug('getContents', p='m', fid=fid)
                                self.delete(fileid=fid, auth=auth,
                                            username=username, password=password)
                    elif '-' in str(q1).strip():
                        fr, to = str(q1).strip().split('-')
                        fr = str(fr).strip()
                        to = str(to).strip()
                        for i in range(int(fr), (int(to) + 1)):
                            i = str(i).strip()
                            info_by_name = self.build_dict(
                                contents, key="name")
                            result = info_by_name[
                                list_sort.get(int(i)).get('name')]
                            debug('getContents', p='m', result=result)
                            auth = self.getAuth(auth, username, password)
                            if result.get('isfolder'):
                                fid = result.get('folderid')
                                debug('getContents', p='m', fid=fid)
                                self.delete(fid, auth=auth, username=username,
                                            password=password)
                            else:
                                fid = result.get('fileid')
                                debug('getContents', p='m', fid=fid)
                                self.delete(fileid=fid, auth=auth,
                                            username=username, password=password)
                    elif ' ' in str(q1).strip():
                        q1 = str(q1).strip().split(' ')
                        for i in q1:
                            if not i == '':
                                i = str(i).strip()
                                info_by_name = self.build_dict(
                                    contents, key="name")
                                result = info_by_name[
                                    list_sort.get(int(i)).get('name')]
                                debug(
                                    'getContents', p='m', result=result)
                                auth = self.getAuth(auth, username, password)
                                if result.get('isfolder'):
                                    fid = result.get('folderid')
                                    debug(
                                        'getContents', p='m', fid=fid)
                                    self.delete(fid, auth=auth, username=username,
                                                password=password)
                                else:
                                    fid = result.get('fileid')
                                    debug(
                                        'getContents', p='m', fid=fid)
                                    self.delete(fileid=fid, auth=auth,
                                                username=username, password=password)
                    else:
                        print "Please Insert Correct Number !"
                    return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                elif p == 'a':
                    for x in list_sort:
                        result = info_by_name[
                            list_sort.get(int(x)).get('name')]
                        if result.get('isfolder'):
                            name = result.get('name') + ".zip"
                            if name:
                                filename = name
                            else:
                                filename = output
                            print "download", filename, '...'
                            self.download_aszip(result.get('folderid'), auth, username, password, filename, debug= self.debug)
                            return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                        else:
                            print "download", list_sort.get(x).get('name'), '...'
                            data, cookies = self.getDownloadLink(
                                list_sort.get(x).get('id'), download_path = download_path)
                            download_url = 'https://' + \
                                data.get('hosts')[0] + data.get('path')
                            if output:
                                self.download(
                                    download_url, download_path, output, cookies)
                            else:
                                self.download(
                                    download_url, download_path, cookies=cookies)
                            return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                elif p == 'q':
                    sys.exit(0)
                elif p == 'f':
                    #createFolder(self, foldername, folderid=0, auth=None, username=None, password=None)
                    foldername = raw_input('Folder Name:')
                    auth = self.getAuth(auth, username, password)
                    self.createFolder(foldername, self.folderid,
                                      auth, username, password)
                    return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                else:
                    if str(p).isdigit():
                        if str(p) == '0':
                            pass
                        else:
                            info_by_name = self.build_dict(contents, key="name")
                            result = info_by_name[
                                list_sort.get(int(p)).get('name')]
                            if result.get('isfolder'):
                                name = result.get('name') + ".zip"
                                if name:
                                    filename = name
                                else:
                                    filename = output
                                print "download", filename, '...'
                                self.download_aszip(result.get('folderid'), auth, username, password, filename, debug= self.debug)
                                return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
                            else:
                                print "download", result.get('name'), '...'
                                data, cookies = self.getDownloadLink(result.get('id'), download_path = download_path)
                                download_url = 'https://' + \
                                    data.get('hosts')[0] + data.get('path')
                                #self.download(download_url, download_path)
                                if output:
                                    self.download(
                                        download_url, download_path, output, cookies)
                                else:
                                    self.download(
                                        download_url, download_path, cookies=cookies)
                            return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
            else:
                return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
        return self.getContents(auth, path, folderid, recursive, showdelete, nofiles, noshares, username, password, interactive, download_path, output, nlist, quite)
    
    def progress(self, sizes, step):
        sizes = int(sizes)
        widgets = [
            Percentage(),
            ' ', Bar(),
            ' ', ETA(),
            ' ', AdaptiveETA(),
            ' ', AdaptiveTransferSpeed(),
        ]
        pbar = ProgressBar(widgets=widgets, max_value=sizes)
        pbar.start()
        # for i in range(sizes):
        #time.sleep(0.001 + (i < 100) * 0.0001 + (i > 400) * 0.009)
        time.sleep(0.001 + (i < 100) * 0.0001 + (i > 400) * 0.009)
        pbar.update(step)
        pbar.finish()

    def run_in_separate_process(self, func, *args, **kwds):
        pread, pwrite = os.pipe()
        pid = os.fork()
        if pid > 0:
            os.close(pwrite)
            with os.fdopen(pread, 'rb') as f:
                status, result = cPickle.load(f)
            os.waitpid(pid, 0)
            if status == 0:
                return result
            else:
                raise result
        else:
            os.close(pread)
            try:
                result = func(*args, **kwds)
                status = 0
            except Exception, exc:
                result = exc
                status = 1
            with os.fdopen(pwrite, 'wb') as f:
                try:
                    cPickle.dump((status, result), f, cPickle.HIGHEST_PROTOCOL)
                except cPickle.PicklingError, exc:
                    cPickle.dump((2, exc), f, cPickle.HIGHEST_PROTOCOL)
            os._exit(0)

    def uploadprogress(self, auth=None, username=None, password=None, progresshash='upload-9392343-xhr-816'):
        
        if self.progresshash:
            progresshash = self.progresshash
        else:
            self.progresshash = progresshash
        progresshash = self.progresshash
        current_server = self.getCurrentServer().get('hostname')
        URL = 'https://' + current_server + '/uploadprogress'
        params = {
            'auth': self.getAuth(auth, username, password),
            'progresshash': progresshash,
        }
        try:
            data1 = self.getURL2(URL, params)
            debug('uploadprogress', data1=data1)
            data = json.loads(data1)
        except:
            data = {}
            import traceback
            print traceback.format_exc()
        return auth, data

    def datapost_upload_generator(self, fullfilepath):
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers

        data, headers = multipart_encode(
            {os.path.basename(fullfilepath): open(fullfilepath)})
        debug('datapost_upload_generator', headers=headers)
        return data, headers

    def fileUpload(self, filepath, auth=None, username=None, password=None, folderid=0, nopartial=1, progresshash=None, renameit=None, foldername=None, debug=False):
        if foldername:
            self.mkdir(foldername, auth, username, password, folderid)
        if not progresshash:
            progresshash = self.getHash(debug=debug)
        from multiprocessing.pool import ThreadPool
        pool = ThreadPool(processes=1)

        if self.nopartial:
            nopartial = self.notpartial
        if self.progresshash:
            progresshash = self.progresshash
        else:
            self.progresshash = progresshash
        current_server = self.getCurrentServer().get('hostname')
        URL = 'https://' + current_server + '/uploadfile'
        debug('fileUpload', URL=URL, debug=debug)
        n = 1

        finished = {}
        params = {
            'auth': self.getAuth(auth, username, password),
            'folderid': folderid,
            'nopartial': nopartial,
            'progresshash': progresshash,
        }
        data_post, headers = self.datapost_upload_generator(filepath)
        data = {
            'Source': data_post,
        }

        debug('fileUpload', params=params, debug=debug, )
        debug('fileUpload', data=data, debug=debug, )
        result = pool.apply_async(
            self.getURL3, (URL, filepath, params, headers))
        # print "fileUpload -> result:", result.get()
        #debug('fileUpload', result_0 = result.get(), )
        auth, uploaded = self.uploadprogress(
            auth, username, password, progresshash)
        uploaded = uploaded.get('uploaded')
        auth, total = self.uploadprogress(
            auth, username, password, progresshash)
        total = total.get('total')
        widgets = [
            Percentage(),
            ' ', Bar(),
            ' ', ETA(),
            ' ', AdaptiveETA(),
            ' ', AdaptiveTransferSpeed(),
        ]

        while 1:
            if uploaded == '' or uploaded == None:
                auth, uploaded = self.uploadprogress(
                    auth, username, password, progresshash)
                uploaded = uploaded.get('uploaded')
                #debug('fileUpload', uploaded_1 = uploaded)
                auth, total = self.uploadprogress(
                    auth, username, password, progresshash)
                total = total.get('total')
                #debug('fileUpload', total = total)
            else:
                pbar = ProgressBar(widgets=widgets, max_value=total)
                pbar.start()
                break
        while 1:
            if total != uploaded:
                pbar.update(uploaded)
                auth, uploaded = self.uploadprogress(
                    auth, username, password, progresshash)
                uploaded = uploaded.get('uploaded')
                #debug('fileUpload', uploaded_2 = uploaded)
                time.sleep(0.2)
            else:
                auth, finish = self.uploadprogress(
                    auth, username, password, progresshash)
                debug('fileUpload', finish=finish, debug=debug)
                pbar.finish()
                break
        #finished.update({n: [json.loads(finish), json.loads(result.get())],})
        # return finished

        # if isinstance(filepath, list):
            # for i in filepath:
                # fileProcess(i)
        # else:
        #finished = fileProcess(filepath, auth)

        data_return = json.loads(result.get())
        if renameit:
            fileid = data_return.get('metadata')[0].get('fileid')
            self.renameFile(newname, fileid, auth, username, password)
        #debug('fileUpload', data = str(data))
        # return data
        #debug('fileUpload', finished = str(finished))
        return data_return

    def fileUploadStart(self, filepath, auth=None, username=None, password=None, folderid=0, nopartial=1, progresshash=None, renameit=None):
        for i in filepath:
            result = self.fileUpload(i, auth, username, password,
                                     folderid, nopartial, progresshash, renameit=renameit)
            #debug('fileUploadStart', result = result)
            print 'result =', result

    def remoteUpload(self, url, auth=None, username=None, password=None, folderid=0, nopartial=1, progresshash='upload-9392343-xhr-816', renameit=None, foldername=None):
        debug(url = url)
        data = {}
        data_result = {}
        if foldername:
            mkfolder = self.mkdir(foldername, auth, username,
                                  password, folderid)

            debug(mkfolder=mkfolder)
            folderid = mkfolder.get('folderid')
            debug(folderid=folderid)

        debug(progresshash=progresshash)
        from multiprocessing.pool import ThreadPool
        pool = ThreadPool(processes=1)

        if self.nopartial:
            nopartial = self.notpartial
        if self.progresshash:
            progresshash = self.progresshash
        else:
            self.progresshash = progresshash
        current_server = self.getCurrentServer().get('hostname')
        URL = 'https://' + current_server + '/downloadfile'
        debug(URL=URL)
        params = {
            'auth': self.getAuth(auth, username, password),
            'folderid': folderid,
            'nopartial': nopartial,
            'progresshash': progresshash,
            'url': url,
        }

        debug(params=params)
        result = pool.apply_async(self.getURL2, (URL, params, 'post'))
        #debug('remoteUpload', result_get = result.get())

        auth, downloaded = self.uploadprogress(
            auth, username, password, progresshash)
        
        debug(downloaded=downloaded)
        
        if hasattr(downloaded, 'files'):                        
            if downloaded.get('files')[0].get('status') == 'error':
                debug(
                    'remoteUpload', downloaded='ERROR', ERROR=downloaded)
                print "DOWNLOAD ERROR [main] !"
                sys.exit(0)

        
        if json.loads(result.get()).get('result') == 2008:
            print make_colors("OVER QUOTA !", 'white', 'red', attrs= ['blink'])
            self.userInfo()
            sys.exit(0)
        else:
            if downloaded.get('result') == 1900:
                print make_colors("DOWNLOAD ERROR [1900-1] !", 'white', 'red', ['bold', 'blink']) + make_colors(downloaded.get('error'), 'white', 'blue')
                sys.exit(0)
        debug(downloaded = downloaded)
        if downloaded.get('result') == 1900:
            print make_colors("DOWNLOAD ERROR [1900-2] !", 'white', 'red', ['bold', 'blink']) + make_colors(downloaded.get('error'), 'white', 'blue')
            sys.exit(0)
        
        debug(download_0 = downloaded)
        debug(type_download_0 = type(downloaded))
        if downloaded.has_key('files'):
            sizes = downloaded.get('files')[0].get('size')
        else:
            pass
        
        files = downloaded.get('files')
        if isinstance(downloaded, dict):
            for p in files:                
                downloaded_size = p.get('downloaded')
                debug(downloaded_1 = downloaded)
                size = p.get('size')
        
                widgets = [
                    Percentage(),
                    ' ', Bar(),
                    ' ', ETA(),
                    ' ', AdaptiveETA(),
                    ' ', AdaptiveTransferSpeed(),
                ]
                pbar = ProgressBar(widgets=widgets, max_value=sizes)
                pbar.start()                            
                while 1:
                    debug(size = size)
                    debug(downloaded = downloaded)
                    if p.get('finished') == True:
                        pbar.finish()
                        debug(status = p.get('status'))
                        break
                    elif p.get('finished') == False:
                        debug(status = p.get('status'))
                        debug(ERROR = 'Download Interupted by SYSTEM and still download in background by SYSTEM !')
                        print make_colors('Download Interupted by SYSTEM and still download in background by SYSTEM !', 'white', 'red')
                        sys.exit('Download Interupted by SYSTEM and still download in background by SYSTEM !')
                        break
                    else:
                        if size == downloaded_size:
                            pbar.finish()
                            if renameit:
                                data = json.loads(result.get())
                                debug(data = data)
                                fileid = data.get('metadata')[files.index(p)].get('fileid')
                                #debug(downloaded = downloaded)
                                #debug(p = downloaded.get('files')[files.index(p)])
                                #debug(type_p = type(downloaded.get('files')[files.index(p)]))
                                #fileid = unicode(downloaded.get('files')[files.index(p)].get('fileid'))
                                debug(fileid = fileid)
                                self.renameFile(renameit, fileid, auth, username, password)
                                if fileid:
                                    if not data_result:
                                        data_result = json.loads(result.get())
                                    data_result.get('metadata')[files.index(p)].update({'name': renameit,})
                            break
                        else:
                            debug(downloaded_size = downloaded_size)
                            pbar.update(downloaded_size)
                            auth, downloaded = self.uploadprogress(auth, username, password, progresshash)
                            downloaded_size = downloaded.get('files')[files.index(p)].get('downloaded')
                            debug(downloaded_size = downloaded_size)
        if not data_result:
            if result:
                data_result = json.loads(result.get())
                debug('remoteUpload', data_finish=str(data_result))

        return data_result

    def remoteUploadDownload(self, url, foldername = None, username = None, password = None, name = None, folderid = 0, progresshash = None, download_path = os.getcwd()):
        if not progresshash:
            progresshash = self.getHash()
        if foldername:
            folder = self.mkdir(foldername, username=username, password=password, folderid=folderid).get('folderid')
            datax = self.remoteUpload(url.strip(), None, username, password, folderid=folderid, progresshash=progresshash, renameit=name)
        else:
            datax = self.remoteUpload(url.strip(), None, username, password, folderid=folderid, progresshash=progresshash, renameit=name)
        debug(datax = datax)
        idx = datax.get('metadata')[0].get('id')
        debug(idx = idx)
        data, cookies = self.getDownloadLink(idx, download_path = download_path)
        debug(data = data)
        debug(cookies = cookies)
        download_path = os.path.abspath(download_path)
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        if not os.path.isdir(download_path):
            download_path = os.path.dirname(__file__)
        fileid = data.get('fileid')
        if name:
            self.renameFile(name, fileid, None, username, password)
        download_url = 'https://' + \
            data.get('hosts')[0] + data.get('path')
        if name:
            self.download(download_url, download_path, name, cookies)
        else:
            self.download(
                download_url, download_path, cookies=cookies)
            
    def getDownloadLink(self, fileide, auth=None, username=None, password=None, forcedownload=1, hashcache=None, download_path = "."):
        if download_path:
            download_path = os.path.abspath(download_path)
        fileide = fileide[1:]
        auth = self.getAuth(auth, username, password)
        debug('getDownloadLink', auth=auth)

        URL = self.setURL('getfilelink?auth={0}&fileid={1}&forcedownload={2}&hashcache={3}'.format(
            auth, fileide, forcedownload, hashcache))
        debug('getDownloadLink 1', URL=URL)
        data, cookies = self.getURL1(URL)
        data = json.loads(data)
        hashcache = data.get('hash')
        URL = self.setURL('getfilelink?auth={0}&fileid={1}&forcedownload={2}&hashcache={3}'.format(
            auth, fileide, forcedownload, hashcache))
        debug('getDownloadLink 2', URL=URL)
        data, cookies = self.getURL1(URL)
        data = json.loads(data)
        data.update({'Download Path': download_path,})
        for i in data:
            debug(i, data.get(i), size=10)
        return data, cookies

    def download(self, url, path=".", output=None, cookies=None, referer='https://my.pcloud.com/', postData = ''):
        if path == '.':
            path = os.getcwd()
        debug('download', url=url)
        debug('download', output=output)
        debug('download', referer=referer)
        debug('download', cookies=cookies)
        try:
            if sys.platform == 'win32':
                dm = idm.IDMan()
                debug('download', url=url)
                debug('download', output=output)
                debug('download', referer=referer)
                debug('download', cookies=cookies, debug = debug)
                dm.download(url, path, output, referer)
            else:
                wget.download(url, path)
        except:
            import traceback
            print traceback.format_exc()
            debug('download', use_download_manager='wget')
            wget.download(url, path)

    def download_aszip(self, folderids, auth = None, username = None, password = None, filename = None, debug = False):
        url = 'https://api.pcloud.com/getzip'
        if not filename:
            filename = datetime.datetime.strftime(datetime.datetime.now(), '%d%m%Y_%H%M%S') + str(random.randint(300, 400)) + ".zip"
        if not auth:
            auth = self.getAuth(auth, username, password)
        URL = url + '?auth={0}&folderids={1}&filename={2}'.format(auth, folderids, filename)
        self.download(URL, debug= debug)
        #return self.getURL1(url, rtype= 'post', data = data, stream= True, debug= True)
    def listFolderContentsList(self, contents, parent=None):
        '''
            contents.get('contents')
            contents is LIST
        '''

        this_root = ''
        for i in contents:
            if isinstance(i, dict):
                for b in i:
                    if b == 'folderid':
                        #this is root
                        for c in i:
                            if c == 'name':
                                self.tree.create_node(c, c, parent=parent)
                                this_root = c
                            elif c == 'path':
                                self.tree.create_node(c, c, parent=parent)
                                this_root = c
                            else:
                                self.tree.create_node(str(c.get('folderid')), str(
                                    c.get('folderid')), parent=parent)
                                this_root = str(c.get('folderid'))
                    elif b == 'contents':
                        if this_root:
                            self.listFolderContentsList(i.get(b), this_root)
                    elif b == 'fileid':
                        self.tree.create_node(
                            i.get('name'), i.get('name'), parent=parent)

    def register(self, email, password=None, os=4, invite=0, print_user_info=True):
        # print "print_user_info:", print_user_info
        URL = 'https://api.pcloud.com/register'
        if not email:
            email = raw_input('EMAIL: ')
        if not password:
            password = getpass.getpass('PASSWORD: ')
        #URL = 'https://api.pcloud.com/register?termsaccepted=yes&mail={0}&password={1}&os={2}&invite={3}'.format(email, password, os, invite)
        params = {
            'termsaccepted': 'yes',
            'mail': email,
            'password': password,
            'os': os,
            'invite': invite,
        }
        data, cookies = self.getURL1(URL, params)
        data = json.loads(data)
        if data.get('result') == 2038:
            print make_colors("REGISTERED", 'white', 'red')
            #userinfo = self.userInfo1(email, password, print_list=print_user_info)
            return False
        #debug(data=data, debug= True)
        auth = self.login(email, password, False).get('auth')
        userinfo = self.userInfo(auth, print_list=print_user_info)
        #userinfo = self.userInfo(
            #username=email, password=password, print_list=print_user_info)
        #userinfo = self.userInfo(auth, print_list=print_user_info)
        #debug(userinfo=userinfo, debug= True)
        #return userinfo
        return auth

    def getHash(self):
        # upload-9392343-xhr-816
        hash1 = 'upload-{0}-xhr'.format(random.randint(9390000, 9399999))
        hash2 = hash1 + '-{0}'.format(random.randint(500, 999))
        debug(hash2= str(hash2))
        return hash2

    def getDeleteID(self, idx=0):
        # upload-9392343-xhr-816
        id1 = '{0}-{1}'.format(random.randint(150, 190), idx)
        debug(id1=id1)
        return id1

    def delete(self, folderid=None, fileid=None, auth=None, username=None, password=None, name=None, idx=None):
        data = ''
        isFolder = False
        if folderid or fileid:
            contents = self.listFolder(auth, username=username, password=password).get(
                'metadata').get('contents')
            if not name:
                for i in contents:
                    if folderid:
                        if i.get('folderid') == int(folderid):
                            data = i
                    if fileid:
                        if i.get('fileid') == long(fileid):
                            data = i
                if data != '':
                    name = data.get('name')

        if idx:
            contents = self.listFolder(auth, username=username, password=password).get(
                'metadata').get('contents')
            for i in contents:
                if i.get('id') == idx:
                    data = i
            #deleteid = self.getDeleteID()

        if not data == '':
            if data.get('isfolder'):
                # https://api.pcloud.com/deletefolderrecursive?folderid=552455958&name=My+Music&id=187-0&auth=sKVtJXZhLWlZFFzSoIwoPAyQO3bs7JKWIuanRGWX
                auth, URL = self.AUTH(auth, username, password,
                                      'deletefolderrecursive')
                debug(URL = URL)
                params = {
                    'folderid': data.get('folderid'),
                    'id': self.getDeleteID(),
                    'name': data.get('name'),
                }
            else:
                auth, URL = self.AUTH(auth, username, password, 'deletefile')
                debug(URL = URL)
                params = {
                    'fileid': data.get('fileid'),
                    'id': self.getDeleteID(),
                    'name': data.get('name'),
                }

            contents, cookies = self.getURL1(URL, params)
            data = json.loads(contents)
            debug(data = data)
            return data

    def multi_delete(self, folderid=None, fileid=None, auth=None, username=None, password=None, name=None, idx=None):
        if folderid:
            for i in folderid:
                self.delete(i, auth=auth, username=username,
                            password=password, name=name, idx=idx)
        if fileid:
            for i in fileid:
                self.delete(fileid=i, auth=auth, username=username,
                            password=password, name=name, idx=idx)
        if idx:
            for i in idx:
                self.delete(auth=auth, username=username,
                            password=password, name=name, idx=i)

    def mkdir(self, name, auth=None, username=None, password=None, folderid='0'):
        #debug = True
        auth, URL = self.AUTH(auth, username, password, 'createfolder')
        debug(auth=auth, debug=debug)
        debug(URL=URL, debug=debug)
        # https://api.pcloud.com/createfolder?folderid=0&name=testx-3&auth=sKVtJXZhLWlZFFzSoIwoPAyQO3bs7JKWIuanRGWX
        params = {
            'auth': auth,
            'folderid': folderid,
            'name': name,
        }
        debug(params=params, debug=debug)
        contents, cookies = self.getURL1(URL, params, debug=debug)
        data = json.loads(contents)
        debug(data1=data, debug=debug)
        debug(data_get_result=data.get('result'), debug=debug)
        debug(type_data_get_result=type(
            data.get('result')), debug= debug)
        if data.get('result') == 5000:
            debug(process_001='', debug=debug)
            contents = self.listFolder(auth, folderid=folderid, username=username,
                                       password=password).get('metadata').get('contents')
            #data = json.loads(contents)
            for i in contents:
                if i.get('name') == name:
                    debug(i=i, debug=debug)
                    return i
        elif data.get('result') == 2400:
            debug(process_002='')
            contents = self.listFolder(auth, folderid=folderid, username=username,
                                       password=password).get('metadata').get('contents')
            #data = json.loads(contents)
            debug(contents = contents, debug = debug)
            for i in contents:
                if i.get('name') == name:
                    debug(i=i, debug=debug)
                    return i
        else:
            debug(process_003='', debug=debug)
            if data.get('result') == 2004 or data.get('result') == 5000:
                contents = self.listFolder(auth, folderid=folderid, username=username, password=password).get(
                    'metadata').get('contents')
                #data = json.loads(contents)
                for i in contents:
                    if i.get('name') == name:
                        debug(i=i, debug=debug)
                        return i

        debug(data2=data, debug=debug)
        return data.get('metadata')

    def setProxy(self, proxy_string, debug=False):
        proxy = {}
        if isinstance(proxy_string, list):
            pass
        else:
            print "[ERROR] Format Proxy !"
        proxy_string = str(proxy_string).strip()
        return json.loads(proxy_string)

    def usage(self):
        try:
                
            import argparse
            parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter)
            parser.add_argument('-l', '--login', help='Login', action='store_true')
            parser.add_argument('-U', '--username',
                                help='Username Authentication', action='store')
            parser.add_argument('-P', '--password',
                                help='Password Authentication', action='store')
            parser.add_argument(
                '-A', '--auth', help='Authentication Code', action='store')
            parser.add_argument(
                '-cp', '--change-password', help='Change Password, format: oldpassword newpassword, or just enter pass with prompt', action='store', nargs=2)
            parser.add_argument('-F', '--list-folder',
                                help='List Folder, default root folder', action='store_true')
            parser.add_argument('-Fi', '--folder-info',
                                help='Get Info of Parent Folder, default root folder', action='store_true')
            parser.add_argument('-L', '--list-content',
                                help='List File or Directory', action='store_true')
            parser.add_argument(
                '-s', '--sort', help='Sort List File or Directory', action='store', default='name')
            parser.add_argument(
                '-re', '--reverse', help='Sort List File or Directory Reverse', action='count', default='desc')
            parser.add_argument(
                '-f', '--list-file', help='List Files with given folder name or folder index, default folder index = 0', default='0', action='store_true')
            parser.add_argument('-T', '--list-token',
                                help='List Token', action='store_true')
            parser.add_argument('-i', '--user-info',
                                help='User Info', action='store_true')
            parser.add_argument('-x', '--set-auth-expire',
                                help='Set Authentication Expired in Seconds', action='store', default='63072000')
            parser.add_argument('-X', '--proxy',
                                help='Set Proxy, format example http://127.0.0.1:8118 https://127.0.0.1:3128', action='store', nargs = '*')
            parser.add_argument('-I', '--input-method', help = 'Change input method by insert a word then enter (default) or "msvcrt" = just input a word', action = 'store')
            parser.add_argument('-S', '--save-config', help = 'Save config (authentication) ', action = 'store_true')
            parser.add_argument(
                '-t', '--func', help='Test usage', action='store_true')
            parser.add_argument(
                '-a', '--argv', help='parameter/argument function', action='store', nargs='*')
            parser.add_argument('-d', '--download', help='Download',
                                action='store_true')
            parser.add_argument('-p', '--download-path', help='Download Path save to',
                                action='store', default=os.path.abspath(os.getcwd()))
            parser.add_argument('-g', '--get-currentserver',
                                help='Get Current Server', action='store_true')
            parser.add_argument('-r', '--remote-uploads',
                                help='Remote Upload url', action='store')
            parser.add_argument('-rr', '--clear-remote-uploads',
                                help='Clear Screen & Remote Upload url', action='store')
            parser.add_argument('-rd', '--remote-uploads-download',
                                help='Remote Upload url then download it', action='store')
            parser.add_argument('-n', '--download-name',
                                help='Rename after downloaded', action='store')
            parser.add_argument('-nn', '--download-number',
                                help='Direct download to number of list', action='store', nargs = '*')
            parser.add_argument('-N', '--list-number',
                                help='Numbers of list perline', action='store', type=int, default=2)
            parser.add_argument(
                '-u', '--uploads', help='Upload files', action='store', nargs='*')
            parser.add_argument('-R', '--register',
                                help='Register/SingUp', action='store_true')
            parser.add_argument('-Ri', '--register-invite',
                                help='Register/SingUp Invite', action='store', default=0, type=str)
            parser.add_argument('-Ro', '--register-os',
                                help='Register/SingUp OS', action='store', default=4, type=str)
            #parser.add_argument('--hash', help = 'Upload/Progress Hash or File hash', action = 'store', default = 'upload-9392343-xhr-816')
            parser.add_argument('--hash', help='Upload/Progress Hash or File hash',
                                action='store', default=self.getHash())
            parser.add_argument('-cf', '--create-folder',
                                help='Create Folder', action='store')
            parser.add_argument(
                '-v', '--debug', help='Debug Verbosity', action='store_true')
            parser.add_argument('-fi', '--folder-id',
                                help='Folder ID', default=0, type=int)
            parser.add_argument('-fn', '--folder-name',
                                help='Folder Name', default=0, type=int)
            parser.add_argument('-pi', '--parent-id',
                                help='Parent ID', default=0, type=int)
            parser.add_argument(
                '-D', '--delete', help='Delete Action', action='store_true')
            parser.add_argument('-DF', '--delete-folderid',
                                help='Delete, parameter: folderid [list]', nargs='*', action='store')
            parser.add_argument('-Df', '--delete-fileid',
                                help='Delete, parameter: fileid  [list]', nargs='*', action='store')
            parser.add_argument(
                '-Di', '--delete-id', help='Delete, paramteer: id [list]', nargs='*', action='store')
            #parser.add_argument(
                #'--proxy', help='Use Proxy; format: [http|https|socks5]://[HOST|IP:PORT]', type=str, action='store', nargs='*')
        except:
            print traceback.format_exc()
            sys.exit(0)
        if len(sys.argv) == 1:
            # parser.print_help()
            args = parser.parse_args()
            self.getContents(download_path=args.download_path)
        else:
            args = parser.parse_args()
            if args.debug:
                os.environ.update({'DEBUG': 1,})
            # if args.change_password:
            # self.changePass(args.change_password[0], args.change_password[1],
            # username = args.username, args.password)
            PROXY = {}
            if args.proxy:
                for i in args.proxy:
                    #host, port = str(i).split(":")
                    scheme = urlparse.urlparse(i).scheme
                    PROXY.update({scheme: i,})
            if not self.proxy:
                self.proxy = PROXY
            if args.list_number:
                self.nlist = args.list_number
            # print "args.list_number =", args.list_number
            self.debug = args.debug
            # print "args.debug =", args.debug
            # print "self.debug =", self.debug
            if args.save_config:
                self.setAuth(self.auth)
            if args.delete:
                if args.delete_folderid:
                    self.multi_delete(args.delete_folderid,
                                      username=args.username, password=args.password)
                elif args.delete_fileid:
                    self.multi_delete(fileid=args.delete_fileid,
                                      username=args.username, password=args.password)
                elif args.delete_id:
                    self.multi_delete(username=args.username,
                                      password=args.password, idx=args.delete_id)
                else:
                    print "Please Insert FolderID or FileID or IDs !"
            if args.list_content:
                self.getContents(args.auth, recursive=args.reverse, username=args.username, password=args.password,
                                 download_path=args.download_path, output=args.download_name, folderid=args.folder_id, nlist=args.list_number, input_method= args.input_method)
            if args.create_folder:
                self.createFolder(args.create_folder, args.folder_id,
                                  args.auth, args.username, args.password)
            if args.register:
                self.register(args.username, args.password,
                              args.register_os, args.register_invite)
            if args.remote_uploads:
                if args.folder_name:
                    folder = self.mkdir(args.folder_name, username=args.username,
                                        password=args.password, folderid=args.parent_id).get('folderid')
                    self.remoteUpload(args.remote_uploads.strip(), args.auth, args.username, args.password,
                                      folderid=folder, progresshash=args.hash, renameit=args.download_name)
                else:
                    self.remoteUpload(args.remote_uploads.strip(), args.auth, args.username, args.password,
                                      folderid=args.folder_id, progresshash=args.hash, renameit=args.download_name)
            if args.clear_remote_uploads:
                os.system('cls')
                if args.folder_name:
                    folder = self.mkdir(args.folder_name, username=args.username,
                                        password=args.password, folderid=args.parent_id).get('folderid')
                    self.remoteUpload(args.remote_uploads.strip(), args.auth, args.username, args.password,
                                      folderid=folder, progresshash=args.hash, renameit=args.download_name)
                else:
                    self.remoteUpload(args.remote_uploads.strip(), args.auth, args.username, args.password,
                                      folderid=args.folder_id, progresshash=args.hash, renameit=args.download_name)
            if args.remote_uploads_download:
                if args.folder_name:
                    folder = self.mkdir(args.folder_name, username=args.username,
                                        password=args.password, folderid=args.parent_id).get('folderid')
                    datax = self.remoteUpload(args.remote_uploads_download.strip(), args.auth, args.username,
                                              args.password, folderid=folder, progresshash=args.hash, renameit=args.download_name)
                else:
                    datax = self.remoteUpload(args.remote_uploads_download.strip(), args.auth, args.username, args.password,
                                              folderid=args.folder_id, progresshash=args.hash, renameit=args.download_name)
                idx = datax.get('metadata')[0].get('id')
                data, cookies = self.getDownloadLink(idx, download_path = args.download_path)
                download_path = args.download_path
                download_path = os.path.abspath(download_path)
                if not os.path.isdir(download_path):
                    os.makedirs(download_path)
                if not os.path.isdir(download_path):
                    download_path = os.path.dirname(__file__)
                fileid = data.get('fileid')
                if args.download_name:
                    debug('usage', renamefile='')
                    self.renameFile(args.download_name, fileid,
                                    args.auth, args.username, args.password)
                download_url = 'https://' + \
                    data.get('hosts')[0] + data.get('path')
                if args.download_name:
                    self.download(download_url, args.download_path,
                                  args.download_name, cookies)
                else:
                    self.download(
                        download_url, args.download_path, cookies=cookies)
            if args.uploads:
                if args.folder_name:
                    folder = self.mkdir(args.folder_name, username=args.username,
                                        password=args.password, folderid=args.parent_id).get('folderid')
                #self.fileUpload(args.uploads, args.auth, args.username, args.password, progresshash = args.hash)
                    self.fileUploadStart(args.uploads, args.auth, args.username, args.password,
                                         folder, progresshash=args.hash, renameit=args.download_name)
                else:
                    self.fileUploadStart(args.uploads, args.auth, args.username, args.password,
                                         args.folder_id, progresshash=args.hash, renameit=args.download_name)
            if args.get_currentserver:
                self.getCurrentServer()
            if args.func:
                if args.argv:
                    pass
                methodToCall = getattr(self, str(args.func))
                print methodToCall()
            if args.list_token:
                print self.listToken()
            if args.user_info:
                auth = self.getAuth(username=args.username,
                                    password=args.password)
                debug(auth=auth, debug=args.debug)
                self.userInfo(auth, args.username, args.password)
                #each_len_keys = []
                # for i in data:
                # each_len_keys.append(len(i))
                # for i in data:
                # if i == 'usedquota':
                # print "Used Quota" + " " * (max(each_len_keys) - len(i)) + ": " + "{0} | {1}".format(self.convert_size(data.get(i)), self.h_convert_size(data.get(i)))
                # elif i == 'quota':
                # print "Quota" + " " * (max(each_len_keys) - len(i)) + " : " + "{0} | {1}".format(self.convert_size(data.get(i)), self.h_convert_size(data.get(i)))
                # elif i == 'publiclinkquota':
                # print "Public Link Quota" + " " * ((max(each_len_keys) - len(i)) - 1) + ": " + "{0} | {1}".format(self.convert_size(data.get(i)), self.h_convert_size(data.get(i)))
                # else:
                # print str(i).title() + " " * (max(each_len_keys) - len(i)) + " : " +
                # str((data.get(i)))
            if args.login:
                print "login ..."
                self.login(args.username, args.password)
            if args.set_auth_expire:
                self.AuthExpire(args.set_auth_expire)
            if args.list_folder:
                print "list folder ..."
                print self.listFolder()
            if args.folder_info:
                print "get folder info"
                self.folderInfo(args.auth, args.username, args.password)
            if args.download:
                if args.download_number:
                    for i in args.download_number:
                        list_name, list_sort, contents = self.getContents(args.auth, folderid= args.folder_id, password= args.password, username= args.username, download_path = args.download_path, output= args.download_name, quite = True)
                        info_by_name = self.build_dict(contents, key="name")
                        result = info_by_name[
                            list_sort.get(int(i)).get('name')]
                        # print "result ->", result
                        print "download", result.get('name'), '...'
                        data, cookies = self.getDownloadLink(result.get('id'), download_path = args.download_path)
                        download_url = 'https://' + \
                            data.get('hosts')[0] + data.get('path')
                        self.download(download_url, args.download_path, args.download_name, cookies)
                                        
                    

if __name__ == '__main__':
    c = pcloud()
    #print c.getContents(quite = True)
    c.usage()
    # print c.mkdir('Ninja Scroll - The Series (Sub)', debug= True)
    #c.delete(folderid= '552595880')
    # c.usage()
