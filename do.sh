#!/bin/bash
directory=".env"

if [ ! -d "${directory}" ]; then
	virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
else
	source .env/bin/activate
fi
python main.py