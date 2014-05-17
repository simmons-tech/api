#!/usr/bin/env python

import yaml

#TODO Jinja2 Templating.

stream = open("apis.yaml", 'r')
apis = yaml.load(stream)

print 'Generating client python stubs. These stubs are standalone.'

server_path = 'http://localhost:5000/'

for api in apis:
	print api['name'],'-',api['desc']
	for method in api['fxns']:
		print '\t*', method['name'] + str( tuple(method['args']) ),'-', server_path + api['path'] + method['path']
		print '\t\t', method['desc']

#TODO: Must be a more elegant way to do this.
def python_replace( s ):
	r = '\''
	for c in s:
		if c == "<" :
			r += '\'+'
		elif c == ">" :
			r += '+\''
		else:
			r += c
	r += '\''
	return r
			

import jinja2

templateLoader = jinja2.FileSystemLoader( searchpath="" )
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "stubs.py"
template = templateEnv.get_template( TEMPLATE_FILE )

# Here we add a new input variable containing a list.
# Its contents will be expanded in the HTML as a unordered list.

outputText = template.render( apis = apis, server_path = server_path , f = python_replace)

print outputText
	
