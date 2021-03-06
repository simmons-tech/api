from flask import Flask
from werkzeug.wsgi import DispatcherMiddleware

from auth import app as auth_app
from buses import app as buses_app
from laundry import app as laundry_app
from packages import app as packages_app
from people import app as people_app
from profile import app as profile_app
from rooming_assignment import app as rooming_assignment_app
from officers import app as officers_app
#from rooms import app as rooms_app

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(
	app.wsgi_app,
	{
		'/auth':		auth_app,
		'/buses':		buses_app,
		'/laundry':		laundry_app,
		'/packages':		packages_app,
		'/people':		people_app,
		'/profile':		profile_app, # TODO: rename to profiles?
		'/rooming_assignment':	rooming_assignment_app, # TODO: rename to rooming_assignments?
		'/officers': officers_app,
#		'/rooms':		rooms_app,
	})

if __name__ == '__main__':
	app.run()
