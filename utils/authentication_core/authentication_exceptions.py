class AuthenticationError(Exception):
	def __init__(self, username):
		self.username = username
	def __str__(self):
		return 'Unable to authenticate ' + str(username) + '. Credentials were incorrect or insufficient.'
	def __repr__(self):
		return str( self )

class NonexistentUserError(Exception):
	def __init__(self, username):
		self.username = username
	def __str__(self):
		return str(username) + 'is not a username.'
	def __repr__(self):
		return str( self )

class UserAllocatedError(Exception):
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return str(name) + 'is already an allocated username.'
	def __repr__(self):
		return str( self )
