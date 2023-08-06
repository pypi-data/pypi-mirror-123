#-----------------------------------------------------------------------
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
import addons


#-----------------------------------------------------------------------
def loop_queue():
	while True:
		if config.STATUS == "available":
			conn = database.get_collection( "queue" )
			try:
				doc = conn.find_one( status = "waiting", project = config.PROJECT )
				if doc:
					doc.status.value = "processing"
					conn[ doc.id ]	 = doc
					
					try:
						results 		 = process_queued_item( doc )
						doc.status.value = "done"
					
					except Exception as e:
						doc.status.value  	= "error"
						error 				= str( e )
						tasks.write_to_log( error )

					conn[ doc.id ] = doc

			except Exception as e:
				error = str( e )
				tasks.write_to_log( error )

		else:
			print( f"Host: {config.HOST} not available for processing queue." )

		print( "Going to sleep for 10 seconds" )
		time.sleep( 10 )


#-----------------------------------------------------------------------
def process_queued_item( queued_item ):
	name 	= queued_item.addon.value 
	results = None

	if name in addons.available_addons():
		addon	= addons.LOADED[ name ]
		kwargs	= queued_item.arguments.value
		addon.execute( **kwargs )
	else:
		raise NameError( f"Addon {name} not found, not processing" )

	return results


#-----------------------------------------------------------------------
loop_queue_task		 = tasks.Task( loop_queue )
loop_queue_task.wait = False


#-----------------------------------------------------------------------
def add_to_queue( addon, project = None, **kwargs ):
	# ~ builtin a check if file and addon exist
	if project is None:
		project = config.PROJECT

	try:
		if addon in addons.available_addons():	
			coll 						= database.get_collection( "queue" )
			doc 						= coll.blueprint
			doc[ "addon" ].value 		= addon
			doc[ "project" ].value  	= project
			doc[ "arguments" ].value 	= kwargs
			coll.append( doc )
		else:
			raise NameError( f"Addon {addon} not found, ignoring request and not adding to queue" )

	except Exception as e:
		print( str( e ) )
		tasks.write_to_log( str( e ) )


cli.add_command( add_to_queue )


#-----------------------------------------------------------------------
#
# add entry to database
#
#-----------------------------------------------------------------------
def create_collection():
	if "queue" not in database.list_collections():
		queue					= database.Blueprint()
		queue.project			= database.String()
		queue.project.default	= "default"
		queue.addon				= database.String()
		queue.arguments			= database.Dictionary()
		queue.userhost 			= database.Userhost()
		queue.date	 			= database.Date()
		queue.status 			= database.String()
		queue.status.default	= "waiting"
		
		coll 					= database.Collection( "queue" )
		coll.blueprint 			= queue
		coll.create()


#-----------------------------------------------------------------------
#
# create queue webpage
#
#-----------------------------------------------------------------------
def queue_page():
	coll 			= database.get_collection( "queue" )
	data 			= web.Data( coll.find() )
	data.blueprint 	= coll.blueprint
	return web.Template( "fullscreen", data = data )


queue 			= web.Page()
queue.function 	= queue_page

#-----------------------------------------------------------------------
#
# create queue webpage
#
#-----------------------------------------------------------------------
create_collection()


