# This is a work in progress, MVP implementation. Please do not assume it is secure, because it is not in pretty much literally every way imagininable.
# DO NOT DEPLOY THIS UNTIL IT HAS BEEN FIXED.
# The complete implementation will be based on 858 code, but will need to be modified to aupport SSO based on MIT certs.
#
# This file seeks to implement the backend of the RPC described at
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

# TODO: Protect against loops.

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

### Account managment

def create_user( user, password, admin_user, admin_token ):
	# Pre-permissions sanity check.
	assert is_user( admin_user )

	# Permissions Check.
	assert validate_token( admin_user, admin_token )
	assert is_member( admin_user, "accounts-admin" )

	# Post-pemissions sanity check.	
	assert type_of( name ) == None
	assert type_of( owner ) != None

	U = User( user, password )
	users[ user ] = U

def create_group( group, admin_user, admin_token, owner = "accounts-admin" ):
	# Pre-permissions sanity check.
	assert is_user( admin_user )

	# Permissions Check.
	assert validate_token( admin_user, admin_token )
	assert is_member( admin_user, "accounts-admin" )

	# Post-pemissions sanity check.	
	assert type_of( name ) == None
	assert type_of( owner ) != None

	# Action.
	G = Group( group, owner )
	groups[ group ] = G

def add_to_group( name, group, admin_user, admin_token ):
	assert is_group( group )
	assert is_user( admin_user )

	assert validate_token( admin_user, admin_token )
	assert is_owner( admin_user, group ) or is_member( admin_user, "accounts-admin" )

	assert type_of( name ) != None

	if type_of( name ) == 'user':
		groups[ group ].immediate_members.add( name )
	elif type_of( name ) == 'group':
		groups[ group ].subgroups.add( name )

def remove_from_group( name, group, admin_user, admin_token ):
	assert is_group( group )
	assert is_user( admin_user )

	assert validate_token( admin_user, admin_token )
	assert is_owner( admin_user, group ) or is_member( admin_user, "accounts-admin" )

	assert type_of( name ) != None

	if type_of( name ) == 'user':
		groups[ group ].immediate_members.remove( name )
	elif type_of( name ) == 'group':
		groups[ group ].subgroups.remove( name )

def transfer_group_ownership( group, new_owner, admin_user, admin_token ):
	assert is_group( group )
	assert is_user(  admin_user )

	assert validate_token( admin_user, admin_token )
	assert is_owner( admin_user, group ) or is_member( admin_user, "accounts-admin" )

	assert type_of( new_owner ) != None
	groups[ group ].owner = new_owner
	

### __main__
if __name__ == '__main__':

	admin_token = authenticate( 'admin', 'password' )

	create_user( 'woursler', 'password2', 'admin', admin_token )
	create_user( 'adat', 'password3', 'admin', admin_token )
	create_user( 'larsj', 'password4', 'admin', admin_token )

	larsj_token = authenticate( 'larsj', 'password4' )

	create_group( 'simmons-tech', 'admin', admin_token, 'larsj' )

	add_to_group( 'woursler', 'simmons-tech', 'larsj', larsj_token )
	add_to_group( 'adat', 'simmons-tech', 'admin', admin_token )
	add_to_group( 'larsj', 'simmons-tech', 'larsj', larsj_token )

	print users.keys()
	print groups.keys()

	print groups[ 'simmons-tech' ].immediate_members
	print groups[ 'simmons-tech' ].owner

	print HMAC( "The quick brown fox jumps over the lazy dog", "key" )
