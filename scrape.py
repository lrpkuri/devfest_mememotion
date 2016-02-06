import requests
import urllib2
from urllib2 import Request
from urllib2 import HTTPError
from bs4 import BeautifulSoup
from pymongo import MongoClient
import httplib, urlparse, base64, json

url = 'https://www.google.com/search?q=meme&safe=off&biw=1279&bih=617&source=lnms&tbm=isch&sa=X&'
response = requests.get(url)

html = response.content
soup = BeautifulSoup(html, "html.parser")

images = soup.find('table', attrs={'class': 'images_table'})

memes = images.findAll('td')
client = MongoClient('dyn-160-39-150-144.dyn.columbia.edu', 27000)
db = client['memes']
for row in memes:
	if row.find('a') is not None:
		memeUrl = row.find('img').get('src')
		headers = {
		# Request headers
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': '2750c64f4fcd4c398aac157a5d77c675',
		}

		body = {
		'url': memeUrl,
		}

		try:
			conn = httplib.HTTPSConnection('api.projectoxford.ai')
			conn.request("POST", "/emotion/v1.0/recognize", json.dumps(body), headers)
			resp = conn.getresponse()
			if resp.status == 200:
				data = resp.read().decode('utf-8')
				if len(data) > 2:
				 	j_data = json.loads(data)
				 	scores = j_data[0]['scores']
				 	db.memes.update_one(
				 		{"_id": memeUrl},
				 		{
				 		"$set": {
				 			"scores": scores
				 		}
				 	})
				 	db.memes.insert_one( {
				 		"_id": memeUrl,
				 		"scores": scores
				 		})
			conn.close()
		except Exception as e:
			print(e.message)