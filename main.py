from BeautifulSoup import BeautifulSoup
import json
import re
import urllib
import os


def take_html(file):
	if not os.path.exists(file):
		return

	html = open(file, "r")
	scripts = BeautifulSoup(html).find('script')
	
	if scripts:
		was_found = re.search(r'var r=(.*?);if' , scripts.string)
		if was_found:
			json_object = was_found.group(1) 
			json_object = json.loads(json_object)
			video_title = json_object['video']['title']
			for progressive in json_object['request']['files']['progressive']:
				urllib.URLopener().retrieve(progressive['url'],video_path + '/' + video_title + '.mp4')
				break
	os.remove(file)				

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
	for html in os.listdir(html_path):
		html = html_path + '/' + html
		take_html(html)

	print "Done"
else:
	print "There is a problem with the video path or html path"