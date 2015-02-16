#!/usr/bin/python

from ..utils.sdb import Officers, sdb_session

# Setup flask basics.
from functools import wraps
from flask import Flask, request, jsonify, redirect, current_app
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
	for officer in session.query(Officers, removed=None):
		officers.append( get_person(officer['username']) )
		
	session.close()

	return officers

@app.route('/')
def serve_officers():
	officers = get_officers()
	return jsonify( officers )

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
	app.run()
