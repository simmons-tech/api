#!/usr/bin/python

# Setup flask basics.
from flask import Flask, jsonify
app = Flask(__name__)

import cosmos_db

@app.route('/')
def serve_rooms():
	roomnums = [ room.num for room in cosmos_db.allRooms ]
	return jsonify( rooms = roomnums )

@app.route('/<roomnum>/')
def serve_room( roomnum ):
	room = cosmos_db.find( roomnum )
	return jsonify(
		roomnum = room.num,
		grt = room.grt,
		capacity = room.capacity,
		sq_ft = room.size,
		side = room.view )

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
