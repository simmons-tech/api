# This is a work in progress, MVP implementation. Please do not assume it is secure, because it is not in pretty much literally every way imaginable.
# DO NOT DEPLOY THIS UNTIL IT HAS BEEN FIXED.
# The complete implementation will be based on 858 code, but will need to be modified to support SSO based on MIT certs.
#
# This file seeks to implement the back-end of the RPC described at
# https://github.com/simmons-tech/wiki/wiki/Authentication-API

# System imports
import base64
import pbkdf2
import hashlib
import json
import sys
import os

# Util imports
sys.path.append( os.path.abspath( os.path.join(sys.path[0], '..') ) )
import db

# Authcore imports
import HMAC
from authentication_exceptions import *

# TODO: Cache results short term?
def is_user( name ):
	user_db = db.init('user')
	user = user_db.query(db.User).get( name )
	if user:
		return True
	return False

def get_user( username ):
	if not is_user( username ):
		raise NonexistentUserError( username )
	user_db = db.init('user')
	user = user_db.query(db.User).get( username )
	return user

### Private Helpers

def generate_new_token(user_db, person): # TODO: Should this function really commit to the db? Move commit to authenticate?
	hashinput = "%s%s" % (person.passhash, base64.b64encode(os.urandom(128)))
	person.token = hashlib.md5(hashinput).hexdigest()
	user_db.commit()
	return person.token

### Authentication

def authenticate( username, password ):
	user_db = db.init('user')
	user = user_db.query(db.User).get( username )
	if not user:
		raise NonexistentUserError( username )
	if user.passhash == pbkdf2.PBKDF2(password, user.salt).hexread(32):
		return generate_new_token(user_db, user)
	raise AuthenticationError( username )

# If the token is valid, this will run without issue.
# Otherwise, an AuthenticationError or
# NonexistentUserError will be raised.
def validate_token( username, token ):
	if not is_user( username ):
		raise NonexistentUserError( username )

	user = get_user( username )

	if user.token == None:
		raise AuthenticationError( username )

	if user.token == token:
		return
	raise AuthenticationError( username )

# If the message was HMAC'd with the correct token,
# this will run without issue. Otherwise, an
# AuthenticationError or NonexistentUserError 
# will be raised.
def validate_message( wrapped_message ):
	username = wrapped_message[ 'username' ]
	message = json.loads( wrapped_message[ 'message' ] )
	hmac = wrapped_message[ 'hmac' ]

	if not is_user( username ):
		raise NonexistentUserError( username )

	user = get_user( username )

	if user.token == None:
		raise AuthenticationError( username )

	if hmac == HMAC.encode( message, username, user.token )['hmac']:
		return

	raise AuthenticationError( username )
	

# TODO: Make this work.
def invalidate_token( username, token ):
	validate_token( username, token ) # Ensure the user is logged in.

	user_db = db.init('user')
	user = user_db.query(db.User).get( username )
	user.token = None
	user_db.commit()

'''
from ..authorization_core import restricted # This is a circular import

@restricted( "accounts-admin" )
def create_user( username, password ):
	user_db = db.init('user')
	person = user_db.query(db.User).get( username )
	if person:
		return UsernameAllocatedError( username )
	newperson = User()
	newperson.username = username
	newperson.salt = base64.b64encode(os.urandom(128))
	newperson.passhash = pbkdf2.PBKDF2(password, newperson.salt).hexread(32)
	user_db.add(newperson)
	user_db.commit()'''	

