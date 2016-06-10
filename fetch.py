#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import textwrap
import AppStoreReview

class AppReview(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def fetch(self):
        if (len(sys.argv) == 2):
            app_id = sys.argv[1]
            pages = 100
            self.fetch_reviews(app_id, pages)
        else:
            print textwrap.dedent("""
            [例. AppStore]
            %python Fetch.py 409807569""")
            quit()

    def fetch_reviews(self, app_id, pages):
        if (self.is_app_store_app(app_id)):
            task = AppStoreReview.AppStoreReview()
        task.fetch_reviews(app_id, pages)

    def is_app_store_app(self, id):
        return re.compile('^\d+$').search(id)

if __name__ == "__main__":
	task = AppReview()
	task.fetch()



