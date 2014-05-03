#!/usr/bin/python

# Add the Simmons DB utils to the PYTHONPATH (temporary).
import sys, os
sys.path.append( os.path.abspath( os.path.join(sys.path[0], '../utils') ) )
sys.path.append( os.path.abspath( os.path.join(sys.path[0], 'utils') ) )

import authcore

# Setup flask basics.
from flask import Flask, render_template, make_response, request
app = Flask(__name__)

# TODO: Remove in production? DO NOT PRINT TOKEN FOR FUCKS SAKE.
@app.route('/')
def test():
	username = request.cookies.get('username')
	token = request.cookies.get('token')
	return render_template( 'test.html', username = username, token = token )

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		try:
			token = authcore.authenticate( username, password )
			resp = make_response( render_template( 'logged_in.html', username = username ) )
			resp.set_cookie( 'username', username )
			resp.set_cookie( 'token', token )
			return resp
		except authcore.AuthenticationError:
			return "Authentication Error"
	else:
		return render_template( 'login.html' )

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	username = request.cookies.get('username')
	token = request.cookies.get('token')
	try:
		authcore.invalidate_token( username, token )
		resp = make_response( render_template( 'logged_out.html', username = username ) )
		resp.set_cookie( 'username', '' )
		resp.set_cookie( 'token', '' )
		return resp
	except authcore.AuthenticationError:
		return "Authentication Error"

# TODO: Remove in production.
@app.route('/authtest')
def authtest():
	username = request.cookies.get('username')
	token = request.cookies.get('token')

	@authcore.restricted( "simmons-tech" )
	def super_secret():
		return "Welcome, Simmons Tech Member " + username + "!"

	try:
		return super_secret( username, token )
	except authcore.AuthenticationError:
		return "Nice try " + username + ". No bits for you."


if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
