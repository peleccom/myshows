# -*- coding: utf-8 -*-
import logging
import os
import unittest
import sys
sys.path.insert(0, os.path.abspath('..'))
from myshows import exceptions
from myshows.classes import ShortSeries
from myshows import MyShows

LOGIN = "demo239"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class APITest(unittest.TestCase):

    def setUp(self):
        self.myShows = MyShows()
        self.myShows.login(LOGIN, LOGIN)

    def test_shows(self):
        series_list = self.myShows.shows()
        self.assertIsInstance(series_list[0], ShortSeries)

    def testSearch(self):
        self.myShows.search("theory")

    def test_my_profile(self):
        self.myShows.profile()

    def test_user_profile(self):
        with self.assertRaises(exceptions.MyShowsNotFoundException):
            self.myShows.profile("incorrect_user")
        res1 = self.myShows.profile(LOGIN)
        res2 = self.myShows.profile()
        self.assertEqual(res1, res2)

class LoginTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_correct_login(self):
        ms = MyShows()
        ms.login("demo239", "demo239")

    def test_incorrect_login(self):
        ms = MyShows()
        with self.assertRaises(exceptions.MyShowsLoginIncorrectException):
            ms.login("d", "d")
        with self.assertRaises(exceptions.MyShowsNotFoundException):
            ms.login("", "")

    def test_unathorized_call(self):
        ms = MyShows()
        with self.assertRaises(exceptions.MyShowsLoginRequiredException):
            ms.profile()

if __name__ == '__main__':
    unittest.main()