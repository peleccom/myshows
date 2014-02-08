import urllib
import urllib2
import urlparse
import json
from . import login
from . import constants
from . import exceptions

class MyShows(object):
    def __init__(self, login_object):
        self._login_obj = login_object
        self._opener = login_object.get_opener()
        self.login()

    def login(self):
        if not self._login_obj:
            raise exeptions.MyShowsLoginException("Login object is empty")
        return self._login_obj.login()


    def profile(self):
        url = urlparse.urljoin(constants.API_HOST, constants.PROFILE_PATH)
        print url
        r = self._opener.open(url)
        code = r.getcode()
        if code != 200:
            if code == 401:
                raise exceptions.MyShowsLoginRequired()
            else:
                raise exceptions.MyShowsException("Incorrect return code %d" % code)
	return r.read()
        
    def shows(self):
        url = urlparse.urljoin(constants.API_HOST, constants.SHOWS_PATH)
        print url
        r = self._opener.open(url)
        code = r.getcode()
        if code != 200:
            if code == 401:
                raise exceptions.MyShowsLoginRequired()
            else:
                raise exceptions.MyShowsException("Incorrect return code %d" % code)
        return r.read()






