# TODO: Audit properly.
from hashlib import md5
import json

def JSONify( obj ):
	if isinstance( obj, basestring ):
		try:
			return json.dumps( json.loads( obj ) )
		except:
			pass
	return json.dumps( obj )

def unJSONify( string ):
	return json.loads( string )

def HMAC( message, key ):

	trans_5C = ''.join( chr( x ^ 0x5c ) for x in xrange(256) )
	trans_36 = ''.join( chr( x ^ 0x36 ) for x in xrange(256) )
	blocksize = md5().block_size

	message = JSONify(message)
		
	# Standardize the key...
	if len( key ) > blocksize:
		key = md5(key).digest()
	key += chr( 0 ) * ( blocksize - len( key ) )

	o_key_pad = key.translate( trans_5C )
	i_key_pad = key.translate( trans_36 )
	return md5( o_key_pad + md5( i_key_pad + message ).digest() ).hexdigest()

def authenticate( message, user, key ):
	return json.dumps({
		'message':message,
		'user':user,
		'hmac': HMAC( message, key ),
	})
