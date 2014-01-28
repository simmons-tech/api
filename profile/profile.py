#!/usr/bin/python

from flask import Flask, render_template
app = Flask(__name__)

# BEGIN HELPERS ###########################################

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

password = 'PASSWORD_HERE'

def get_people():
	print "CALL: get_people"
	db = create_engine('postgresql://dashboard:'+password+'@simmons.mit.edu/sdb')

	Base = declarative_base()

	class Resident(Base):
		__tablename__ = 'directory'
		username = Column(String, primary_key = True)

		firstname = Column(String)
		lastname = Column(String)
		room = Column(String)
		phone = Column(String)
		year = Column(Integer)
		cellphone = Column(String)
		homepage = Column(String)
		#home_city = Column(String)
		#home_state = Column(String)
		home_country = Column(String)
		#quote = Column(String)
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

	Session = sessionmaker(bind=db)
	session = Session()

	# Make a full list of people of interest...
	people = []
	for person in session.query(Resident):
		if person.private:
			continue
		people.append( {
			'kerberos'	:person.username,
			'firstname'	:person.firstname,
			'lastname'	:person.lastname,
			'room'		:person.room,
			'year'		:person.year,
			'title'		:person.title,
			'email'		:person.email,
			} )

		
	session.close()

	return people

def get_person( username ):
	print "CALL: get_person"
	people = get_people()
	for person in people:
		if person['kerberos'] == username:
			return HttpResponse(json.dumps({'person':person}), mimetype="application/json")

def get_active_residents():
	print "CALL: get_active_residents"

	db = create_engine('postgresql://dashboard:'+password+'@simmons.mit.edu/sdb')

	Base = declarative_base()

	class ActiveUsernames( Base ):
		__tablename__ = 'sds_users_all'
	
		username = Column( String, primary_key = True )
		active = Column( Boolean )

	Session = sessionmaker(bind=db)
	session = Session()

	people = get_people()
	
	# Figure out which users are active...
	active = {}
	for username in session.query(ActiveUsernames):
		active[ username.username ] = username.active

	usernames = []
	for person in people:
		if active[ person['kerberos'] ]:
			usernames.append( person['kerberos'] )

	return HttpResponse(json.dumps({'usernames':usernames}), mimetype="application/json")

# END HELPERS #############################################

# BEGIN API ###############################################

@app.route('/')
def serve_active_residents():
	print "CALL: serve_active_residents"
	return render_template('residents.json', residents = get_active_residents() )

@app.route('/<username>/')
def serve_person( username ):
	print "CALL: serve_person"
	return render_template('review.json', resident = get_person( username ) )

# END API #################################################

# RUN FLASK APP ###########################################

if __name__ == "__main__":
	app.debug = True # TODO: Remove in production.
    	app.run()

# END FLASK APP ###########################################
