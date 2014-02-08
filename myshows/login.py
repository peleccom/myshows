import urllib
import urllib2
import hashlib
import urlparse
from cookielib import CookieJar
from . import exceptions
from . import constants


class MyShowsLogin(object):
    """Login with username and password"""

    def __init__(self, login, password=None, password_md5=None):
	cj = CookieJar()
	self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	if not login:
            raise ValueError("Empty user login")
        self._login = login
        if password and password_md5:
            raise ValueError("Use password OR password_md5")
        if (not password) and (not password_md5):
            raise ValueError("Password value empty")
        if password:
            self._password_md5 = hashlib.md5(password).hexdigest()
        if password_md5:
            self._password_md5 = password_md5

    def login(self):
        url = urlparse.urljoin(constants.API_HOST, constants.LOGIN_PATH)
        data = {
            'login': self._login,
            'password': self._password_md5
        }
        enc_data = urllib.urlencode(data)
        url += "?" + enc_data
        r = self._opener.open(url)
        code = r.getcode()
        if code != 200:
            if code == 403:
                raise exceptions.MyShowsLoginIncorrectException()
            elif code == 404:
                raise exceptions.MyShowsLoginEmptyException
            else:
                raise exceptions.MyShowsException("Incorrect return code %s" % code)
        print r.read()
        return True
        
    def get_opener(self):
      return self._opener


class MyShowsVKLogin(MyShowsLogin):
    def __init__(self, token, userid):
      
        if (not userid) and (not token):
            raise ValueError("Empy paramters")
        self._token = token
        self._userid = userid

    def login(self):
        url = urlparse.urljoin(constants.API_HOST, constants.VK_LOGIN_PATH)
        data = {
            'userid': self._userid,
            'token': self._token
        }
        enc_data = urllib.urlencode(data)
        url += "?" + enc_data
        r = urllib.urlopen(url)
        code = r.getcode()
        if code != 200:
            if code == 403:
                raise exceptions.MyShowsLoginIncorrectException()
            elif code == 404:
                raise exceptions.MyShowsLoginEmptyException
            else:
                raise exceptions.MyShowsException("Incorrect return code")
        return True