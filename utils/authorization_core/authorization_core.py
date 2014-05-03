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
import authentication_core
import db

# Local imports
from authorization_exceptions import *

def is_group( name ):
	group_db = db.init('group')
	group = group_db.query(db.Group).get( name )
	if group:
		return True
	return False

def get_group( groupname ):
	if not is_group( groupname ):
		raise NonexistentGroupError( groupname )
	group_db = db.init('group')
	group = group_db.query(db.Group).get( groupname )
	return group

#TODO: Make work.
def is_owner( username, groupname ):
	if not authentication_core.is_user( username ):
		raise authentication_core.NonexistentUserError( username )
	if not is_group( groupname ):
		raise NonexistentGroupError( groupname )

	if authentication_core.is_user( owner( groupname ) ):
		return get_group( groupname ).owner == user
	return is_member( username, groupname )

### Membership

# TODO: Protect against loops? Maybe do that during registration.

def is_member( username, groupname ):
	if not authentication_core.is_user( username ):
		raise authentication_core.NonexistentUserError( username )
	if not is_group( groupname ):
		raise NonexistentGroupError( groupname )
	# Inefficient, but simple.
	return username in members( groupname )

def members( groupname ):
	group = get_group( groupname )
	if not group:
		raise NonexistentGroupError( groupname )
	m = set()
	m = m | set( json.loads( get_group( groupname ).immediate_members ) )
	for subgroup in json.loads( get_group( groupname ).subgroups ):
		m = m | members( subgroup )
	return m

# TODO: Make this work.
def immediate_members( groupname ):
	group = get_group( groupname )
	if not group:
		raise NonexistentGroupError( groupname )
	return group.immediate_members

# TODO: Make this work.
def subgroups( groupname ):
	group = get_group( groupname )
	if not group:
		raise NonexistentGroupError( groupname )
	return group.subgroups

def owner( groupname ):
	group = get_group( groupname )
	if not group:
		raise NonexistentGroupError( groupname )
	return group.owner

### restricted decorator ###
#
# A key part of the authcore; allows for easy use of the auth module in other APIs.
#
# When applied to a function, it integrates with the authentication module.
# For now, this does mean that it changes the function header slightly.
#
# f( x1, x2, ... ) -> f( user, token, x1, x2, ... )
#
# To restrict a function f to either (group) 'simmons-tech', (group) 'accounts-admin', or (user) 'woursler':
#
## @restricted([ 'simmons-tech', 'accounts-admin', 'woursler' ])
## def f( x1, x2 ):
## 	dangerous_stuff_here
#
# There is an additional argument require_all. If set to true, the user must match every constraint passed
# in the list.
#
# i.e. @restricted([ 'simmons-tech', 'accounts-admin' ]) restricts usage to people who are in both groups
# (as opposed to just one or the other).
#
# See the Wiki article on /auth/ for more details on usage and security guarantees.
#
# TL;DR, this decorator is for convenience and does not provide security against an
# adversary with code execution over your relevant environment.
#
###

def restricted( names, require_all = False ):
	# Support passing a single name.
	if isinstance( names, basestring ):
		names = [ names ]
	def restricted_decorator( f ):
		def decorated_f( username, token, *args, **kwargs ):
			# Pre-permissions sanity check.
			if not authentication_core.is_user( username ):
				raise authentication_core.NonexistentUserError( username )
			for name in names:
				assert authentication_core.is_user( name ) or is_group( name )

			# Permissions Check.
			# Validate that the user requesting access is who they say they are.
			authentication_core.validate_token( username, token )
			# For each name, check membership.
			approval = set()
			for name in names:
				if authentication_core.is_user( name ):
					approval.add( name == username )
				if is_group( name ):
					approval.add( is_member( username, name ) )
			
			if require_all and ( False in approval ):
				raise AuthorizationError( username )
			if True not in approval:
				raise AuthorizationError( username )

			return f( *args, **kwargs )
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
			username    = authenticated_message[ 'username' ]
			message = authenticated_message[ 'message' ]

			# Pre-permissions sanity check.
			if not authentication_core.is_user( username ):
				raise authentication_core.NonexistentUserError( username )
			for name in names:
				assert authentication_core.is_user( name ) or is_group( name )
			
			# Ensure the message is from the user.
			authentication_core.validate_message( authenticated_message )
			# For each name, check membership.
			approval = set()
			for name in names:
				if authentication_core.is_user( name ):
					approval.add( name == username )
				if is_group( name ):
					approval.add( is_member( username, name ) )

			if require_all and ( False in approval ):
				raise AuthorizationError( username )
			if True not in approval:
				raise AuthorizationError( username )
			
			return f( json.loads( message ) )
		return decorated_f
	return authenticate_message_decorator	

### Account management
@restricted( 'accounts-admin' )
def create_group( groupname, owner = 'accounts-admin' ):	
	assert not ( authentication_core.is_user( groupname ) or is_group( groupname ) )
	assert authentication_core.is_user( owner ) or is_group( owner )

	group_db = db.init('group')
	group = group_db.query(Group).get( groupname )
	if group:
		return None
	newgroup = db.Group()
	newgroup.groupname = groupname
	newgroup.owner = owner
	newgroup.immediate_members = json.dumps([])
	newgroup.subgroups = json.dumps([])
	group_db.add(newgroup)
	group_db.commit()

def add_to_group( admin_user, admin_token, name, groupname ):
	if not is_group( groupname ):
		raise NonexistentGroupError( groupname )

	@restricted([ 'accounts-admin', get_group( groupname ).owner ])
	def dangerous_code():
		if type_of( name ) == None:
			raise NonexistentNameError( name )

		group_db = db.init('group')
		group = group_db.query(db.Group).get( groupname )

		if type_of( name ) == 'user':
			immediate_members = set( json.loads( group.immediate_members ) )
			immediate_members.add( name )
			group.immediate_members = json.dumps( list( immediate_members ) )
		elif type_of( name ) == 'group':
			subgroups = set( json.loads( group.subgroups ) )
			subgroups.add( name )
			group.subgroups = json.dumps( list( subgroups ) )
		group_db.commit()

	dangerous_code( admin_user, admin_token )

def remove_from_group( admin_user, admin_token, name, groupname ):
	if not is_group( groupname ):
		raise NonexistentGroupError( groupname )
	
	@restricted([ 'accounts-admin', get_group( groupname ).owner ])
	def dangerous_code():
		assert authentication_core.is_user( name ) or is_group( name )

		group_db = db.init('group')
		group = group_db.query(db.Group).get( groupname )

		if authentication_core.is_user( name ):
			immediate_members = set( json.loads( group.immediate_members ) )
			immediate_members.remove( name )
			group.immediate_members = json.dumps( list( immediate_members ) )
		elif is_group( name ):
			subgroups = set( json.loads( group.subgroups ) )
			subgroups.remove( name )
			group.subgroups = json.dumps( list( subgroups ) )
		group_db.commit()



def transfer_group_ownership( admin_user, admin_token, groupname, new_owner ):
	assert is_group( groupname )
	
	@restricted([ 'accounts-admin', owner( groupname ) ])
	def dangerous_code():
		# TODO, support user types.
		assert authentication_core.is_user( new_owner ) or is_group( new_owner )
		group_db = db.init('group')
		group = group_db.query(db.Group).get( groupname )
		group.owner = new_owner
		group_db.commit()

	dangerous_code( admin_user, admin_token )

