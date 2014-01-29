#!/usr/bin/python

# Add the Simmons DB utils to the PYTHONPATH (temporary).
import sys, os
sys.path.append( os.path.abspath( os.path.join(sys.path[0], '../utils') ) )

from sdb import Resident, sdb_session

# Setup flask basics.
from flask import Flask, render_template, make_response
app = Flask(__name__)

# BEGIN HELPERS ###########################################

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

# END HELPERS #############################################

# BEGIN API ###############################################

@app.route('/<username>/')
def serve_profile( username ):
	return render_template('resident.json', resident = get_person( username ) )

@app.route('/<username>/picture.png')
def serve_profile_picture( username ):
	# For now, serve the same default picture for everyone.
	resp = make_response( open( "./static/default.png" ).read() )
	resp.content_type = "image/png"
	return resp

# END API #################################################

# RUN FLASK APP ###########################################

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()

# END FLASK APP ###########################################
