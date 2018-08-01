#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LICFACE --<licface@yahoo.com>
  Purpose: PCloud Remote Upload
  Created: 4/23/2018
"""

import os
import sys
import requests
from debug import *

class RemoteUpload(object):
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.URL = ''
        
    def getCurrentServer(self, headers=None):
        url_param = 'currentserver'
        a = json.loads(self.getURL1('https://api.pcloud.com/' + url_param)[0])
        debug(a=str(a))
        return a
    
    def mkdir(self, name, folderid='0', auth=None, username=None, password=None):
        #debug = True
        auth, URL = self.AUTH(auth, username, password, 'createfolder')
        self.printlist(auth=auth, debug=debug)
        self.printlist(URL=URL, debug=debug)
        # https://api.pcloud.com/createfolder?folderid=0&name=testx-3&auth=sKVtJXZhLWlZFFzSoIwoPAyQO3bs7JKWIuanRGWX
        params = {
            'auth': auth,
            'folderid': folderid,
            'name': name,
        }
        self.printlist(params=params, debug=debug)
        contents, cookies = self.getURL1(URL, params, debug=debug)
        data = json.loads(contents)
        self.printlist(data1=data, debug=debug)
        self.printlist(data_get_result=data.get('result'), debug=debug)
        self.printlist(type_data_get_result=type(
            data.get('result')), debug= debug)
        if data.get('result') == 5000:
            self.printlist(process_001='', debug=debug)
            contents = self.listFolder(auth, folderid=folderid, username=username,
                                       password=password).get('metadata').get('contents')
            #data = json.loads(contents)
            for i in contents:
                if i.get('name') == name:
                    self.printlist(i=i, debug=debug)
                    return i
        elif data.get('result') == 2400:
            self.printlist(process_002='', debug=True)
            contents = self.listFolder(auth, folderid=folderid, username=username,
                                       password=password).get('metadata').get('contents')
            #data = json.loads(contents)
            self.printlist(contents = contents, debug = debug)
            for i in contents:
                if i.get('name') == name:
                    self.printlist(i=i, debug=debug)
                    return i
        else:
            self.printlist(process_003='', debug=debug)
            if data.get('result') == 2004 or data.get('result') == 5000:
                contents = self.listFolder(auth, folderid=folderid, username=username, password=password).get(
                    'metadata').get('contents')
                #data = json.loads(contents)
                for i in contents:
                    if i.get('name') == name:
                        self.printlist(i=i, debug=debug)
                        return i    
    
    def remoteUpload(self, url, folderid=0, nopartial=1, progresshash='upload-9392343-xhr-816', auth=None, username=None, password=None, renameit=None, foldername=None):
        data = {}   
        if foldername:
            mkfolder = self.mkdir(foldername, auth, username,
                                  password, folderid, debug=debug)

            self.printlist(mkfolder=mkfolder, debug=debug)
            folderid = mkfolder.get('folderid')
            self.printlist(folderid=folderid, debug=debug)

        self.printlist('remoteUpload', progresshash=progresshash, debug=debug)
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
        self.printlist('remoteUpload', URL=URL, debug=debug)
        params = {
            'auth': self.getAuth(auth, username, password),
            'folderid': folderid,
            'nopartial': nopartial,
            'progresshash': progresshash,
            'url': url,
        }

        self.printlist('remoteUpload', params=params, debug=debug)
        result = pool.apply_async(self.getURL2, (URL, params, 'post'))
        #self.printlist('remoteUpload', result_get = result.get())

        auth, downloaded = self.uploadprogress(
            auth, username, password, progresshash)
        
        self.printlist('remoteUpload', downloaded=downloaded, debug = debug)
        while 1:
            try:
                if downloaded.get('files')[0].get('status') == 'error':
                    self.printlist(
                        'remoteUpload', downloaded='ERROR', ERROR=downloaded)
                    print "DOWNLOAD ERROR [main] !"
                    sys.exit(0)
    
            except:
                if os.getenv('DEBUG'):
                    traceback.format_exc()
                if json.loads(result.get()).get('result') == 2008:
                    print termcolor.colored("OVER QUOTA !", 'white', 'on_red', attrs= ['blink'])
                    self.userInfo()
                    sys.exit(0)
                else:
                    if downloaded.get('result') == 1900:
                        print make_colors("DOWNLOAD ERROR [1900-1] !", 'white', 'red', ['bold', 'blink']) + make_colors(downloaded.get('error'), 'white', 'blue')
                        sys.exit(0)
            if downloaded.get('result') == 1900:
                print make_colors("DOWNLOAD ERROR [1900-2] !", 'white', 'red', ['bold', 'blink']) + make_colors(downloaded.get('error'), 'white', 'blue')
                sys.exit(0)
            #print "downloaded 0 =",downloaded
            debugger.debug(download_0 = downloaded)
            debugger.debug(type_download_0 = type(downloaded))
            if downloaded.has_key('files'):
                sizes = downloaded.get('files').get('size')
            else:
                pass
            #print "type(download) 0 =", type(downloaded)
            files = downloaded.get('files')
            if isinstance(downloaded, dict):
                for p in files:                
                    #downloaded_size = downloaded.get('files')[0].get('downloaded')
                    downloaded_size = p.get('downloaded')
                    #print "downloaded 1 =",downloaded
                    debugger.debug(downloaded_1 = downloaded)
                    auth, size = self.uploadprogress(
                        auth, username, password, progresshash)
                    #size = size.get('files')[0].get('size')
                    #size = size.get('files').get('size')
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
                    #while 1:
                        #if downloaded == '' or downloaded == None:
                            #auth, downloaded = self.uploadprogress(
                                #auth, username, password, progresshash)
                            # #downloaded = downloaded.get('files')[0].get('downloaded')
                            #downloaded_size = p.get('downloaded')
                            # #print "download 1 =", downloaded, "[%s]" % (str(os.getpid()))
                            #auth, size = self.uploadprogress(
                                #auth, username, password, progresshash)
                            # #size = size.get('files')[0].get('size')
                            #size = p.get('size')
                            # #print "size 1 =", size
                            #sys.exit(0)
                        #else:
                            #pbar = ProgressBar(widgets=widgets, max_value=size)
                            #pbar.start()
                            #break
                    while 1:
                        if debugger.DEBUG:
                            print "size     =", size
                            print "download =", downloaded            
                        #if isinstance(downloaded, dict):
                            #if downloaded.get('finished') == True:
                        if p.get('finished') == True:
                            pbar.finish()
                            break
                        elif p.get('finished') == False:
                            debug(ERROR = 'Download Interupted by SYSTEM and still download in background by SYSTEM !')
                            print make_colors('Download Interupted by SYSTEM and still download in background by SYSTEM !', 'white', 'red')
                            #auth, downloaded = self.uploadprogress(auth, username, password, progresshash)    
                            #pbar.update(downloaded.get('downloaded'))
                            sys.exit('Download Interupted by SYSTEM and still download in background by SYSTEM !')
                            #return self.remoteUpload(url, auth, username, password, folderid, nopartial, progresshash, renameit, foldername, debug)
                        else:
                            if size == downloaded_size:
                                pbar.finish()
                                break
                            else:
                                pbar.update(downloaded)
                                auth, downloaded = self.uploadprogress(auth, username, password, progresshash)    
        if result:
            data = json.loads(result.get())
            self.printlist('remoteUpload', data_finish=str(data), debug=True)
            if data.get('metadata'):
                if renameit:
                    fileid = data.get('metadata')[0].get('fileid')
                    self.renameFile(renameit, fileid, auth, username, password)
            else:
                print make_colors("Can't Rename it [ERROR]: ", 'white', 'red', ['blink']) + make_colors('METADATA = ', 'white', 'blue') + make_colors(str(data.get('metadata')), 'magenta', 'yellow')
        return data

    def remoteUploadDownload(self, url, foldername = None, username = None, password = None, name = None, folderid = 0, progresshash = None, download_path = os.getcwd()):
        if not progresshash:
            progresshash = self.getHash()
        if foldername:
            folder = self.mkdir(foldername, username=username, password=password, folderid=folderid).get('folderid')
            datax = self.remoteUpload(url.strip(), None, username, password, folderid=folderid, progresshash=progresshash, renameit=name)
        else:
            datax = self.remoteUpload(url.strip(), None, username, password, folderid=folderid, progresshash=progresshash, renameit=name)
        idx = datax.get('metadata')[0].get('id')
        data, cookies = self.getDownloadLink(idx, download_path = download_path)
        download_path = args.download_path
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