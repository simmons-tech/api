class AuthorizationError(Exception):
	def __init__(self, username):
		self.username = username
	def __str__(self):
		return 'Unable to authorize ' + str(username) + '. Credentials were incorrect or insufficient.'
	def __repr__(self):
		return str( self )

class NonexistentGroupError(Exception):
	def __init__(self, groupname):
		self.groupname = groupname
	def __str__(self):
		return str(groupname) + 'is not a group.'
	def __repr__(self):
		return str( self )

class GroupAllocatedError(Exception):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return str(name) + 'is already allocated in authcore.'
	def __repr__(self):
		return str( self )
