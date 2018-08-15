# -*- coding: utf-8 -*-

import os, sys, threading, time, signal, twitter, csv, video, shutil
from datetime import datetime

conKey = ""
conSec = ""
accTok = ""
accSec = ""
tweets = []
threads = []
postInt = 1
videos = []
timeBase = time.time()

def auth():
	# check for stored data

	fl = ""
	global conKey
	global conSec
	global accTok
	global accSec

	try:
		fl = open("config", "r+").read()
		if(raw_input("\nPrevious settings found. Should use it? (y/n): ") == "n"):
			fl = ""
	except:
		print("\nNo previous settings found")

	if(fl == ""):
		#ask for credentials
		conKey = raw_input("Consumer Key: ")
		conSec = raw_input("Consumer Secret: ")
		accTok = raw_input("Access Token: ")
		accSec = raw_input("Access Token Secret: ")
		fr = open("config", "w+")
		fr.write(conKey + ":" + conSec + ":" + accTok + ":" + accSec)
	else:
		conKey = fl.split(":")[0]
		conSec = fl.split(":")[1]
		accTok = fl.split(":")[2]
		accSec = fl.split(":")[3]

	#login
	twitter.auth(conKey, conSec, accTok, accSec)

def schedule():
	
	path = ""
	deli = ""
	global conKey
	global conSec
	global accTok
	global accSec

	try:
		cfg = open("config", "r").read()
		path = cfg.split(":")[4]
		deli = cfg.split(":")[5]

		if(raw_input("\nPrevious CSV found (" + path + "). Should use it? (y/n): ") == "n"):
			path = raw_input("CSV file name (e.g sample.csv): ")
			deli = raw_input("Delimiter (default: ','): ")
	except:
		print("\nNo previous CSV found")
		path = raw_input("CSV file name (e.g sample.csv): ")
		deli = raw_input("Delimiter (default: ','): ")

	if(deli == ""):
		deli = ","
	
	open("config", "r+").write(conKey + ":" + conSec + ":" + accTok + ":" + accSec + ":" + path + ":" + deli)

	csvf = ""

	try:
		csfv = csv.reader(open(path, "r"), delimiter=deli)
	except:
		print("\nCSV corrupted or not found. Try again.\n")
		schedule()
		return
		
	global tweets
	tweets = []

	for r in csfv:
		tweets.append(r)

def start():

	print("")

	global videos
	global threads

	cnt = 0

	for vd in videos:
		work(vd, 0, cnt)	
		cnt = cnt + 2		

	print("\n--== Results ==--\n")
	
def work(tw, ti, cnt):
	print("[Pre-Upload] Starting...")

	tw[1] = video.cutVideo(tw[1])

	print("[Pre-Upload] Video done.")

	#

	global template_1

	tmp = template_1
	#open("template_1.txt", "r").read()

	tmp = tmp.replace("[title]", tw[0])
	tmp = tmp.replace("[link]", tw[2])

	tos = [ tmp, "video/2_" + tw[1]]

	media = twitter.start(conKey, conSec, accTok, accSec, "video/1_" + tw[1], tmp)

	if media != 0:
		print("[Pre-Upload] Done")
	else:
		if ti <= 0:
			print("[Pre-Upload] Failed. Trying again")
			work(tw, ti + 1, cnt)
		else:
			print("[Pre-Upload] Aborted after 3 attemps. Maybe this file isn't supported by Twitter.")
			print("[Pre-Upload] Aborted: " + tw[1])
		return

	global timeBase, postInt
	
	tim = (timeBase + postInt + (postInt * cnt)) - time.time()
	cnt = cnt + 1

	t = threading.Timer(tim, send, [tos, media])
	t.start()
	threads.append("")
	print("[Tweet] Post scheduled to ~" + str(int(tim / 60)) + " minute(s) from now")
	print("")

	##

	global template_2

	tmp = template_2

	#tmp = open("template_2.txt", "r").read()

	tmp = tmp.replace("[title]", tw[0])
	tmp = tmp.replace("[link]", tw[2])

	tos = [ tmp, "video/2_" + tw[1]]

	media = twitter.start(conKey, conSec, accTok, accSec, "video/2_" + tw[1], tmp)

	if media != 0:
		print("[Pre-Upload] Done")
	else:
		if ti <= 0:
			print("[Pre-Upload] Failed. Trying again")
			work(tw, ti + 1, cnt)
		else:
			print("[Pre-Upload] Aborted after 3 attemps. Maybe this file isn't supported by Twitter.")
			print("[Pre-Upload] Aborted: " + tw[1])
		return
	
	tim = (timeBase + postInt + (postInt * cnt)) - time.time()

	t = threading.Timer(tim, send, [tos, media])
	t.start()
	threads.append("")
	print("[Tweet] Post scheduled to ~" + str(int(tim / 60)) + " minute(s) from now")
	print("")

	#
	

def send(tw, media):
	print("[Tweet] Initializing...")
	twitter.tweet(conKey, conSec, accTok, accSec, tw[1], tw[0], media)

def getVideos():
	global videos, postInt
	videos, postInt = video.get()

def signal_handler(sig, frame):
	sys.exit(0)

def main():

	t = threading.Timer(60 * 60 * 24, main)
	t.start()

	try:
		# set everything
		print("---=== TwitterVideoBot - https://fiverr.com/lihilip ===---")
		auth()
		#schedule()
		getVideos()
		start()
		signal.signal(signal.SIGINT, signal_handler)
		try:
			signal.pause() # not work on Windows, batch pause
		except:
			pass

	except Exception, ex:
		print(ex)
		print("\nShutting down...")
		for t in threads:
			#t.cancel()
			print("Cancelling scheduled tweet...")
		print("Done.")


template_1 = u"📷Pt.1/2\n[title]\n👇👇👇\n[link]\n\n👆👆👆\n🔐Next Part UNLOCKED in 1 Hour/15 RTs🔓\n@HentaiAdvisor @DoujinsApp ManuelH84670868\n#adult #nsfw #porn"
template_2 = u"📷Pt.2/2\n[title]\n👇👇👇\n[link]\n\n👆👆👆\n🔐Next Part UNLOCKED in 1 Hour/15 RTs🔓\n@HentaiAdvisor @DoujinsApp @mh447885570\n#adult #nsfw #porn"

try:
	shutil.rmtree("cache", ignore_errors=False, onerror=None)
	shutil.rmtree("video", ignore_errors=False, onerror=None)
except Exception, e:
	print(e)
	pass

main()












