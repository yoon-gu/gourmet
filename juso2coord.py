#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, urllib2, json, csv
import pandas as pd
from pprint import pprint

client_id = 'UUS_VAWyY5FwHdKOYsVQ'
client_secret = 'JqLh86Ttd6'
qeury_args = {'query' : '서울 마포구 노고산동 31-11',
			  'encoding' : 'utf-8', 'coord':'latlng', 
			  'output':'json'}

info = []
df = pd.read_csv('database.csv')
for index, row in df.iterrows():
	qeury_args['query'] = row['주소']
	url = 'https://openapi.naver.com/v1/map/geocode?' + urllib.urlencode(qeury_args)
	req = urllib2.Request(url)
	req.add_header("X-Naver-Client-Id",client_id)
	req.add_header("X-Naver-Client-Secret",client_secret)
	resp = urllib2.urlopen(req)
	content = resp.read()
	dic = json.loads(content)
	name = row['상호명']
	lat = dic['result']['items'][0]['point']['y']
	lon = dic['result']['items'][0]['point']['x']
	item = {"name" : name, "lat" : lat, "lon" : lon, "type" : row['업종'] }
	info.append(item)

pprint(info)
pd.DataFrame(info).to_csv('data.csv', encoding='utf8', index=False)