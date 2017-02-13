#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, urllib2, json
import pandas as pd

client_id = 'UUS_VAWyY5FwHdKOYsVQ'
client_secret = 'JqLh86Ttd6'
qeury_args = {'query' : '서울 마포구 노고산동 31-11',
			  'encoding' : 'utf-8', 'coord':'latlng', 
			  'output':'json'}

filename = 'seoul_subway_station_address/subway_stations_1_4.csv'
df1 = pd.read_csv(filename)
df1 = df1[['line','station','address']]

filename = 'seoul_subway_station_address/subway_stations_5_8.csv'
df2 = pd.read_csv(filename)
df2 = df2[['line','station','address']]

df = df1.append(df2)

info = []
fail_items = []
for index, row in df.iterrows():
	line, station, address = row['line'], row['station'], row['address']
	try:
		qeury_args['query'] = address
		if address.startswith("경기"):
			continue
		url = 'https://openapi.naver.com/v1/map/geocode?' + urllib.urlencode(qeury_args)
		req = urllib2.Request(url)
		req.add_header("X-Naver-Client-Id",client_id)
		req.add_header("X-Naver-Client-Secret",client_secret)
		resp = urllib2.urlopen(req)
		content = resp.read()
		dic = json.loads(content)
		name = station
		lat = dic['result']['items'][0]['point']['y']
		lon = dic['result']['items'][0]['point']['x']
		item = {"name":name, "lat":lat, "lon":lon, "no_line":line }
		info.append(item)
	except Exception, e:
		print station
		item = {"name":station, "line":line, "address": "", "no_line":line}
		fail_items.append(item)

df = pd.DataFrame(info)
df.to_csv('station_latlen.csv', encoding='utf8', index=False)

df = pd.DataFrame(fail_items)
df.to_csv('fail_list.csv', encoding='utf8', index=False)