// SIMMONS API CLIENT STUBS FOR JAVASCRIPT
// This code was auto-generated by stubgen.py
// DO NOT EDIT IT BY HAND. Edit apis.yaml instead.
// This will ensure that changes are reflected in other
// languages stubs.

function getJSONP(url, success) {

    var ud = '_' + +new Date,
        script = document.createElement('script'),
        head = document.getElementsByTagName('head')[0] 
               || document.documentElement;

    window[ud] = function(data) {
        head.removeChild(script);
        success && success(data);
    };

    script.src = url.replace('callback=?', 'callback=' + ud);
    head.appendChild(script);

}

getJSONP('http://localhost:5000/people/', function(data){
    console.log(data);
});

this.RPC_call = function( path ) {
	console.log( "http://localhost:5000/" + path );
	var wtf = $.getJSON(
		"http://localhost:5000/" + path,
		function() { console.log( wtf.responseJSON ); }
	).fail( function(d, textStatus, error) {
        console.error("getJSON failed, status: " + textStatus + ", error: "+error)
    });
	//print 'tried to call to http://localhost:5000/' + path;
	return "";
}


// Beginning stubs for rooms:
// Provides data about the physical characteristics of Simmons rooms.
this.rooms = {
	
	// Returns a list of all rooms.
	get_all: function(  ) {
		return RPC_call( "rooms/" );
	},

	// Returns all data for a specific room.
	get_room: function( roomnum ) {
		return RPC_call( "rooms/"+roomnum+"/" );
	}
}; // End of stubs for rooms

// Beginning stubs for people:
// Provides identity-related data about the residents of Simmons residents.
this.people = {
	
	// Returns a list of all current residents' usernames
	get_all: function(  ) {
		return RPC_call( "people/" );
	},

	// Returns all data on a specific resident.
	get_person: function( username ) {
		return RPC_call( "people/"+username+"/" );
	},

	// Returns the usernames matching the passed query. To match a query, a user has to have each space seperated token (querylet) as part of its special fields. The special fields are 'kerberos', 'firstname', and 'lastname'. Matches are case insenstive.
	query: function( query ) {
		return RPC_call( "people/?q="+query+"" );
	}
}; // End of stubs for people
