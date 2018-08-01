from pcloud import pcloud
import cmdw

class uploadtransfer(pcloud):
    def __init__(self):
        pcloud.__init__(self)
        
    def uploadtransfer(self, sendermail, receivermails):
        url = self.MASTER_URL + "uploadtransfer"
        login = self.login()
        print "login =", login
        auth = login.get('auth')
        print "auth  =", auth
        url = url + '?sendermail={0}&receivermails={1}'.format(sendermail, receivermails)
        print "upload transfer -> url:", url
        data = self.getURL1(url)
        return data
    
if __name__ == '__main__':
    p = uploadtransfer()
    sendermail = "todut001@gmail.com"
    receivermails = "cumulus13@gmail.com"
    print p.uploadtransfer(sendermail, receivermails)