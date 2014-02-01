from werkzeug.wsgi import DispatcherMiddleware
from auth import app as auth_app
from people import app as people_app

application = DispatcherMiddleware(
	auth_app,
	{
		'/people':	people_app,
	})
