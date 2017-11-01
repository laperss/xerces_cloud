#!/usr/bin/env python3
import os, requests, shutil, time, random, string
from threading import Thread

server = 'http://129.192.68.34:5000'
testfile = "test.mkv"

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def download_file():
    # Download example video file if testfile does not exist
    if not os.path.isfile(testfile):
        print("Downloading example video file")
        url = 'http://jell.yfish.us/media/jellyfish-3-mbps-hd-h264.mkv'
        response = requests.get(url, stream=True)
        with open(testfile, "wb") as handle:
            shutil.copyfileobj(response.raw, handle)

def user(id):
    s = requests.session()
    print("[" + str(id) + "]" + "Upload file")
    response = s.post(server, files={'file': open(testfile, 'rb')})
    #print(response)

    print("[" + str(id) + "]" + "Download converted file")
    response = s.get(server + '/file', stream=True)
    #print(response)
    outputfile = "output_%s.avi" % random_string()
    with open(outputfile, "wb") as handle:
        shutil.copyfileobj(response.raw, handle)

    print("[" + str(id) + "]" + "Remove file")
    os.remove(outputfile)

if __name__ == "__main__":
    download_file()

    userid = 0
    while True:
        # Spawn thread
        userthread = Thread(target=user, args=(userid,))
        userthread.setDaemon(True)
        userthread.start()
        
        # Sleep for a random time
        time.sleep(random.randint(0, 25))
        userid += 1
