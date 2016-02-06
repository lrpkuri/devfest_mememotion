#!/usr/bin/env python
import os, sys

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

def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))

def upload_files():
    print("--- Upload a local file")
    url_list = []
    for x in set_directory:
        if not x.startswith('.'):
            response = upload("screens/"+x, tags = TAG)
            dump_response(response)
            url, options = cloudinary_url(response['public_id'],
                format = response['format'],
            )
            print("video" + url)
            print("")
            url_list.append(url)
    print ("ve",url_list)
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
