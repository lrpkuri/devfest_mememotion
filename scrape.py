import requests
import urllib
from bs4 import BeautifulSoup
from pymongo import MongoClient

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
		db.memes.insert_one( {
			"_id": memeUrl
			}
		)