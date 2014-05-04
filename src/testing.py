import utils.authentication_core as authentication
import utils.authorization_core as authorization

admin_token = authentication.authenticate( 'admin', 'password' )
woursler_token = authentication.authenticate( 'woursler', 'password2' )
adat_token = authentication.authenticate( 'adat', 'password3' )
larsj_token = authentication.authenticate( 'larsj', 'password4' )
timwilz_token = authentication.authenticate( 'timwilz', 'password6' )

print admin_token, larsj_token, timwilz_token, adat_token

print authentication.HMAC.encode( 'The quick brown fox jumps over the lazy dog', 'admin', admin_token )

print authorization.members( 'simmons-tech' )

print authorization.is_member( 'woursler', 'simmons-tech' )
print authorization.immediate_members( 'simmons-tech' )
s_t_owner = authorization.owner( 'simmons-tech' )

if s_t_owner == 'larsj':
	authorization.transfer_group_ownership( 'larsj', larsj_token, 'simmons-tech', 'adat' )
else:
	authorization.transfer_group_ownership( 'adat', adat_token, 'simmons-tech', 'larsj' )

print s_t_owner + '\n\n\n'
@authorization.restricted( "simmons-tech" )
def super_secret( s ):
	print "Welcome to Simmons Tech. Your string is: " + s

@authorization.authenticate_message( "simmons-tech" )
def authd_echo( message ):
	print message


print "\nTest @restricted.\n"
super_secret( 'larsj', larsj_token, "TESTING TESTING" )
authd_echo( authentication.HMAC.encode( ["Testing","A","List"], 'adat', adat_token ) )
try:
	super_secret( 'timwilz', timwilz_token, "Psh. Simmons Tech." )
except:
	print "Successful interception of trolling."
