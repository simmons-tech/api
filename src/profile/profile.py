#!/usr/bin/python

from ..utils.sdb import Resident, sdb_session

# Setup flask basics.
from flask import Flask, jsonify, make_response
app = Flask(__name__)

# TODO: fix DoS vulnerabilties.
# TODO: Used in people.py as well, perhaps abstract to sdb?

def get_people():
	session = sdb_session()

	# Make a full list of people of interest...
	people = []
	for person in session.query(Resident):
		if person.private:
			continue
		people.append( {
			'kerberos'	:person.username,
			'firstname'	:person.firstname,
			'lastname'	:person.lastname,
			'room'		:person.room,
			'year'		:person.year,
			'title'		:person.title,
			'email'		:person.email,
			} )

		
	session.close()

	return people

def get_person( username ):
	people = get_people()
	for person in people:
		if person['kerberos'] == username:
			return person

@app.route('/<username>/')
def serve_profile( username ):
	resident = get_person( username )
	profile = {
		"title": resident['title'],
		"hometown": "DOESN'T WORK YET :(",
	}
	return jsonify( **profile )

@app.route('/<username>/picture.png')
def serve_profile_picture( username ):
	# For now, serve the same default picture for everyone.
	resp = make_response( open( "./static/default.png" ).read() )
	resp.content_type = "image/png"
	return resp

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
