import requests
import re
import os
from tqdm import tqdm
import os
import argparse

parser = argparse.ArgumentParser()
parser.description = 'Download video from .3m8u url'
parser.add_argument("-u", "--url", help="url of .3m8u", dest="url", type=str, default="0")
parser.add_argument("-n", "--name", help="save video name", dest="name", type=str, default="0")
args = parser.parse_args()

if args.url != 0 and args.name != 0:

    main_path = "https://cdn.605-zy.com/"
    # download_url = "https://cdn.605-zy.com/20210520/1YmE5mHe/index.m3u8"
    # video_name = "《逃避虽可耻但有用》第07集HD高清在线观看-迅雷下载-日剧电视剧-电影先生.mp4"
    download_url = args.url
    video_name = args.name

    ts_download_url = []
    data = requests.get(download_url).text
    url = re.findall(r"ppvod/(.+?).m3u8", data)[0]
    url = f"ppvod/{url}.m3u8"
    ts_all_path = os.path.join(main_path, url)

    ts_data = requests.get(ts_all_path).text
    with open("ts.txt", "w") as fr:
        fr.write(ts_data)

    with open("ts.txt", "r") as fr:
        content = fr.readlines()

    for i in content:
        if i[:-1].endswith(".ts"):
            ts_download_url.append(main_path[:-1] + i[:-1])

    loop = tqdm(enumerate(ts_download_url), desc="Downloading ts files", total=len(ts_download_url))
    for idx, url in loop:
        finished = False
        loop.set_postfix(total=f"{idx}/{len(ts_download_url)}")
        while(not finished):
            content = requests.get(url)
            if content.status_code == 200:
                with open(f"video/{idx}.ts", "wb") as fr:
                    content = content.content
                    fr.write(content)
                    with open(f"video/file.txt", "a") as f:
                        f.write(f"file '{idx}.ts'\n")
                    loop.update(1)
                    finished = True
            else:
                print(f"Download {idx}.ts error, retry..")
    print("Processing..")
    os.system(f"ffmpeg -f concat -i video/file.txt -c copy video/{video_name}")
    os.system("rm -rf video/*.ts video/file.txt")
