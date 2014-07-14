# The Simmons API

This file was autogenerated from the `apis.yaml` description of the https://github.com/simmons-tech/api repository. 


## rooms module

Provides data about the physical characteristics of Simmons rooms.


### get_all

URL: `http://simapi.xvm.mit.edu/rooms/`

Python: `get_all(  )`

Javascript: `get_all: function( callback )`

Returns a list of all rooms.


### get_room

URL: `http://simapi.xvm.mit.edu/rooms/<roomnum>/`

Python: `get_room( roomnum )`

Javascript: `get_room: function( roomnum, callback )`

Returns all data for a specific room.



## rooming_assignment module

Provides information about the mapping between residents and the rooms where they live. Historical data is planned.


### get_room_by_person

URL: `http://simapi.xvm.mit.edu/rooming_assignment/person/<username>/`

Python: `get_room_by_person( username )`

Javascript: `get_room_by_person: function( username, callback )`

Returns the room that the given person is currently living in.


### get_people_by_room

URL: `http://simapi.xvm.mit.edu/rooming_assignment/room/<roomnum>/`

Python: `get_people_by_room( roomnum )`

Javascript: `get_people_by_room: function( roomnum, callback )`

Returns the people that currently reside in the given room.



## people module

Provides identity-related data about the residents of Simmons.


### get_all

URL: `http://simapi.xvm.mit.edu/people/`

Python: `get_all(  )`

Javascript: `get_all: function( callback )`

Returns a list of all current residents' usernames


### get_person

URL: `http://simapi.xvm.mit.edu/people/<username>/`

Python: `get_person( username )`

Javascript: `get_person: function( username, callback )`

Returns all data on a specific resident.


### query

URL: `http://simapi.xvm.mit.edu/people/?q=<query>`

Python: `query( query )`

Javascript: `query: function( query, callback )`

Returns the usernames matching the passed query. To match a query, a user has to have each space seperated token (querylet) as part of its special fields. The special fields are 'kerberos', 'firstname', and 'lastname'. Matches are case insenstive.



## profiles module

Provides more personal information about the residents of Simmons.


### get_profile

URL: `http://simapi.xvm.mit.edu/profile/<username>/`

Python: `get_profile( username )`

Javascript: `get_profile: function( username, callback )`

Returns a resident profile.



## laundry module

Provides information on the current state of laundry machines in the building.


### get_raw

URL: `http://simapi.xvm.mit.edu/laundry/`

Python: `get_raw(  )`

Javascript: `get_raw: function( callback )`

Returns a raw dump of all avalible information on the laundry. Stopgap until a better API is enacted.



## buses module

Provides information on the current state of buses coming to Simmons.


### get_raw

URL: `http://simapi.xvm.mit.edu/buses/`

Python: `get_raw(  )`

Javascript: `get_raw: function( callback )`

Returns a raw dump of all avalible information on buses. Stopgap until a better API is enacted.



## packages module

Provides information about who has packages.


### get_raw

URL: `http://simapi.xvm.mit.edu/packages/`

Python: `get_raw(  )`

Javascript: `get_raw: function( callback )`

Returns a dump object with attrs that are usernames, and values that are numbers of packages.


### get_packages_for_user

URL: `http://simapi.xvm.mit.edu/packages/<username>/`

Python: `get_packages_for_user( username )`

Javascript: `get_packages_for_user: function( username, callback )`

Get the number of packages the given user has.

