import sys
import os


# Load the sdb password from file.
password = None

try:
	# Construct a reliable location, should be reasonably cross platform.
	__location__ = os.path.realpath( os.path.join( os.getcwd(), os.path.dirname( __file__ ) ) )
	with open( os.path.join( __location__, 'password' ), 'r' ) as password_file:
		password = password_file.read().strip()
except IOError:
	sys.stderr.write('sdb.py:  Unable to open password file; most likely {{apis_dir}}/utils/sdb/password does not exist.\n')
	exit()

try:
	assert password != None
	assert password != ''
except AssertionError:
	sys.stderr.write('sdp.py: Empty password detected. Make sure the password is in {{apis_dir}}/utils/sdb/password.\n')
	exit()

print 'Password is "' + password +'"'

db = create_engine('postgresql://dashboard:'+password+'@simmons.mit.edu/sdb')
