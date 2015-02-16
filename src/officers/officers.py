#!/usr/bin/python

from ..utils.sdb import Officers, sdb_session, Resident

# Setup flask basics.
from functools import wraps
from flask import Flask, request, jsonify, redirect, current_app, json
app = Flask(__name__)

# TODO: fix DoS vulnerabilties.

import json
from functools import wraps
from flask import redirect, request, current_app

from ..people.people import get_person

def get_officers():
	session = sdb_session()
	# Make a full list of people of interest...
	officers = []
	#print 'querying...'
	#print session.query(Officers)
	for officer in session.query(Officers).filter(Officers.removed == None):
		#print officer
		#print officer.username
		#try:
		for person in session.query(Resident).filter(Resident.username == officer.username):
			officers.append( {
				'kerberos'	:person.username,
				'firstname'	:person.firstname,
				'lastname'	:person.lastname,
				'year'		:person.year,
				#'title'		:person.title,
				'email'		:person.email,
				'position': officer.position
				} )
		#except Exception, ex:
		#	print ex
		
	session.close()
	#print officers, ' added'

	return officers

@app.route('/')
def serve_officers():
	#try:
	officers = get_officers()
	return json.dumps(get_officers())
	#except Exception, ex:
		#print ex

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
	app.run()
