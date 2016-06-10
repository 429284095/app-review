#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import requests
import re
from lxml import etree
import pre
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class AppStoreReview():
    __base = os.path.dirname(os.path.abspath(__file__))
    __reviewXML = os.path.normpath(os.path.join(__base, './tmp/app_review.xml'))
    __basehost = "http://ax.itunes.apple.com"
    __basePath = "/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id="
    __baseUrl = __basehost + __basePath
    __userAgent = ("iTunes/9.2 (Windows; Microsoft Windows 7 "
            "Home Premium Edition (Build 7600)) AppleWebKit/533.16")

    def __init__(self):
        pass

    def __del__(self):
        pass

    def get_reviews(self, doc, app_id, arfffile):
        ns = { "itms" : "http://www.apple.com/itms/"}
        root = etree.fromstring(doc)
        infotags = root.xpath('.//itms:TextView[@topInset="0"][@styleSet="basic13"][@squishiness="1"][@leftInset="0"][@truncation="right"][@textJust="left"][@maxLines="1"]', namespaces = ns)
        users = []
        versions = []
        dates = []
        for tag in infotags:
            if(etree.tostring(tag).find('by') != -1):
              tmplist = re.sub(' ', '', etree.tostring(tag, encoding='utf-8')).split('\n')
              for i, tmp in enumerate(tmplist):
                  if i == 0: #user byAnonymous
                      if(tmp.find('byAnonymous') > 0):
                          users.append('by Anonymous')
                          versions.append('')
                          dates.append('')
                  elif i == 4:
                      users.append(tmp)
                  elif i == 9: #version
                      m = re.compile('^Version([\d\.]+)').search(tmp)
                      if m:
                          versions.append(m.group(1))
                      else:
                          versions.append('')
                  elif i == 12: #date
                          dates.append(tmp)

        titles = []
        titletags = root.xpath('.//itms:TextView[@styleSet="basic13"][@textJust="left"][@maxLines="1"]', namespaces = ns)
        for tag in titletags:
            tmplist = tag.xpath('.//itms:b', namespaces = ns)
            for tmp in tmplist:
                titles.append(tmp.text.encode('utf_8'))
                #print tmp.text.encode('utf_8')

        stars = []
        startags = root.xpath('.//itms:HBoxView[@topInset="1"]', namespaces = ns)
        for tag in startags:
            m = re.compile('^(\d).+').search(tag.get('alt'))
            if m:
                stars.append(m.group(1))
            else:
                stars.append('')

        bodies = []
        bodytags = root.xpath('.//itms:TextView[@styleSet="normal11"]/itms:SetFontStyle', namespaces = ns)
        for tag in bodytags:
            bodies.append(tag.text.encode('utf_8'))
            #print tag.text.encode('utf_8')

        count = len(stars)
        for i in range(0, count):
                body = pre.root(bodies[i])
                length = len(body)
                line = "\'%s\',%s,\'%s\',%s,\'%s\',\'%s\'" % (str.strip(users[i]), stars[i], titles[i], length, body, dates[i])
                arfffile.writelines(line + '\n')
        return arfffile

    def fetch_reviews(self, app_id, pages):
        with open('./' + str(app_id) + '.arff', 'w') as fp:
            fp.write('''@relation ExceptionRelation

@attribute user string
@attribute star string
@attribute title string
@attribute length string
@attribute body string
@attribute date string

@data
''')
            for i in range(0, pages):
                try:
                    print "Processing :%s/%s...." % (i+1, pages)
                    url = self.__baseUrl\
                            + app_id\
                            + "&pageNumber="\
                            + str(i)\
                            + "&sortOrdering=4&type=Purple+Software"\

                    response = requests.get(url, headers={'User-Agent':self.__userAgent, 'X-Apple-Store-Front':'143441-1'})
                    if response.status_code == 200:
                        self.get_reviews(response.text.encode('utf_8'), app_id, fp)
                except:
                    pass


