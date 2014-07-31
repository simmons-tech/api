#!/usr/bin/python

from ..utils import authentication_core
from ..utils import authorization_core

import binascii
import os

# Setup flask basics.
from flask import Flask, render_template, make_response, request, jsonify, redirect
app = Flask(__name__)

### SESSION LOOKUP AND STORE ###

# TODO: Do not use an in memory store. Make a LOGIN_SESSION Database.

session_cache = {}

def register_session(redirect, state, domain):
	session_id = binascii.hexlify(os.urandom(16)) # Hex Encoding for URL Saftey.
	session_cache[session_id] = (redirect, state, domain)
	return session_id

# Deletes the session and returns it.
def recall_session( session_id ):
	session_id = session_id.strip()
	# TODO: Delete to preserve memory...
	return session_cache[session_id]

################################

def domain_from_redirect( redirect ):
	#TODO: Use URL Parse.
	if 'mit.edu' in redirect:
		return '.mit.edu'
	return ''

@app.route('/')
def login_page():
	# Required args.
        redirect = request.args.get('redirect', None)
	if redirect == None:
		return "500: Must Provide Redirect (i.e. login/?redirect=google.com)"
	# Optional args.
        state = request.args.get('state', '')
	domain = request.args.get('domain', domain_from_redirect(redirect))

	# TODO: Generate session key? Don't expose redirect, state, domain.
	session_id = register_session(redirect, state, domain)

	# Lot of work in login.html.
	return render_template( 'login.html', session_id = session_id )

@app.route('/handler', methods=['POST'])
def login_handler():
	# TODO: This is only the local case, reflect that.
	session_id = request.args.get('session_id')
	username = request.form['username']
	password = request.form['password'] # TODO: This is horribly insecure... Use a burner key with SRP.
	redirect_link, state, domain = recall_session( session_id ) # TODO: Handle case where session_id not in cache.
	try:
		token = authentication_core.authenticate( username, password )
		response = make_response(redirect(redirect_link))
		response.set_cookie( 'username', username )
		response.set_cookie( 'token', token )
		return response
	except authentication_core.AuthenticationError:
		return "500: Authentication Error"

# TODO: Add redirect to this, default to login page.
@app.route('/invalidate', methods=['GET','POST'])
def invalidate_token():
	username = request.cookies.get('username')
	token = request.cookies.get('token')
        redirect_link = request.args.get('redirect', '/login/?redirect=http://simmons.mit.edu')
	try:
		authentication_core.invalidate_token( username, token )
		return make_response(redirect(redirect_link))
	except authentication_core.AuthenticationError:
		return "500: Authentication Error"

@app.route('/check')
def check_token():
	try:
		username = request.cookies.get('username')
		token = request.cookies.get('token')
		authentication_core.validate_token(username, token)
		return jsonify(response='200', username=username)
	except: # TODO: Restrict what this catches.
		return jsonify(response='401')

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()
