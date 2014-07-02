#!/usr/bin/python

import lxml.html
import json

# Setup flask basics.
from flask import Flask, jsonify
app = Flask(__name__)

#TODO: Needs many improvements.
def scrape_laundryview():

	lvs = lxml.html.parse('http://laundryview.com/lvs.php')
	div = lvs.find(".//div[@id='campus1']")

	rooms = []
	statuses = []
	for a in div.findall('.//a'):
		rooms.append(str(a.text).strip().title())
	for span in div.findall('.//span'):
		statuses.append(str(span.text).strip())
	pairs = dict(zip(rooms, statuses))

	def format_room( room ):
		s = pairs[room]
		return {
			'name': room,
			'status': {'open_washers': s[1], 'open_dryers': s[7], 'total_washers':2, 'total_dryers':2}
			}

	return [ format_room( room ) for room in rooms ]

@app.route('/')
def serve_raw():
	return jsonify( rooms = scrape_laundryview() )

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
