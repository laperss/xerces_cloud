#!/usr/bin/env python3
import os, requests, shutil

server = 'http://129.192.68.50:5000'
testfile = "test.mkv"
outputfile = "output.avi"

# Download example video file if testfile does not exist
if not os.path.isfile(testfile):
    print("Downloading example video file")
    url = 'http://jell.yfish.us/media/jellyfish-3-mbps-hd-h264.mkv'
    response = requests.get(url, stream=True)
    with open(testfile, "wb") as handle:
        shutil.copyfileobj(response.raw, handle)

# Movie convertion
s = requests.session()
print("Upload file")
response = s.post(server, files={'file': open(testfile, 'rb')})
print(response)

print("Download converted file")
response = s.get(server + '/file', stream=True)
with open(outputfile, "wb") as handle:
    shutil.copyfileobj(response.raw, handle)
print(response)


