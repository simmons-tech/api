#!/usr/bin/env python

import yaml
import jinja2

templateLoader = jinja2.FileSystemLoader( searchpath="templates/" )
templateEnv = jinja2.Environment( loader=templateLoader )

with open("apis.yaml", 'r') as stream:
	apis = yaml.load(stream)

server_path = 'http://localhost:5000/'

#TODO: Must be a more elegant way to do this.
def url_replace( s ):
	r = '"'
	for c in s:
		if c == "<" :
			r += '"+'
		elif c == ">" :
			r += '+"'
		else:
			r += c
	r += '"'
	return r

###
#
# Javascript
#
###

with open('stubs/javascript/simmons-api.js', 'w') as f:
	template = templateEnv.get_template( 'stubs.js' )
	f.write( template.render( apis = apis, server_path = server_path , f = url_replace ) )

###
#
# Python
#
###

with open('stubs/python/simmons_api/__init__.py', 'w') as f:
	template = templateEnv.get_template( '__init__.py' )
	f.write( template.render( apis = apis, server_path = server_path , f = url_replace ) )

with open('stubs/python/simmons_api/__common.py', 'w') as f:
	template = templateEnv.get_template( '__common.py' )
	f.write( template.render( apis = apis, server_path = server_path , f = url_replace ) )

for api in apis:
	with open('stubs/python/simmons_api/' + api['name'] + '.py', 'w') as f:
		template = templateEnv.get_template( 'module.py' )
		f.write( template.render( api = api, f = url_replace ) )
