from pcloud import pcloud
import cmdw

class UploadLink(pcloud):
    def __init__(self):
        pcloud.__init__(self)
    
    def list_uploadlink(self):
        url = self.MASTER_URL + "listuploadlinks"
        login = self.login()
        print "login =", login
        auth = login.get('auth')
        print "auth  =", auth
        url = url + '?auth={0}'.format(auth)
        print "list_uploadlink -> url:", url
        data = self.getURL1(url)
        return data

    def create_uploadlink(self, folderid = 0, path = '/', comment = 'test 1', expire = '', maxspace = 0, maxfiles = 0):
        url = self.MASTER_URL + "createuploadlink"
        login = self.login()
        print "login =", login
        auth = login.get('auth')
        print "auth  =", auth
        url = url + '?auth={0}&folderid={1}&path={2}&comment={3}&maxspace={4}&maxfiles={5}'.format(auth, folderid, path, comment, maxspace, maxfiles)
        print "create uploadlink -> url:", url
        data = self.getURL1(url)
        return data    
        
if __name__ == '__main__':
    c = UploadLink()
    print c.create_uploadlink()
    print "-" * cmdw.getWidth()
    print c.list_uploadlink()
    