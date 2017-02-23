import urllib.request, json, csv, re
import pandas as pd
from pprint import pprint

client_id = 'UUS_VAWyY5FwHdKOYsVQ'
client_secret = 'JqLh86Ttd6'
qeury_args = {'query' : '서울 마포구 노고산동 31-11',
			  'encoding' : 'utf-8', 'coord':'latlng', 
			  'output':'json'}

import xml.etree.ElementTree
tree = xml.etree.ElementTree.parse('vincent_legacy.kml')
root = tree.getroot()

info = []
for place in tree.findall('.//Placemark'):
	name = place.find('name').text
	coord = place.find('Point/coordinates').text

	# Name Parsing
	if "☆" in name: # He visited this place
		place_type = re.search(r'\((.*?)\)',name).group(1).replace('아샨', '아시안')
		name = name[4:]
		stars = name[0:3].strip()

		encText = urllib.parse.quote(coord)
		url = "https://openapi.naver.com/v1/map/reversegeocode?query=" + encText
		request = urllib.request.Request(url)
		request.add_header("X-Naver-Client-Id",client_id)
		request.add_header("X-Naver-Client-Secret",client_secret)
		response = urllib.request.urlopen(request)
		rescode = response.getcode()

		if(rescode is 200):
			response_body = response.read()
			content = response_body.decode('utf-8')
			dic = json.loads(content)
			for j in range(0, len(dic['result']['items'])):
				address = dic['result']['items'][j]['address']
			lon, lat, _ = coord.split(',')
			item = {"name" : name[3:].strip(), "lat" : lat, "lon" : lon, "type" : place_type }
			info.append(item)
			
			print(place_type, name[3:].strip(), address, coord, stars)
		else:
			print("Error!")

old = pd.read_csv('data.csv')
new = pd.DataFrame(info)
old.append(new).to_csv('data.csv', encoding='utf8', index=False)