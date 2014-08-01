#!/usr/bin/python

# Setup flask basics.
from flask import Flask, jsonify
from ..utils import authorization_core as authcore

app = Flask(__name__)

@app.route('/')
def serve_groups():
	return jsonify(groupnames = authcore.get_groupnames())

@app.route('/<groupname>/')
def serve_members( groupname ):
	return jsonify(
		groupname = groupname,
		members = list(authcore.members(groupname)))

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
	app.run()
