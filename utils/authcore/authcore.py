# This is a work in progress, MVP implementation. Please do not assume it is secure, because it is not in pretty much literally every way imaginable.
# DO NOT DEPLOY THIS UNTIL IT HAS BEEN FIXED.
# The complete implementation will be based on 858 code, but will need to be modified to support SSO based on MIT certs.
#
# This file seeks to implement the back-end of the RPC described at
# https://github.com/simmons-tech/wiki/wiki/Authentication-API

## TEMP INIT
#

class User:
	def __init__( self, username, password):
		self.username = username
		self.password = password
		self.token = None

class Group:
	def __init__( self, groupname, owner ):
		self.groupname = groupname
		self.owner = owner
		self.immediate_members = set()
		self.subgroups = set()

users = {
	'admin': User( 'admin', 'password' )
}

accounts_admin = Group( 'accounts-admin', 'accounts-admin' )
accounts_admin.immediate_members = set([ 'admin' ])

groups = {
	'accounts-admin': accounts_admin
}

def type_of( name ):
	if name in users:
		return 'user'
	if name in groups:
		return 'group'
	return None

#def users():
#	return users.keys()
#
#def groups():
#	return groups.keys()

def is_user( name ):
	return type_of( name ) == 'user'

def is_group( name ):
	return type_of( name ) == 'group'

def is_owner( user, group ):
	assert is_group( group )
	assert is_user( user )
	if type_of( groups[ group ].owner ) == 'user':
		return groups[ group ].owner == user
	return is_member( user, group )

## HMAC ##
#
# MD5-HMAC code from Wikipedia.
# TODO: Audit properly.
# TODO: Move to own file.
#

from hashlib import md5

def HMAC( message, key ):

	trans_5C = ''.join( chr( x ^ 0x5c ) for x in xrange(256) )
	trans_36 = ''.join( chr( x ^ 0x36 ) for x in xrange(256) )
	blocksize = md5().block_size
		
	# Standardize the key...
	if len( key ) > blocksize:
		key = md5(key).digest()
	key += chr( 0 ) * ( blocksize - len( key ) )
	o_key_pad = key.translate( trans_5C )
	i_key_pad = key.translate( trans_36 )
	return md5( o_key_pad + md5( i_key_pad + message).digest() ).hexdigest()

## Temp Token Generation
#
#

import string
import random
def generate_new_token():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))

### Authentication

def authenticate( user, password ):
	assert is_user( user )
	assert users[user].password == password

	token = generate_new_token()
	users[user].token = token
	return token

def invalidate_token( user, token ):
	assert is_user( user )
	assert users[ user ].token != None
	assert users[ user ].token == token
	
	users[ user ].token = None

def validate_message( message, hmac, user ):
	assert is_user( user )
	assert users[ user ].token != None
	
	return hmac == HMAC( message, users[ user ].token )

def validate_token( user, token ):
	assert is_user( user )

	return users[ user ].token == token

### Membership

# TODO: Protect against loops? Maybe do that during registration.

def is_member( user, group ):
	assert is_user( user )
	assert is_group( group )
	# Inefficient, but simple.
	return user in members( group )

def members( group ):
	assert is_group( group )
	m = set()
	m = m | groups[ group ].immediate_members
	for subgroup in groups[group ].subgroups:
		m = m | members( subgroup )
	return m

def immediate_members( group ):
	assert is_group( group )
	return groups[ group ].immediate_members

def subgroups( group ):
	assert is_group( group )
	return groups[ group ].subgroups

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
# TODO: Make a variant for HMAC'd messages?
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
			else:
				assert True in approval

			f( *args, **kwargs )
		return decorated_f
	return restricted_decorator

### Account management

@restricted( "accounts-admin" )
def create_user( user, password ):
	assert type_of( user ) == None
	
	U = User( user, password )
	users[ user ] = U

@restricted( "accounts-admin" )
def create_group( group, owner = "accounts-admin" ):	
	assert type_of( group ) == None
	assert type_of( owner ) != None

	G = Group( group, owner )
	groups[ group ] = G

def add_to_group( admin_user, admin_token, name, group ):
	assert is_group( group )

	@restricted([ "accounts-admin", groups[group].owner ])
	def dangerous_code():
		assert type_of( name ) != None

		if type_of( name ) == 'user':
			groups[ group ].immediate_members.add( name )
		elif type_of( name ) == 'group':
			groups[ group ].subgroups.add( name )

	dangerous_code( admin_user, admin_token )

def remove_from_group( admin_user, admin_token, name, group ):
	assert is_group( group )
	
	@restricted([ "accounts-admin", groups[group].owner ])
	def dangerous_code():
		assert type_of( name ) != None

		if type_of( name ) == 'user':
			groups[ group ].immediate_members.remove( name )
		elif type_of( name ) == 'group':
			groups[ group ].subgroups.remove( name )



def transfer_group_ownership( admin_user, admin_token, group, new_owner ):
	assert is_group( group )
	
	@restricted([ "accounts-admin", groups[group].owner ])
	def dangerous_code():
		assert type_of( new_owner ) != None
		groups[ group ].owner = new_owner

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

	add_to_group( 'larsj', larsj_token, 'woursler', 'simmons-tech' )
	add_to_group( 'admin', admin_token, 'adat', 'simmons-tech' )
	add_to_group( 'larsj', larsj_token, 'larsj', 'simmons-tech' )

	transfer_group_ownership( 'larsj', larsj_token, 'simmons-tech', 'adat' )

	adat_token = authenticate( 'adat', 'password3' )

	add_to_group( 'adat', adat_token, 'omalley1', 'simmons-tech' )

	print users.keys()
	print groups.keys()

	print groups[ 'simmons-tech' ].immediate_members
	print groups[ 'simmons-tech' ].owner

	print HMAC( "The quick brown fox jumps over the lazy dog", "key" )

	print "\nTest @restricted.\n"
	super_secret( 'larsj', larsj_token, "TESTING TESTING" )
	print ""
	super_secret( 'timwilz', timwilz_token, "Psh. Simmons Tech." )
