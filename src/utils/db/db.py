#!/usr/bin/python
from sqlalchemy import *
from sqlalchemy.orm import *z
from sqlalchemy.ext.declarative import *
import os

# TODO: Create a way to specify these definitions everywhere, have the db module work on them.
# Decorators are the power of the hour, perhaps decorated classes?

UserBase = declarative_base()
GroupBase = declarative_base()
RoomsBase = declarative_base()

class User(UserBase):
	__tablename__= "user"
	username = Column(String(128), primary_key=True)
	passhash = Column(String(128))
	token = Column(String(128))
	salt = Column(String(128))

class Group(GroupBase):
	__tablename__= "group"
	groupname = Column(String(128), primary_key=True)
	owner = Column(String(128))
	immediate_members = Column(String(512))
	subgroups = Column(String(512))

class Rooms(RoomsBase):
	__tablename__ = "rooms"
	num = Column(String, primary_key=True)
	grt = Column(String)
	capacity = Column(String)
	size = Column(String)
	view = Column(String)
	X = Column(Integer)
	Y = Column(Integer)
	hasCurvyWall = Column(String)
	bathroom = Column(String)

class Section(RoomsBase):
	__tablename__ = "sections"
	label = Column(String, primary_key=True)

def dbsetup(name, base):
	thisdir = os.path.dirname(os.path.abspath(__file__))
	dbdir   = os.path.join(thisdir, 'db', name)
	if not os.path.exists(dbdir):
		os.makedirs(dbdir)
	dbfile  = os.path.join(dbdir, '%s.db' % name)
	engine  = create_engine('sqlite:///%s' % dbfile)
	base.metadata.create_all(engine)
	session = sessionmaker(bind=engine)
	return session()

def init( tablename ):
	return dbsetup( tablename, globals()[tablename.title() + 'Base'] )

if __name__ == '__main__':

	commands = [ 'init' ]
	tablenames = [ 'user', 'group' ]

	def CLIformat(l):
		s = '['
		for x in l:
			s += str(x)
			s += '|'
		return s[:-1]+']'
	
	import sys
	if len(sys.argv) != 3:
		print 'Usage: %s %s %s' % (sys.argv[0], CLIformat(commands), CLIformat(tablenames))
		exit(1)
	
	command = sys.argv[1].strip()
	tablename = sys.argv[2].strip()
	
	if command in commands:
		if tablename in tablenames:
			globals()[command](tablename)
		else:
			raise Exception('Unknown table: %s' % tablename)
	else:
		raise Exception('Unknown command: %s' % command)
