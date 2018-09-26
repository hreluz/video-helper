# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import json
import re
import urllib
import os
import time
from yaspin import yaspin

def take_html(file):
	if not os.path.exists(file):
		return

	html = open(file, "r")
	scripts = BeautifulSoup(html).find('script').string
	
	if scripts:
		index_start = scripts.find('{"cdn_url":')
		index_end = scripts.find('meo.com"};')
		was_found = scripts[index_start:index_end+9]  if index_start >= 0 and index_end >= 0 else False

		if was_found:
			json_object = json.loads(was_found)
			video_title = json_object['video']['title']
			for progressive in json_object['request']['files']['progressive']:
				video = video_path + '/' + video_title + '.mp4'
				try:
					if os.path.exists(video):
						sp.write("> Video %s ----> skipped because already exists" %(video_title))		
					else:
						urllib.URLopener().retrieve(progressive['url'],video)
						sp.write("> Video %s download complete" %(video_title))				
					os.remove(file)
				except:
					sp.write("############### ERROR in file %s ###############" %(file))
				break

def set_videos_folder(file_path,folder_name,type):

	if not does_file_exists_and_is_not_empty(file_path):
		path = raw_input('Enter the path for saving the %s (A folder would be created), leave empty to create it here:' %(type))
		if path:
			path += "/"
		path = path + folder_name

		if not os.path.exists(path):
			os.mkdir(path)

		write(file_path,path)
	else:
		path = read(file_path)

	return path

def read(file_path):
	if file_path:
		file = open(file_path,"r")  
		return file.read() 

def write(file_path, video_path):
	file = open(file_path,"w")  
	file.write(video_path) 		 
	file.close()


def does_file_exists_and_is_not_empty(file_path):
	return os.path.exists(file_path) and os.stat(file_path).st_size > 0 

video_path = set_videos_folder("video_path","videoFolder","videos")
html_path = set_videos_folder("html_path","htmlFolder","HTML")

if video_path and html_path:
	with yaspin(text="Downloading videos", color="cyan") as sp:
		for html in sorted(os.listdir(html_path)):
			html = html_path + '/' + html
			take_html(html)

    	sp.ok("✔")
else:
	print "There is a problem with the video path or html path"