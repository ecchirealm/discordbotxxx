# -*- coding: utf-8 -*-

import requests, urllib, os, subprocess

def download_file(url):
    local_filename = "cache/" + url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def shortURL(u):

    serv = "http://twtporn.xyz/yourls-api.php?username=admin&password=825852Raw!&action=shorturl&format=json&url="

    r = requests.get(serv + urllib.quote_plus(u))

    return r.json()["shorturl"]

def cutVideo(v):
    
    print "[Video] Downloading: " + v

    # download
    try:
        os.makedirs("cache")
        os.makedirs("video")
    except OSError:
        pass

    lf = download_file(v).split("/")[1]

    dura = ""

    for line in run_command("ffmpeg -i cache/" + lf):
        if "Duration" in line:
            dura = line.split("ration:")[1]
    
    h = int(dura.split(":")[0]) * 60 * 60
    m = int(dura.split(":")[1]) * 60
    s = int(dura.split(":")[2].split(".")[0])

    print "[Video] Cutting video... May take awhile"

    cmd = "ffmpeg -ss " + str((h + m + s) / 2) + " -i cache/" + lf + " -t 60 -async 1 -strict -2 video/1_" + lf + " -y"

    for line in run_command(cmd):
        a = line

    print "[Video] Cutting video... May take awhile"

    cmd = "ffmpeg -ss " + str(((h + m + s) / 2) + 60) + " -i cache/" + lf + " -t 60 -async 1 -strict -2 video/2_" + lf + " -y"

    for line in run_command(cmd):
        a = line

    return lf

def run_command(command):
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def get():
    
    print("")
    url  = raw_input("Site URL: ")
    time = int(raw_input("How many minutes between each tweet? ")) * 60
    print("")

    print "[Video] Requesting videos..."

    r = requests.get(url).text

    vds = r.split("well well-sm\"> <a")

    videos = []

    for v in vds:

        if("href=\"/video/" in v):

            u = "http://pornohand.com" + v.split("href=\"")[1].split("\"")[0]

            ru = requests.get(u).text

            title = ru.split("<title>")[1].split("</title>")[0]
            furl = ru.split("<source")[1].split("src=\"")[1].split("\"")[0]
            vurl = shortURL(u)

            videos.append([title, furl, vurl])
    
    print "[Video] Got " + str(len(videos)) + " video(s) on that link"

    return videos, time




