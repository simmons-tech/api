#!/usr/bin/python

import lxml.html
import json

# Setup flask basics.
from flask import Flask, render_template, request
app = Flask(__name__)

def get_laundry():
	print "GOT HERE!"
	lvs = lxml.html.parse('http://laundryview.com/lvs.php')
	div = lvs.find(".//div[@id='campus1']")
	rooms = []
	statuses = []
	for a in div.findall('.//a'):
		rooms.append(str(a.text).strip().title())
	for span in div.findall('.//span'):
		statuses.append(str(span.text).strip())

	pairs = dict(zip(rooms, statuses))

	def parseAvalibility( s ):
		return {'open_washers': s[1], 'open_dryers': s[7], 'total_washers':2, 'total_dryers':2}

	simmons = {}
	for room in rooms:
		if room.startswith('Simmons'):
			simmons[room[-3:]] = parseAvalibility( pairs[room] )

	return simmons

@app.route('/')
def serve_raw():
	return json.dumps( get_laundry() )

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
