# I made this for Ubuntu 13.04 Linux. I've tried to keep it cross platform, but I may not have succeeded.
# Let me know. ~woursler
all: clean init-db populate-db

init-db:
	# Initialize database files.
	@# Run db.py init for each table.
	@# TODO: Wildcard DB targets?
	@# TODO: List from db.py?
	python db.py init user
	python db.py init group
	python db.py init room

populate-db:
	python init_auth.py
	python init_rooms.py

# Remove all runtime based information.
# Should return the repo to a "source-only" state.
clean:
	# Remove all database files.
	rm -rf db
