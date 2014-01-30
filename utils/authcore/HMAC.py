# TODO: Audit properly.
from hashlib import md5
import json

def HMAC( message, key ):

	trans_5C = ''.join( chr( x ^ 0x5c ) for x in xrange(256) )
	trans_36 = ''.join( chr( x ^ 0x36 ) for x in xrange(256) )
	blocksize = md5().block_size
	
	# Standardize the key...
	key = str( key )
	if len( key ) > blocksize:
		key = md5(key).digest()
	key += chr( 0 ) * ( blocksize - len( key ) )

	o_key_pad = key.translate( trans_5C )
	i_key_pad = key.translate( trans_36 )
	return md5( o_key_pad + md5( i_key_pad + message ).digest() ).hexdigest()

# Need to carefully work on this and then make a JS equivalent.
def hmac_message( message, user, key ):
	message = json.dumps( message )
	return {
		'message': message,
		'user':user,
		'hmac': HMAC( message, key ),
	}
