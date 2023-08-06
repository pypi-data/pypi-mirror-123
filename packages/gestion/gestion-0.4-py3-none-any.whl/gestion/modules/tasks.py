import os
import time
import psutil
from multiprocessing import Process
from multiprocessing import Queue


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import database
	from modules import web
else:
	import database
	import web


#-----------------------------------------------------------------------
class Proc():
	def __init__( self, func ):
		self.__func 	= func
		self.__queue	= None
		self.__wait		= False
		self.__daemon	= False
		self.__results	= { "output" : None, "error" : None }


	#-------------------------------------------------------------------
	def execute(self, *args, **kwargs):
		write_to_log( "Starting proces: %s" % self.__func.__name__ )
		self.__queue = Queue()
		self.__queue.put( { "args":args, "kwargs":kwargs } )
		self.__proc = Process( target = self.wrapped_func, args = ( self.__queue, ) )
		
		self.__proc.daemon = self.__daemon
		self.__proc.start()

		if self.__wait:
			self.__proc.join()


	#-------------------------------------------------------------------
	def wrapped_func( self, queue ):
		output 	  = None
		error 	  = None
		arguments = self.__queue.get()

		try:
			output = self.__func( *arguments[ "args" ], **arguments[ "kwargs" ] )
		except Exception as exc:
			error = str(exc)

		self.__queue.put( { "output":output, "error":error } )
	
	#-------------------------------------------------------------------
	def get_queue(self):
		if self.__queue != None:
			self.__results = self.__queue.get()
			self.__queue = None

	#-------------------------------------------------------------------
	@property
	def output( self ):
		self.__get_queue()
		return self.__results[ "output" ]
			
	@property
	def error( self ):
		self.__get_queue()
		return self.__results[ "error" ]
	
	@property
	def func_name( self ):
		return self.__func.__name__

	@property
	def pid(self):
		return self.__proc.pid

	@property
	def state(self):
		return self.__proc.is_alive()
		
	@property
	def type(self):
		return self.__class__.__name__.lower()



#-----------------------------------------------------------------------
class Addon( Proc ):
	def __init__( self, func ):
		Proc.__init__( self, func )
		self.__daemon = True
		
		# ~ self.__wait = False # locked value


class Task( Proc ):
	def __init__( self, func ):
		Proc.__init__( self, func )
		self.__wait	= False


#-----------------------------------------------------------------------		
def create_collections():
	if not database.collection_exists( "log" ):
		log 			= database.Blueprint()
		log.userhost	= database.Userhost()
		log.type 		= database.String()
		log.date 		= database.Date()
		log.log 		= database.String()
		log.set_local( False )
		database.create_collection( "log", log )


#-----------------------------------------------------------------------
#
# LOG PAGE
#
def log_page():
	coll 			= database.get_collection( "log" )
	data			= web.Data( coll.find() )
	data.blueprint	= coll.blueprint
	return web.Template( "fullscreen", data = data )

log 				= web.Page()
log.function		= log_page


#-----------------------------------------------------------------------
#
# taskmanager-a-like functions
#
#-----------------------------------------------------------------------
def find_process_by_name(name):
	results = [ proc.info for proc in psutil.process_iter( ["name", "pid"] ) if name.lower() in proc.info["name"].lower() ]
	return results


#-----------------------------------------------------------------------
def find_process_by_port(port:int):
	processes = [ psutil.Process(pid=proc.pid) for proc in psutil.net_connections() if proc.laddr.port == port ]
	return processes


#-----------------------------------------------------------------------
def manager():
	while True:
		print("Checking for zombified processes")


#-----------------------------------------------------------------------
def write_to_log( to_log:str):
	coll 				= database.get_collection( "log" )
	blueprint 			= coll.blueprint
	blueprint.log.value = to_log
	coll.append( blueprint )
	
	

create_collections()
#-----------------------------------------------------------------------
# ~ def start():
	# ~ pass


#-----------------------------------------------------------------------
