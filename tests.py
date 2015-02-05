# -*- coding: utf-8 -*-
import unittest

from myshows import login
from myshows import myshows
from myshows import exceptions

from datetime import datetime


class APITest(unittest.TestCase):

    def setUp(self):
        myShows_login = login.MyShowsLogin("demo", "demo")
        self.myShows = myshows.MyShows(myShows_login)
    def testMyShows(self):
        print self.myShows.shows()
        
    def testSearch(self):
        print self.myShows.search("theory")

if __name__ == '__main__':
    unittest.main()