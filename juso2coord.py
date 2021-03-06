import urllib.request, json, csv
import pandas as pd
from pprint import pprint

client_id = 'UUS_VAWyY5FwHdKOYsVQ'
client_secret = 'JqLh86Ttd6'
qeury_args = {'query' : '서울 마포구 노고산동 31-11',
			  'encoding' : 'utf-8', 'coord':'latlng', 
			  'output':'json'}

info = []
df = pd.read_csv('requested_places.csv')
done_df = pd.read_csv('done_places.csv')
done_df_len = len(done_df)
for idx, row in df.iterrows():
	encText = urllib.parse.quote(row['주소'])
	url = "https://openapi.naver.com/v1/map/geocode?query=" + encText
	request = urllib.request.Request(url)
	request.add_header("X-Naver-Client-Id",client_id)
	request.add_header("X-Naver-Client-Secret",client_secret)
	response = urllib.request.urlopen(request)
	rescode = response.getcode()
	if(rescode is 200):
		response_body = response.read()
		content = response_body.decode('utf-8')
		dic = json.loads(content)
		name = row['상호명']
		lat = dic['result']['items'][0]['point']['y']
		lon = dic['result']['items'][0]['point']['x']
		item = {"name" : name, "lat" : lat, "lon" : lon, "type" : row['업종'] }
		info.append(item)
		done_df.loc[done_df_len + idx] = df.loc[idx]
		df = df.drop(df.index[[0]])
	else:
		print("Error Code:" + rescode)
pprint(info)
old = pd.read_csv('data.csv')
new = pd.DataFrame(info)
old.append(new).to_csv('data.csv', encoding='utf8', index=False)
df.to_csv('requested_places.csv', encoding='utf8', index=False)
done_df.to_csv('done_places.csv', encoding='utf8', index=False)