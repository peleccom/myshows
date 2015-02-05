# -*- coding: UTF-8 -*-
#‡‡‡
import urllib
import urllib2
import urlparse
import json
from . import constants
from . import exceptions
from .classes import ShortSeries, Series

class MyShows(object):
    def __init__(self, login_object):
        self._login_obj = login_object
        self._opener = login_object.get_opener()
        self.login()

    def login(self):
        if not self._login_obj:
            raise exceptions.MyShowsLoginException("Login object is empty")
        return self._login_obj.login()

    def api_call(self, url, params, return_codes, not_json=False):
        if params:
            for k in params.keys():
                val = params[k]
                if isinstance(val, unicode):
                    params[k] = val.encode('utf8')
            enc_data = urllib.urlencode(params)
            url += "?" + enc_data
        print url
        try:
            r = self._opener.open(url)
        except urllib2.HTTPError, e:
            code = e.getcode()
            if code not in return_codes:
                raise exceptions.MyShowsException("Incorrect return code %d" % code)
            else:
                if code == 401:
                    raise exceptions.MyShowsLoginRequiredException()
                elif code == 404:
                    raise exceptions.MyShowsNotFoundException()
                elif code == 500:
                    raise exceptions.MyShowsInvalidParameter()
        s = r.read()
        if not_json:
            return s
        json_result = json.loads(s)
        return json_result

    def profile(self):
        url = urlparse.urljoin(constants.API_HOST, constants.PROFILE_PATH)
        return self.api_call(url, None, [401])
        
    def shows(self):
        url = urlparse.urljoin(constants.API_HOST, constants.SHOWS_PATH)
        shows_dict = self.api_call(url, None, [401])
        res = []
        for show_id in shows_dict.keys():
            print shows_dict[show_id].keys()
            res.append(ShortSeries(shows_dict[show_id]))
        return res


    def search_file(self, filename):
        url = urlparse.urljoin(constants.API_HOST, constants.SEARCH_EPISODE_PATH)
        data = {
            'q': filename
        }
        return self.api_call(url, data, [404, 500])

    def search(self, q):
        url = urlparse.urljoin(constants.API_HOST, constants.SEARCH_PATH)
        data = {
        'q': q
        }
        shows_dict = self.api_call(url, data, [404, 500])
        res = []
        for show_id in shows_dict.keys():
            print shows_dict[show_id].keys()
            res.append(Series(shows_dict[show_id]))
        return res

    def show_id(self, show_id):
        url = urlparse.urljoin(constants.API_HOST, constants.SHOW_ID_PATH)
        url += "%d" % show_id
        return self.api_call(url, None, [404])

    def genres(self):
        url = urlparse.urljoin(constants.API_HOST, constants.SHOW_ID_PATH)
        return self.api_call(url, None, None)

    def check_episode(self, episode_id):
        url = urlparse.urljoin(constants.API_HOST, constants.CHECK_PATH)
        url += "%d" % episode_id
        return self.api_call(url, None, [401], not_json=True)

    def unwatched(self):
        url = urlparse.urljoin(constants.API_HOST, constants.UNWATCHED_PATH)
        return self.api_call(url, None, [401])
