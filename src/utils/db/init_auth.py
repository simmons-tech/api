import base64
import pbkdf2
import os
import json

from db import *

# TODO: init_users
# TODO init_groups

user_db = init('user')
user = user_db.query(User).get( 'admin' )
if user:
	exit() # TODO: Shouldn't exit because other stuff runs below.
newuser = User()
newuser.username = 'admin'
newuser.salt = base64.b64encode( os.urandom(128) )
newuser.passhash = pbkdf2.PBKDF2( 'password', newuser.salt ).hexread(32)
user_db.add( newuser )
user_db.commit()

group_db = init('group')
group = group_db.query(Group).get( 'accounts-admin' )
if group:
	exit()
newgroup = Group()
newgroup.groupname = 'accounts-admin'
newgroup.owner = 'accounts-admin'
newgroup.immediate_members = json.dumps(['admin'])
newgroup.subgroups = json.dumps([])
group_db.add( newgroup )
group_db.commit()
