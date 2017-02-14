#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, urllib2, json
import pandas as pd
from pprint import pprint

client_id = 'UUS_VAWyY5FwHdKOYsVQ'
client_secret = 'JqLh86Ttd6'
qeury_args = {'query' : '서울 마포구 노고산동 31-11',
			  'encoding' : 'utf-8', 'coord':'latlng', 
			  'output':'json'}

url = 'https://openapi.naver.com/v1/map/geocode?' + urllib.urlencode(qeury_args)
req = urllib2.Request(url)
req.add_header("X-Naver-Client-Id",client_id)
req.add_header("X-Naver-Client-Secret",client_secret)
resp = urllib2.urlopen(req)
content = resp.read()
dic = json.loads(content)
pprint(dic)