#!/usr/bin/env python

import yaml

#TODO Jinja2 Templating.

stream = open("apis.yaml", 'r')
apis = yaml.load(stream)

print 'Generating client python stubs. These stubs are standalone.'

hostpath = 'http://localhost:5000/'

for api in apis:
	print api['name'],'-',api['desc']
	for method in api['fxns']:
		print '\t*', method['name'] + str( tuple(method['args']) ),'-', api['path'] + method['path']
		print '\t\t', method['desc']
	
