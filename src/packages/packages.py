#!/usr/bin/python

from ..utils.sdb import Package, sdb_session

# Setup flask basics.
from flask import Flask, render_template, request
app = Flask(__name__)

def get_packages():
	session = sdb_session()

	# query db, get number of rows corresponding to a given user
	# this may be able to be made into a single sql query rather than using a dict
	packages = {}
	for p in session.query(Package).filter(Package.pickup == None):
		if p.recipient in packages:
			packages[p.recipient] += 1
		else:
			packages[p.recipient] = 1

	session.close()
	return packages

@app.route('/')
def serve_all_packages():
	return render_template('packages.json', packages = get_packages() )

@app.route('/<username>/')
def serve_user_packages( username ):
	packages = get_packages()
	if username in packages:
		return str( packages[ username ] )
	return "0"

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
