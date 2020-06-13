#!/bin/bash
directory=".env"

if [ ! -d "${directory}" ]; then
	virtualenv -p /usr/bin/python2.7 .env && source .env/bin/activate && pip install -r requirements.txt
else
	source .env/bin/activate
fi
python main.py