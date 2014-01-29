#!/usr/bin/python

# Add the Simmons DB utils to the PYTHONPATH (temporary).
import sys, os
sys.path.append( os.path.abspath( os.path.join(sys.path[0], '../utils') ) )

# Setup flask basics.
from flask import Flask, render_template, make_response
app = Flask(__name__)

import cosmos_db

# BEGIN HELPERS ###########################################

def get_rooms():
	result = []
	for room in cosmos_db.allRooms:
		result.append( room.num )
	return result

def get_room( roomnum ):
	return cosmos_db.find( roomnum )

# END HELPERS #############################################

# BEGIN API ###############################################

@app.route('/')
def serve_rooms():
	return render_template('rooms.json', rooms = get_rooms() )

@app.route('/<roomnum>/')
def serve_room( roomnum ):
	return render_template('room.json', room = get_room( roomnum ) )

# END API #################################################

# RUN FLASK APP ###########################################

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()

# END FLASK APP ###########################################
