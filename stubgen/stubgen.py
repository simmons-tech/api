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

with open('stubs/python/simmons-api.py', 'w') as f:
	template = templateEnv.get_template( 'stubs.py' )
	f.write( template.render( apis = apis, server_path = server_path , f = url_replace ) )
	
