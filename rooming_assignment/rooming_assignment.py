#!/usr/bin/python

# Add the Simmons DB utils to the PYTHONPATH (temporary).
import sys, os
sys.path.append( os.path.abspath( os.path.join(sys.path[0], 'utils') ) )

from sdb import Resident, sdb_session

# Setup flask basics.
from flask import Flask, render_template, make_response
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

def get_person_room( username ):
	people = get_people()
	for person in people:
		if person['kerberos'] == username:
			return person['room']

def get_room_people( room ):
	result = []
	for person in get_people():
		if person['room'] == room:
			result.append( person['kerberos'] )
	return result

@app.route('/person/<username>/')
def serve_person_room( username ):
	return str( get_person_room( username ) ) # TODO: Template

@app.route('/room/<roomnum>/')
def serve_room_people( roomnum ):
	return str( get_room_people( roomnum ) ) # TODO: Template

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
