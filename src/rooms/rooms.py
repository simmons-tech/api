#!/usr/bin/python

# Setup flask basics.
from flask import Flask, render_template, make_response
app = Flask(__name__)

import cosmos_db

def get_rooms():
	result = []
	for room in cosmos_db.allRooms:
		result.append( room.num )
	return result

def get_room( roomnum ):
	return cosmos_db.find( roomnum )

@app.route('/')
def serve_rooms():
	return render_template( 'rooms.json', rooms = get_rooms() )

@app.route('/<roomnum>/')
def serve_room( roomnum ):
	return render_template( 'room.json', room = get_room( roomnum ) )

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
