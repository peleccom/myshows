# -*- coding: UTF-8 -*-
import hashlib
import urllib
import urllib2
import urlparse
import json
from . import constants
from . import exceptions
from .classes import ShortSeries, Series
import requests

class MyShows(object):
    def __init__(self):
        self.session = requests.Session()

    def login(self,login,password):
        params = {
            'login': login,
            'password': hashlib.md5(password).hexdigest()
        }
        url = urlparse.urljoin(constants.API_HOST, constants.LOGIN_PATH)
        self.api_call(url, params, [403, 404], not_json=True)

    def login_vk(self,user_id, token):
        pass

    def login_fb(self,user_id, token):
        pass

    def login_tw(self, user_id, secret, token):
        pass

    def api_call(self, url, params, return_codes, not_json=False):
        try:
            r = self.session.get(url, params=params)
        except Exception, e:
            raise exceptions.MyShowsException(e.message)
        code = r.status_code
        if code != 200:
            if code not in return_codes:
                raise exceptions.MyShowsException("Incorrect return code %d" % code)
            else:
                if code == 401:
                    raise exceptions.MyShowsLoginRequiredException()
                if code == 403:
                    raise exceptions.MyShowsLoginIncorrectException()
                elif code == 404:
                    raise exceptions.MyShowsNotFoundException()
                elif code == 500:
                    raise exceptions.MyShowsInvalidParameter()

        if not_json:
            return r.text
        json_result = r.json()
        return json_result

    def profile(self, username=None):
        """
        User profile
        :param username:
        :return:
        """
        url = urlparse.urljoin(constants.API_HOST, constants.PROFILE_PATH)
        if username:
            url = urlparse.urljoin(url, username)
        return self.api_call(url, None, [401])
        
    def shows(self):
        """
        user shows
        :return: list of ShortSeries
        """
        url = urlparse.urljoin(constants.API_HOST, constants.SHOWS_PATH)
        shows_dict = self.api_call(url, None, [401])
        res = []
        for show_id in shows_dict.keys():
            # print shows_dict[show_id].keys()
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
            # print shows_dict[show_id].keys()
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
