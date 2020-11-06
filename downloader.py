#!python3
import argparse
import os
from concurrent.futures.thread import ThreadPoolExecutor

import requests
import threading
from time import sleep

TWITCH_URL = "https://clips-media-assets2.twitch.tv/"
TIMEOUT = 10*60*60 # 10 hours in seconds


def get_url(vod_id, offset):
    return f"{TWITCH_URL}{vod_id}-offset-{offset}.mp4"


def get_fname(vod_id, offset):
    return f"./clips/{vod_id}-offset-{offset}.mp4"


def dl_clip(url, file):
    r = requests.request("GET", url)
    if r.status_code == 200:
        print(f"found clip {file}")
        with open(file, "wb") as f:
            f.write(r.content)


def check_vod(vod_id, start_offset, end_offset):
    try:
        os.mkdir("./clips")
    except OSError:
        pass
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(start_offset,end_offset):
            executor.submit(dl_clip, get_url(vod_id, i), get_fname(vod_id, i))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sid", metavar="Stream_ID", type=int)
    parser.add_argument("s", metavar="Start_Offset", nargs="?", default=0, type=int)
    parser.add_argument("e", metavar="End_Offset", nargs="?", default=TIMEOUT, type=int)
    args = parser.parse_args()
    check_vod(args.sid, args.s, args.e)