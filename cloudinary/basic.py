#!/usr/bin/env python
import os, sys
from pymongo import MongoClient
from urllib2 import Request
from urllib2 import HTTPError
import httplib, base64, json

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cloudinary.api import delete_resources_by_tag, resources_by_tag

# config
os.chdir(os.path.join(os.path.dirname(sys.argv[0]), '.'))
if os.path.exists('settings.py'):
    execfile('settings.py')

directory = os.listdir("screens/")
set_directory = set(directory)
print set_directory

TAG = "videos"

client = MongoClient('dyn-160-39-150-144.dyn.columbia.edu', 27000)
db = client['photos']

def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))

def upload_files():
    print("--- Upload a local file")
    # url_list = []
    for x in set_directory:
        if not x.startswith('.'):
            response = upload("screens/"+x, tags = TAG)
            dump_response(response)
            url, options = cloudinary_url(response['public_id'],
                format = response['format'],
            )
            print("video" + url)
            print("")
            # url_list.append(url)

            headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '2750c64f4fcd4c398aac157a5d77c675',
        }
        body = {
        'url': url,
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
                    db.photos.insert_one(
                        {"_id": url,
                        "scores": scores
                    })
            conn.close()
        except Exception as e:
            print(e.message)
        dat = db.photos.find()
        for i in dat:
            print i

    # print (url_list)
def cleanup():
    response = resources_by_tag(TAG)
    count = len(response.get('resources', []))
    if (count == 0):
        print("No images found")
        return
    print("Deleting %d images..." % (count,))
    delete_resources_by_tag(TAG)
    print("Done!")
    pass

if len(sys.argv) > 1:
    if sys.argv[1] == 'upload': upload_files()
    if sys.argv[1] == 'cleanup': cleanup()
else:
    print("--- Uploading files and then cleaning up")
    print("    you can only one instead by passing 'upload' or 'cleanup' as an argument")
    print("")
    upload_files()
