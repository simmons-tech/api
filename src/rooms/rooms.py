#!/usr/bin/python

# Setup flask basics.
from ..utils import db
from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/')
def serve_rooms():
	room_db = db.init('room')
	rooms = room_db.query(db.Room).all()
	roomnums = [ room.num for room in rooms ]
	return jsonify( rooms = roomnums )

@app.route('/<roomnum>/')
def serve_room( roomnum ):
	room_db = db.init('room')
	room = room_db.query(db.Room).get(roomnum)

	return jsonify(
		roomnum = room.num,
		type = room.type,
		size = room.size,
		view = room.view,
		X = room.X,
		Y = room.Y,
		hasCurvyWall = room.hasCurvyWall,
		bathroom = room.bathroom
	)

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
