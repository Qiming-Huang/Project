import requests
import re
from tqdm import tqdm
import time
import os
import argparse


class Downloader():
    def __init__(self, download_url, video_name):
        self.main_path = "https://cdn.605-zy.com/"
        self.download_url = download_url
        self.video_name = video_name
        self.speed = None
        self.status_code = None

    def get_all_ts(self):
        ts_download_url = []
        data = requests.get(self.download_url).text
        url = re.findall(r"ppvod/(.+?).m3u8", data)[0]
        url = f"ppvod/{url}.m3u8"
        ts_all_path = os.path.join(self.main_path, url)

        ts_data = requests.get(ts_all_path).text
        with open("video/ts.txt", "w") as fr:
            fr.write(ts_data)

        with open("video/ts.txt", "r") as fr:
            content = fr.readlines()

        for i in content:
            if i[:-1].endswith(".ts"):
                ts_download_url.append(self.main_path[:-1] + i[:-1])

        return ts_download_url

    def compose(self):
        print("Start composing..")
        os.system(f"ffmpeg -f concat -i video/file.txt -c copy video/{self.video_name}")
        os.system("rm -rf video/*.ts video/file.txt")

    def MB(self, bype):
        return bype / 1024 / 1024

    def download_ts(self, url, index):
        res = requests.get(url, stream=True)
        self.status_code = res.status_code
        fr = open(f"video/{index}.ts", "wb")

        down_size = 0
        old_down_size = 0
        time_ = time.time()
        interval = 0.2

        for chunk in res.iter_content(chunk_size=512):
            if chunk:
                fr.write(chunk)
                down_size += len(chunk)
                if time.time() - time_ > interval:
                    speed = (down_size - old_down_size) / interval

                    old_down_size = down_size
                    time_ = time.time()
                    self.speed = self.MB(speed)
        with open(f"video/file.txt", "a") as f:
            f.write(f"file '{index}.ts'\n")

        fr.close()

    def download(self):
        ts_download_url = self.get_all_ts()
        loop = tqdm(enumerate(ts_download_url), total=len(ts_download_url))
        for idx, url in loop:
            finished = False
            loop.set_description(f"Total {idx}/{len(ts_download_url)}")
            while (not finished):
                self.download_ts(ts_download_url[idx], idx)
                loop.set_postfix(speed=f"{self.speed} MB/s")
                if self.status_code == 200:
                    loop.update(1)
                    finished = True
                else:
                    print(f"Download {idx}.ts error, retry..")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'Download video from .3m8u url'
    parser.add_argument("-u", "--url", help="url of .3m8u", dest="url", type=str, default="0")
    parser.add_argument("-n", "--name", help="save video name", dest="name", type=str, default="0")
    args = parser.parse_args()

    if args.url != 0 and args.name != 0:
        downloader = Downloader(args.url, args.name)
        downloader.download()
        downloader.compose()
