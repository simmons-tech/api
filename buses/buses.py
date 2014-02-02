#!/usr/bin/python

from lxml import etree
import json

# Setup flask basics.
from flask import Flask, render_template, request
app = Flask(__name__)

def get_buses():
	# Nextbus api: http://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf
	baseURL = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions'
	agency = 'mit'
	stop = 'simmhl'

	techURL = '{}&a={}&r={}&s={}'.format(baseURL, agency, 'tech', stop)
	saferideURL = '{}&a={}&r={}&s={}'.format(baseURL, agency, 'saferidecambwest', stop)

	try:
		techTimes = etree.parse(techURL).findall('predictions/direction/prediction')
		saferideTimes = etree.parse(saferideURL).findall('predictions/direction/prediction')
	except:
		techTimes = []
		saferideTimes = []

	times = []

	def nextbus( name, time_till ):
		return {'name':name,'time_till':time_till}

	for bus in techTimes:
		times.append( nextbus( "Tech Shuttle", bus.get('minutes') ) )
	for bus in saferideTimes:
		times.append( nextbus( "Saferide Cambridge West", bus.get('minutes') ) )

	times = sorted( times, key=lambda nb: nb['time_till'] )

	return times

@app.route('/')
def serve_raw():
	return json.dumps( get_buses() )

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
