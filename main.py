# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import json
import urllib
import os
from datetime import datetime
from yaspin import yaspin
import unidecode

def take_html(file):
	if not os.path.exists(file):
		return

	with open(file) as f:
		html = " ".join([x.strip() for x in f])

	scripts = BeautifulSoup('<script>' + html + '</script>').find('script').string
	
	if scripts:
		index_start = scripts.find('{"cdn_url":')
		index_end = scripts.find('meo.com"};')
		was_found = scripts[index_start:index_end+9]  if index_start >= 0 and index_end >= 0 else False

		if was_found:
			video, video_title, url = get_url_and_video_details(was_found)
			try:
				if url:
					if does_video_exists(video_title):
						sp.write("> Video %s ----> skipped because already exists" %(video_title))		
					else:
						urllib.URLopener().retrieve(url,video)
						sp.write("> Video %s download complete" %(video_title))				
					os.remove(file)
				else:
					sp.write("############### ERROR in file %s ############### Error: %s" %(file, 'URL NOT FOUND'))
			except Exception, e:
				sp.write("############### ERROR in file %s ############### Error: %s" %(file, str(e)))


def does_video_exists(video):
	for f in os.listdir(video_path):
		if video in f:
			return True
	return False


def get_url_and_video_details(was_found):
	json_object = json.loads(was_found)
	video_title = unidecode.unidecode(json_object['video']['title'])
	video = video_path + '/' + (datetime.utcnow().strftime('%s') + '____' + video_title + '.mp4').replace('/','_')
	height = 0
	url = ''

	for progressive in json_object['request']['files']['progressive']:
		if progressive['height'] > height:
			height = progressive['height']
			url = progressive['url']

	return video, video_title, url					

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