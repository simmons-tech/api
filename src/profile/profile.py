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
			'home_city'	:person.home_city,
			'home_state'	:person.home_state,
			'home_country'	:person.home_country,
			'quote'			:person.quote,
			'homepage'		:person.homepage,
			'favorite_category'	:person.favorite_category,
			'favorite_value'	:person.favorite_value,
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
		"home_city": resident['home_city'],
		"home_state"	:resident['home_state'],
		"home_country"	:resident['home_country'],
		"quote"			:resident['quote'],
		"homepage"		:resident['homepage'],
		"favorite_category"	:resident['favorite_category'],
		"favorite_value"	:resident['favorite_value'],
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
