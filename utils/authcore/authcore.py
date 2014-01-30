# This is a work in progress, MVP implementation. Please do not assume it is secure, because it is not in pretty much literally every way imaginable.
# DO NOT DEPLOY THIS UNTIL IT HAS BEEN FIXED.
# The complete implementation will be based on 858 code, but will need to be modified to support SSO based on MIT certs.
#
# This file seeks to implement the back-end of the RPC described at
# https://github.com/simmons-tech/wiki/wiki/Authentication-API

## TEMP INIT
import base64
import pbkdf2
import hashlib
import json
import sys
import os

sys.path.append( os.path.abspath( os.path.join(sys.path[0], '../') ) )
from db import *
from HMAC import *

#TODO: Properly consider race conditions and efficiency. Perhaps a global db lock or similar is in order?

# TODO: Make work.
#def users():
#	return users.keys()
#
#def groups():
#	return groups.keys()

def is_user( name ):
	db = init('user')
	user = db.query(User).get( name )
	if user:
		return True
	return False

def get_user( username ):
	assert is_user( username )
	db = init('user')
	user = db.query(User).get( username )
	return user

def is_group( name ):
	db = init('group')
	group = db.query(Group).get( name )
	if group:
		return True
	return False

def get_group( groupname ):
	assert is_group( groupname )
	db = init('group')
	group = db.query(Group).get( groupname )
	return group

def type_of( name ):
	if is_user( name ):
		return 'user'
	if is_group( name ):
		return 'group'
	return None

def is_owner( user, group ):
	assert is_group( group )
	assert is_user( user )
	if type_of( get_group( groupname ).owner ) == 'user':
		return get_group( groupname ).owner == user
	return is_member( user, group )

### Private Helpers

def generate_new_token(db, person):
	hashinput = "%s%s" % (person.passhash, base64.b64encode(os.urandom(128)))
	person.token = hashlib.md5(hashinput).hexdigest()
	db.commit()
	return person.token

### Authentication

def authenticate( username, password ):
	db = init('user')
	person = db.query(User).get( username )
	if not person: # TODO: Throw Exception?
		return None
	if person.passhash == pbkdf2.PBKDF2(password, person.salt).hexread(32):
		return generate_new_token(db, person)
	else:
		return None

# TODO: Make this work.
def invalidate_token( username, token ):
	assert is_user( username )
	assert users[ username ].token != None
	assert users[ username ].token == token
	
	users[ user ].token = None

def validate_message( message, hmac, username ):
	assert is_user( username )
	user = get_user( username )
	assert user.token != None
	
	return hmac == HMAC( message, user.token )

def validate_token( username, token ):
	assert is_user( username )

	db = init('user')
	user = db.query(User).get( username )
	if not user:
		return False
	return user.token == token

### Membership

# TODO: Protect against loops? Maybe do that during registration.

def is_member( user, group ):
	assert is_user( user )
	assert is_group( group )
	# Inefficient, but simple.
	return user in members( group )

def members( groupname ):
	assert is_group( groupname )
	m = set()
	m = m | set( json.loads( get_group( groupname ).immediate_members ) )
	for subgroup in json.loads( get_group( groupname ).subgroups ):
		m = m | members( subgroup )
	return m

def immediate_members( group ):
	assert is_group( group )
	return get_group( groupname ).immediate_members

def subgroups( group ):
	assert is_group( group )
	return get_group( groupname ).subgroups

### restricted decorator ###
#
# A key part of the authcore; allows for easy use of the auth module in other APIs.
#
# When applied to a function, it integrates with the authentication module.
# For now, this does mean that it changes the function header slightly.
#
# f( x1, x2, ... ) -> f( user, token, x1, x2, ... )
#
# To restrict a function f to either (group) "simmons-tech", (group) "accounts-admin", or (user) "woursler":
#
## @restricted([ "simmons-tech", "accounts-admin", "woursler" ])
## def f( x1, x2 ):
## 	dangerous_stuff_here
#
# There is an additional argument require_all. If set to true, the user must match every constraint passed
# in the list.
#
# i.e. @restricted([ "simmons-tech", "accounts-admin" ]) restricts usage to people who are in both groups
# (as opposed to just one or the other).
#
# See the Wiki article on /auth/ for more details on usage and security guarantees.
#
# TL;DR, this decorator is for convenience and does not provide security against an
# adversary with code execution over your relevant environment.
#
# TODO: Make a variant for HMAC'd messages.
#
###

def restricted( names, require_all = False ):
	# Support passing a single name.
	if isinstance( names, basestring ):
		names = [ names ]
	def restricted_decorator( f ):
		def decorated_f( user, token, *args, **kwargs ):
			# Pre-permissions sanity check.
			assert is_user( user )
			for name in names:
				assert type_of( name ) != None

			# Permissions Check.
			# Validate that the user requesting access is who they say they are.
			assert validate_token( user, token )
			# For each name, check membership.
			approval = set()
			for name in names:
				if type_of( name ) == 'user':
					approval.add( name == user )
				if type_of( name ) == 'group':
					approval.add( is_member( user, name ) )
			
			if require_all:
				assert False not in approval
			assert True in approval

			f( *args, **kwargs )
		return decorated_f
	return restricted_decorator

# TODO: Comprehensive testing across JSON formats.
# TODO: Documentation.
# TODO: Rename to something sensible.
def authenticate_message( names, require_all = False ):
	# Support passing a single name.
	if isinstance( names, basestring ):
		names = [ names ]
	def authenticate_message_decorator( f ):
		def decorated_f( authenticated_message ):
			# Unpackage the message.
			user    = authenticated_message[ 'user' ]
			hmac    = authenticated_message[ 'hmac' ]
			message = authenticated_message[ 'message' ]

			# Pre-permissions sanity check.
			assert is_user( user )
			for name in names:
				assert type_of( name ) != None
			
			# Check the message if from the user.
			assert validate_message( message, hmac, user )
			# For each name, check membership.
			approval = set()
			for name in names:
				if type_of( name ) == 'user':
					approval.add( name == user )
				if type_of( name ) == 'group':
					approval.add( is_member( user, name ) )

			if require_all:
				assert False not in approval
			assert True in approval
			
			f( json.loads( message ) )
		return decorated_f
	return authenticate_message_decorator	

### Account management

@restricted( "accounts-admin" )
def create_user( username, password ):
	assert type_of( username ) == None
	db = init('user')
	person = db.query(User).get( username )
	if person:
		return None
	newperson = User()
	newperson.username = username
	newperson.salt = base64.b64encode(os.urandom(128))
	newperson.passhash = pbkdf2.PBKDF2(password, newperson.salt).hexread(32)
	db.add(newperson)
	db.commit()

@restricted( "accounts-admin" )
def create_group( groupname, owner = "accounts-admin" ):	
	assert type_of( groupname ) == None
	assert type_of( owner ) != None

	db = init('group')
	group = db.query(Group).get( groupname )
	if group:
		return None
	newgroup = Group()
	newgroup.groupname = groupname
	newgroup.owner = owner
	newgroup.immediate_members = json.dumps([])
	newgroup.subgroups = json.dumps([])
	db.add(newgroup)
	db.commit()

def add_to_group( admin_user, admin_token, name, groupname ):
	assert is_group( groupname )

	@restricted([ "accounts-admin", get_group( groupname ).owner ])
	def dangerous_code():
		assert type_of( name ) != None

		db = init('group')
		group = db.query(Group).get( groupname )

		if type_of( name ) == 'user':
			immediate_members = set( json.loads( group.immediate_members ) )
			immediate_members.add( name )
			group.immediate_members = json.dumps( list( immediate_members ) )
		elif type_of( name ) == 'group':
			subgroups = set( json.loads( group.subgroups ) )
			subgroups.add( name )
			group.subgroups = json.dumps( list( subgroups ) )
		db.commit()

	dangerous_code( admin_user, admin_token )

def remove_from_group( admin_user, admin_token, name, groupname ):
	assert is_group( groupname )
	
	@restricted([ "accounts-admin", get_group( groupname ).owner ])
	def dangerous_code():
		assert type_of( name ) != None

		db = init('group')
		group = db.query(Group).get( groupname )

		if type_of( name ) == 'user':
			immediate_members = set( json.loads( group.immediate_members ) )
			immediate_members.remove( name )
			group.immediate_members = json.dumps( list( immediate_members ) )
		elif type_of( name ) == 'group':
			subgroups = set( json.loads( group.subgroups ) )
			subgroups.remove( name )
			group.subgroups = json.dumps( list( subgroups ) )
		db.commit()



def transfer_group_ownership( admin_user, admin_token, groupname, new_owner ):
	assert is_group( groupname )
	
	@restricted([ "accounts-admin", get_group( groupname ).owner ])
	def dangerous_code():
		assert type_of( new_owner ) != None
		db = init('group')
		group = db.query(Group).get( groupname )
		group.owner = new_owner
		db.commit()

	dangerous_code( admin_user, admin_token )

	

### __main__
if __name__ == '__main__':

	admin_token = authenticate( 'admin', 'password' )

	create_user( 'admin', admin_token, 'woursler', 'password2' )
	create_user( 'admin', admin_token, 'adat', 'password3' )
	create_user( 'admin', admin_token, 'larsj', 'password4' )
	create_user( 'admin', admin_token, 'timwilz', 'password6' )
	create_user( 'admin', admin_token, 'omalley1', 'password7' )

	larsj_token = authenticate( 'larsj', 'password4' )
	timwilz_token = authenticate( 'timwilz', 'password6' )

	create_group( 'admin', admin_token, 'simmons-tech', 'larsj' )

	@restricted( "simmons-tech" )
	def super_secret( s ):
		print "Welcome to Simmons Tech. Your string is: " + s

	@authenticate_message( "simmons-tech" )
	def authd_echo( message ):
		print message

	add_to_group( 'larsj', larsj_token, 'woursler', 'simmons-tech' )
	add_to_group( 'admin', admin_token, 'adat', 'simmons-tech' )
	add_to_group( 'larsj', larsj_token, 'larsj', 'simmons-tech' )

	transfer_group_ownership( 'larsj', larsj_token, 'simmons-tech', 'adat' )

	adat_token = authenticate( 'adat', 'password3' )

	add_to_group( 'adat', adat_token, 'omalley1', 'simmons-tech' )

	# TODO: Make work.
	#print users()
	#print groups()

	print get_group( 'simmons-tech' ).immediate_members
	print get_group( 'simmons-tech' ).owner

	print hmac_message( "The quick brown fox jumps over the lazy dog", "someuser", "key" )

	print "\nTest @restricted.\n"
	super_secret( 'larsj', larsj_token, "TESTING TESTING" )
	print ""
	authd_echo( hmac_message( ["Testing","A","List"], 'adat', adat_token ) )
	print ""
	super_secret( 'timwilz', timwilz_token, "Psh. Simmons Tech." )
