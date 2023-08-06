# ~ https://github.com/AlexandreMahdhaoui/MongoNow
# ~ misschien al extra module installeren zodat er geen echte mongodb hoeft te runnen in eerste instantie
import os
import sys
import time
import argparse


# -----------------------------------------------------------------------
sys.path.append( os.path.split( __file__ )[0] )


# -----------------------------------------------------------------------
import modules
from modules import config
from modules import database
from modules import node
from modules import tasks
from modules import web
from modules import cli
from modules import queue
from modules import watchfolder
from modules import misc


# -----------------------------------------------------------------------
import addons


# -----------------------------------------------------------------------
def start():
	# check if the database server  instance is running
	info = database.database_is_running()
	if info is None:
		print( "Cannot connect to server on: %s" % database.DATABASE_IP )
		exit()


	print( "Initializing the web server" )
	web.init( __name__ )
	print( "Connecting to database: '%s'" % config.GESTION_DB )
	database.load()
	print( "Loading node for host:  '%s'" % config.HOST )
	node.load()
	
	if config.FIRST_RUN:
		root = os.path.join( config.GESTION_FOLDER, "default" )
		if not os.path.exists( root ):
			os.mkdir( root )
			node.create_project( "default", root )
			
			
	# ~ page.create_route()
	# ~ create_project( name = "default" )

	routes_to_create 	= []
	processes_to_start 	= []
	
	for name in [ name for name in dir( modules ) if not name.startswith("__") ]:
		print( name )
		mod = getattr( modules, name )
		for item in dir( mod ):
			obj = getattr( mod, item )
			if isinstance(obj, web.Page):
				if obj.name is None:
					obj.name = item
				routes_to_create.append( obj )
			elif isinstance( obj, tasks.Task ):
				processes_to_start.append( obj )
				# ~ web.create_route( obj )


	addons_path = os.path.join( os.path.split( __file__ )[0], "addons"  )
	for f in os.listdir( addons_path ):
		if f[0] not in ["_", "."]:
			addon_name, extension = os.path.splitext( f )
			if extension.lower() == ".py":
				addon = getattr( addons, addon_name )
				for item in dir( addon ):
					obj = getattr( addon, item )
					if isinstance( obj, web.Page ):
						if obj.name is None:
							obj.name = item
						routes_to_create.append( obj )
					elif isinstance( obj, tasks.Task ):
						processes_to_start.append( obj )


	print( "Creating routes" )
	for route in routes_to_create:
		web.create_route( route )


	print( "Starting tasks" )
	for proc in processes_to_start:
		print( "Starting task: %s" % proc.func_name )
		proc.execute()


# start web server
	web.start_server()


# -----------------------------------------------------------------------
def main():
	if len( sys.argv ) > 1:
		cli.parse_args_and_execute( sys.argv )
	# check for args, parse them and execute them
	else:
		# ~ print( "else" )
		start()

def main():
	coll = database.get_collection( "projects" )
	doc = coll.find_one( name = "luisterklinkers" )
	print( doc.root["_value"] )
	
# ~ # -----------------------------------------------------------------------
if __name__ == "__main__":
	main()




