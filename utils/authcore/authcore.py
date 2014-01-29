# This is a work in progress, MVP implementation. Please do not assume it is secure, because it is not.
# DO NOT DEPLOY THIS UNTIL IT HAS BEEN FIXED.
# The complete implementation will be based on 858 code, but will need to be modified to aupport SSO.
#
# This file seeks to implement the backend of the RPC described at
# https://github.com/simmons-tech/wiki/wiki/Authentication-API

# TODO: move user in users type asserts over to something functional to facilitate backups.

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
	assert user in users
	assert users[user].password == password

	token = generate_new_token()
	users[user].token = token
	return token

def invalidate_token( user, token ):
	assert user in users
	assert users[ user ].token != None
	assert users[ user ].token == token
	
	users[ user ].token = None

def validate_message( message, hmac, user ):
	assert user in users
	assert users[ user ].token != None
	
	return hmac == HMAC( message, users[ user ].token )

def validate_token( user, token ):
	assert user in users

	return users[ user ].token == token

### Membership

def is_member( user, group ):
	assert user in users
	assert group in groups
	# Inefficient, but simple.
	return user in members( group )

def members( group ):
	assert group in groups
	m = set()
	m = m | groups[ group ].immediate_members
	for subgroup in groups[ group ].subgroups:
		m = m | members( subgroup )
	return m

def immediate_members( group ):
	assert group in groups
	return groups[ group ].immediate_members

def subgroups( group ):
	assert group in groups
	return groups[ group ].subgroups

### Account managment

def create_user( user, password, admin_user, admin_token ):
	assert validate_token( admin_user, admin_token )
	assert is_member( admin_user, "accounts-admin" )

	assert user not in users
	assert user not in groups
	U = User( user, password )
	users[ user ] = U

def create_group( group, admin_user, admin_token, owner = "accounts-admin" ):
	assert validate_token( admin_user, admin_token )
	assert is_member( admin_user, "accounts-admin" )
	
	assert group not in users
	assert group not in groups
	G = Group( group, owner )
	groups[ group ] = G

def add_to_group( name, group, admin_user, admin_token ):
	pass

def remove_from_group( name, group, admin_user, admin_token ):
	pass

def transfer_group_ownership( group, new_owner, admin_user, admin_token ):
	pass
	

### __main__
if __name__ == '__main__':

	admin_token = authenticate( 'admin', 'password' )
	print admin_token
	create_user( 'woursler', 'password2', 'admin', admin_token )

	print users
	print groups

	print HMAC( "The quick brown fox jumps over the lazy dog", "key" )
