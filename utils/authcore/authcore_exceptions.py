class AuthenticationError(Exception):
	def __init__(self, username):
		self.username = username
	def __str__(self):
		return 'Unable to authenticate ' + str(username) + '. Credentials were incorrect or insufficient.'
	def __repr__(self):
		return str( self )

class NonexistentNameError(Exception):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return str(name) + 'is not a registered authcore name.'
	def __repr__(self):
		return str( self )

class NonexistentUserError(Exception):
	def __init__(self, username):
		self.username = username
	def __str__(self):
		return str(username) + 'is not a user.'
	def __repr__(self):
		return str( self )

class NonexistentGroupError(Exception):
	def __init__(self, groupname):
		self.groupname = groupname
	def __str__(self):
		return str(groupname) + 'is not a group.'
	def __repr__(self):
		return str( self )

class NameAllocatedError(Exception):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return str(name) + 'is already allocated in authcore.'
	def __repr__(self):
		return str( self )
