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
		projects.name.default 	= "default"
		projects.root 			= database.Path()
		projects.root.value 	= os.path.join( config.HOME )
		projects.workspace		= database.Dictionary()
		projects.set_local( True )
		database.create_collection( "projects", projects )


	if not database.collection_exists( "software" ):
		software 			= database.Blueprint()
		software.name 		= database.String()
		software.path 		= database.Path()
		software.extension 	= database.String()
		software.set_local( True )
		database.create_collection( "software", software )


	if not database.collection_exists( "mounts" ):
		mounts 			  = database.Blueprint()
		mounts.user 	  = database.User()
		mounts.userhost   = database.Userhost()
		mounts.servername = database.String()
		mounts.root 	  = database.Path()
		mounts.set_local( True )
		database.create_collection( "mounts", mounts )

	
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

		
update_status_proc 			= tasks.Task( update_status )
update_status_proc.__wait 	= False

#-----------------------------------------------------------------------
#
# commonly used functions included
#
#-----------------------------------------------------------------------
def map_path( path, user = config.USER, project = config.PROJECT ):
	mounts 			= database.Collection( "mounts" )
	local_mounts 	= mounts.find_one(user = user)
	maps 			= local_mounts[ "maps" ]
	mapped_path 	= path

	for item in mounts.find():
		for key in [ key for key in item[ "maps" ].keys() if key in maps.keys() ]:
			if path.lower().startswith( item[ "maps" ][key].lower()):
				found 		= path[ :len( item[ "maps" ][ key ] ) ]
				mapped_path	= path.replace( found, maps[ key ] )
				break

	if os.path.exists( mapped_path ):
		return mapped_path
	else:
		raise Exception( "Cannot open %s on client: %s" % ( mapped_path, config.USER ) )


#-----------------------------------------------------------------------
def add_software( name, path, extension ):
	coll 					= database.get_collection( "software" )
	doc 					= coll.blueprint
	doc["name"].value 		= name
	doc["path"].value 		= path
	doc["extension"].value 	= extension
	coll.append( doc )

cli.add_command( add_software )


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
def get_software( name, user = config.USER ):
	software = database.Collection("renderers").find_one( user = user )
	if name in renderers["renderers"].keys():
		return renderers["renderers"][name]

	else:
		raise Exception( "Cannot find renderer %s on client: %s" % ( name, user ) )
		

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
	return web.Template( "default", data = web.Data( projects.find_one( name = config.PROJECT ) ) )

projects			= web.Page()
projects.function	= projects_page


#-----------------------------------------------------------------------
def create_project( name, root ):
	projects 			= database.get_collection( "projects" )
	document 			= projects.blueprint
	document.name.value = name
	document.root.value = root
	projects.append( document )


#-----------------------------------------------------------------------
def load():
	create_collections()
	if config.FIRST_RUN:
		root = os.path.join( config.GESTION_FOLDER, "default" )
		if not os.path.exists( root ):
			os.mkdir( root )
		create_project( "default", root )
		# ~ page.create_route()
		# ~ create_project( name = "default" )

#-----------------------------------------------------------------------
load()
