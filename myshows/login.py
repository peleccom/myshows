import urllib
import urllib2
import hashlib
import urlparse
from cookielib import CookieJar
from . import exceptions
from . import constants


class MyShowsBaseLogin(object):
    def __init__(self):
        cj = CookieJar()
        self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        self._credentials = {}
        self._login_path = ''

    def get_opener(self):
        return self._opener

    def login(self):
        url = urlparse.urljoin(constants.API_HOST, self._login_path)
        enc_data = urllib.urlencode(self._credentials)
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
        return True


class MyShowsLogin(MyShowsBaseLogin):
    """Login with username and password"""
    def __init__(self, login, password=None, password_md5=None):
        super(MyShowsLogin, self).__init__()
        self._login_path = constants.LOGIN_PATH
        if not login:
            raise ValueError("Empty user login")
        self._credentials['login'] = login
        if password and password_md5:
            raise ValueError("Use password OR password_md5")
        if (not password) and (not password_md5):
            raise ValueError("Password value empty")
        if password:
            self._credentials['password'] =  hashlib.md5(password).hexdigest()
        if password_md5:
            self._credentials['password'] = password_md5


class MyShowsSocialLogin(MyShowsBaseLogin):
    """Login with social networks"""
    SOCIALS = ['vk', 'fb', 'tw']
    def __init__(self, social, **kwargs):
        """
        http://api.myshows.ru/profile/login/vk?token=<token>&userId=<userId>
        http://api.myshows.ru/profile/login/fb?token=<token>&userId=<userId>
        http://api.myshows.ru/profile/login/tw?token=<token>&userId=<userId>&userId=<secret>
        """
        super(MyShowsSocialLogin, self).__init__()

        if social not in self.SOCIALS:
            raise ValueError("Invalid social parameter. Must be in %s" % self.SOCIALS)
        self._login_path = constants.LOGIN_PATH + "/%s" % social
        for item in kwargs.items():
            if not item[1]:
                raise ValueError("Empty %s login parameter" % item[0])
        self._credentials.update(kwargs)