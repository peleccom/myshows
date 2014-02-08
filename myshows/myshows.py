import hashlib
import urllib
import urllib2
import urlparse


class MyShowsException(Exception):
    pass
class EmptyParametersException(MyShowsException):
    pass
class IncorrectLoginParametersException(MyShowsException):
    pass

class MyShows(object):
    API_HOST = "http://api.myshows.ru/"

    def __init__(self, login, password=None, password_md5=None):
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
        self.login()

    def login(self):
        URL = "profile/login"
        url = urlparse.urljoin(self.API_HOST, URL)
        data = {
            'login': self._login,
            'password': self._password_md5
        }
        enc_data = urllib.urlencode(data)
        url += "?" + enc_data
        r = urllib.urlopen(url)
        code = r.getcode()
        if code != 200:
            if code == 403:
                raise IncorrectLoginParametersException()
            elif code == 404:
                raise EmptyParametersException()
            else:
                raise MyShowsException("Incorrect return code")


def main():
    myShows = MyShows("demo", "demo")

if __name__ == "__main__":
    main()

