#-----------------------------------------------------------------------
import os
import sys
import json
import time


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
	from modules import tasks
	from modules import database
	from modules import web
	from modules import cli
else:
	import config
	import tasks
	import database
	import web
	import cli


#-----------------------------------------------------------------------
def create_collections():
	# ~ [ "mounts", "software", "projects", "log", "users" ]
	if not database.collection_exists( "projects" ):
		projects 				= database.Blueprint()
		projects.name 			= database.String()
		projects.root 			= database.Path()
		projects.local			= database.Boolean()
		projects.local.defaults = False
		projects.set_local( True )
		
		database.create_collection( "projects", projects )


	if not database.collection_exists( "software" ):
		software 			= database.Blueprint()
		software.name 		= database.String()
		software.path 		= database.Path()
		software.extension 	= database.String()
		software.set_local( True )
		
		database.create_collection( "software", software )


	# ~ if not database.collection_exists( "mounts" ):
		# ~ mounts 			  = database.Blueprint()
		# ~ mounts.user 	  = database.User()
		# ~ mounts.userhost   = database.Userhost()
		# ~ mounts.servername = database.String()
		# ~ mounts.root 	  = database.Path()
		# ~ mounts.set_local( True )
		
		# ~ database.create_collection( "mounts", mounts )

	
	if not database.collection_exists( "nodes" ):
		nodes 			= database.Blueprint()
		nodes.host 		= database.Host()
		nodes.status	= database.String()
		nodes.heartbeat	= database.Integer()
		
		database.create_collection( "nodes", nodes )


#-----------------------------------------------------------------------
#
# node tasks
#
#-----------------------------------------------------------------------
def update_status():
	nodes = database.get_collection( "nodes" )
	while True:
		doc = nodes.find_one( host = config.HOST )
		time.sleep( 10 )

		
update_status_task 			= tasks.Task( update_status )
update_status_task.wait 	= False

#-----------------------------------------------------------------------
#
# commonly used functions included
#
#-----------------------------------------------------------------------
def map_path( path ):
	print( "map_path" )
	print( path )
	# ~ mounts 			= database.Collection( "mounts" )
	# ~ local_mounts 	= mounts.find_one( user = user )
	# ~ maps 			= local_mounts[ "maps" ]
	# ~ mapped_path 	= path

	# ~ for item in mounts.find():
		# ~ for key in [ key for key in item[ "maps" ].keys() if key in maps.keys() ]:
			# ~ if path.lower().startswith( item[ "maps" ][key].lower()):
				# ~ found 		= path[ :len( item[ "maps" ][ key ] ) ]
				# ~ mapped_path	= path.replace( found, maps[ key ] )
				# ~ break

	# ~ if os.path.exists( mapped_path ):
		# ~ return mapped_path
	# ~ else:
		# ~ raise Exception( "Cannot open %s on client: %s" % ( mapped_path, config.USER ) )


#-----------------------------------------------------------------------
def add_software( name, path, extension ):
	coll 					= database.get_collection( "software" )
	doc 					= coll.blueprint
	doc["name"].value 		= name
	doc["path"].value 		= path
	doc["extension"].value 	= extension
	coll.append( doc )


cli.add_command( add_software )


#-----------------------------------------------------------------------
def available_software():
	coll 	= database.get_collection( "software" )
	results = coll.find()
	return [ result["name"].value for result in  results ]


#-----------------------------------------------------------------------
def list_software():
	coll 	= database.get_collection( "software" )
	results = coll.find()
	
	print("#"*32)
	print( "Software available:" )
	for result in results:
		print( "%s: %s" % ( result["name"].value,  result["path"].value ) )
	print("#"*32)


cli.add_command( list_software )


#-----------------------------------------------------------------------
def get_software( name ):
	path = None
	if name in available_software():
		document = database.Collection("software").find_one( name = name )
		if document:
			path = document["path"].value

	
	if path is None:
		raise ValueError( "Cannot find software %s on client: %s" % ( name, user ) )
	else:
		return path
	
		

#-----------------------------------------------------------------------
#
# WEB PAGES
#
#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
#
# INDEX PAGE
#

def index_page():
	if config.FIRST_RUN:
		config.FIRST_RUN = False
		return web.Redirect( "login" )
	else:
		return web.Redirect( "home" )

index 				= web.Page()
index.add_route( "/" )
index.function 		= index_page



#-----------------------------------------------------------------------
def toggle_status():
	referrer = web.request.referrer.split("/")[-1]
	
	if config.STATUS == "available":
		config.STATUS = "unavailable"
	else:
		config.STATUS = "available"

	return web.Redirect( referrer )
	
	
toggle = web.Page()
toggle.function = toggle_status
	


#-----------------------------------------------------------------------
def login_page():	
	bp 					 	= database.Blueprint()
	bp.database_ip		 	= database.String()
	bp.database_ip.value	= config.DATABASE_IP
	bp.database_port		= database.Integer()
	bp.database_port.value	= config.DATABASE_PORT
	
	data	 				= web.Data( bp )
	return web.Template( "default", data )


login				= web.Page()
login.function		= login_page

#-----------------------------------------------------------------------
#
# HOME PAGE
#

def home_page():
	return web.Template( "default" )

home			 = web.Page()
home.function	 = home_page

#-----------------------------------------------------------------------
#
# SETTINGS PAGE
#
def settings_page():
	data = web.Data( config )
	return web.Template( "default", data = data )

settings 			= web.Page()
settings.function	= settings_page


#-----------------------------------------------------------------------
#
# PROJECTS PAGE
#
def projects_page():
	projects = database.get_collection( "projects" )
	return web.Template( "default", data = web.Data( projects.find( ) ) )


projects			= web.Page()
projects.function	= projects_page


#-----------------------------------------------------------------------
def create_project( name, root ):
	projects 			= database.get_collection( "projects" )
	document 			= projects.blueprint
	document.name.value = name
	document.root.value = root
	projects.append( document )


cli.add_command( create_project )
#-----------------------------------------------------------------------
def list_projects():
	coll 	= database.get_collection( "projects" )
	results = coll.find()
	
	print("#"*32)
	print( "Projects available:" )
	for result in results:
		print( "%s: %s" % ( result["name"].value,  result["root"].value ) )
	print("#"*32)
	
cli.add_command( list_projects )


#-----------------------------------------------------------------------
def set_project( name ):
	pass 
	

	


#-----------------------------------------------------------------------
def load():
	create_collections()

#-----------------------------------------------------------------------
load()
