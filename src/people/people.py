#!/usr/bin/python

# Add the Simmons DB utils to the PYTHONPATH (temporary).
import sys, os
sys.path.append( os.path.abspath( os.path.join(sys.path[0], 'utils') ) )

from sdb import Resident, ActiveUsernames, sdb_session

# Setup flask basics.
from flask import Flask, render_template, request
app = Flask(__name__)

# TODO: fix DoS vulnerabilties.

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

def get_active_residents():
	session = sdb_session()

	people = get_people()
	
	# Figure out which users are active...
	active = {}
	for username in session.query(ActiveUsernames):
		active[ username.username ] = username.active

	active_residents = []
	for person in people:
		if active[ person['kerberos'] ]:
			active_residents.append( person )

	session.close()

	return active_residents

@app.route('/')
def serve_active_residents():
	if request.args.get('q'):
		return  serve_query( request.args.get('q') )
	return render_template('residents.json', residents = get_active_residents() )

@app.route('/<username>/')
def serve_person( username ):
	return render_template('resident.json', resident = get_person( username ) )

def serve_query( query ):
	querylets = query.split()

	# TODO: This could be done with a proper SQL Query.
	# To match a query, a user has to have each space seperated token (querylet) as part of its special fields.
	# The special fields are 'kerberos', 'firstname', and 'lastname'.
	# Matches are case insenstive.
	#
	# For room based search, check the rooming_assignment API.
	def is_match( resident ):
		for querylet in querylets:
			matches_querylet =  False
			for field in [ 'kerberos','firstname','lastname' ]:
				if querylet.lower() in resident[field].lower():
					matches_querylet = True
			if not matches_querylet:
				return False
		return True

	return render_template('residents.json', residents = filter( is_match, get_active_residents() ) )

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
