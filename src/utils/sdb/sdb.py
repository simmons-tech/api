import sys
import os

# TODO: Assess need for each import.
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


# Load the sdb password from file.
password = None

try:
	# Construct a reliable location of the directory containing password file, should be reasonably cross platform.
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

db = create_engine('postgresql://dashboard:'+password+'@simmons.mit.edu/sdb')

# TODO: Check the password is correct.

def sdb_session():
	Session = sessionmaker(bind=db)
	session = Session()
	return session

ResidentBase = declarative_base()
ActiveUsernamesBase = declarative_base()
PackageBase = declarative_base()
OfficersBase = declarative_base()

class Resident(ResidentBase):
	__tablename__ = 'directory'
	username = Column(String, primary_key = True)

	firstname = Column(String)
	lastname = Column(String)
	room = Column(String)
	phone = Column(String)
	year = Column(Integer)
	cellphone = Column(String)
	homepage = Column(String)
	home_city = Column(String)
	home_state = Column(String)
	home_country = Column(String)
	quote = Column(String)
	favorite_category = Column(String)
	favorite_value = Column(String)
	private = Column(Boolean)
	type = Column(String)
	email = Column(String)
	lounge = Column(String)
	title = Column(String)
	loungevalue = Column(Integer)
	showreminders = Column(Boolean)
	guest_list_expiration = Column(String)

class ActiveUsernames( ActiveUsernamesBase ):
	__tablename__ = 'sds_users_all'

	username = Column( String, primary_key = True )
	active = Column( Boolean )

class Package(PackageBase):
	__tablename__ = 'packages'

	packageid         = Column(Integer, primary_key=True)
	recipient         = Column(String)
	bin                 = Column(String)
	checkin         = Column(Date)
	checkin_by         = Column(String)
	pickup                 = Column(Date)
	pickup_by         = Column(String)
	perishable         = Column(Boolean)

class Officers(OfficersBase):
	__tablename__ = 'officers'

	officerid = Column(Integer, primary_key=True)
	username = Column(String)
	position = Column(String)
	ordering = Column(Integer)
	created = Column(Date)
	removed = Column(Date)
