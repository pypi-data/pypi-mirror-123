import os
import sys
import inspect
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from markupsafe import Markup


#-----------------------------------------------------------------------
# mongod version  v4.4.4
# pymongo 3.12.0


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
else:
	import config


#-----------------------------------------------------------------------
# moet nog iets verzinnen voor database van iedereen of voor de node
# dus projecten staan op server, en path maps en software staan in de database 
# met de naam van de userhost
class Collection( object ):
	def __init__( self, name:str ):
		# ~ list.__init__( self )
		self.name 		= name		
		self._root_id 	= Blueprint().id
		self._blueprint = None
		self._sort 		= ( "_id", -1 )
		self._filter 	= {}
		self._limit		= 25


	def __str__( self ):
		return "<Instance of Collection: %s>" % self.name


	def __repr__( self ):
		return "<Instance of Collection: %s>" % self.name


	@property
	def local( self ):
		return self.blueprint.local
		# ~ check whether the database is specifica for the node or a global database ( e.g. projects )


	@property
	def database_name( self ):
		return self.database.name
		
	
	@property
	def database( self ):
		return connect_to_database() 


	@property
	def exists( self ):
		if self.database_name in list_databases():
			return collection_exists( self.name )
		else:
			return False


	@property
	def blueprint( self ):
		if self.exists:
			if self._blueprint is None:
				result = self.database[ self.name ].find_one( { "_id": self._root_id } )
				result.pop( "_id" )
				document = Document()
				document.create_from_dict( result )
				self._blueprint = document
			return self._blueprint.copy()

		else:
			return self._blueprint.copy()


	@blueprint.setter
	def blueprint( self, blueprint ):
		if not self.exists:
			# ~ print ( "%s doesnt exist"  % self.name ) 
			if isinstance( blueprint, Blueprint ):
				self._blueprint 					= dict( blueprint )
				self._blueprint["_id"] 				= self._root_id
				for key in self._blueprint.keys():
					if key != "_id":
						self._blueprint[ key ][ "_collection" ] = self.name

			else:
				raise Exception( "Need a Blueprint instance, not a %s " % type( blueprint ) )
		else:
			raise Exception( "Collection %s already exists!" % self.name )


	def create( self ):
		if not self.exists:
			if self._blueprint != None:
				self.database[ self.name ].insert_one( self._blueprint )


	def update_blueprint( self, blueprint ):
		pass


	def append( self, document ):		
		if "_id" in document.keys():
			document.pop( "_id" )
		for key in document.keys():
			document[ key ].execute_before_append()
			
		# ~ perhaps only put the _value in databse, eareir for searching perhaps?
		
		self.database[ self.name ].insert_one( document )


	def extend( self, *documents ):
		self.database[ self.name ].insert_many( documents )


	def clear( self ):
		self.database[ self.name ].delete_many( {} )
		
	
	def delete( self ):
		self.database[ self.name ].drop()


	def __getitem__( self, key ):
		# wel of niet met id?
		if isinstance( key, slice ):
			start 	= int(key.start) + 1
			end 	= int(key.stop) + 1
			results = []
			for item in list( self.database[ self.name ].find( {} )[ start:end ] ):
				doc 	= self.blueprint
				doc.create_from_dict( item )
				results.append( doc )
			return results
		else:
			return self.find_one()


	def __iter__( self ):
		print( "__iter__" )
		for item in self.database[ self.name ].find(  { "_id" :{ "$ne": self._root_id} } ):
			doc = self.blueprint
			doc.create_from_dict( item )
			yield doc


	def __setitem__( self, key, kwargs ):
		if isinstance( key, ObjectId ):
			if key == self._root_id:
				raise ValueError( "Changing document with __root_id will change blueprint, use update_blueprint instead!" )
			else:
				if self.database[ self.name ].find_one( { "_id" : key } ):
					self.database[ self.name ].replace_one( { "_id" : key }, kwargs )
				else:
					raise ValueError( "No item found with _id: " + str( key ) )
		else:
				raise ValueError("Key needs be an ObjectdId and not a " + type( key ) )


	def find( self, **kwargs ):
		keys = list( kwargs.keys() )
		for key in keys:
			datatype 		= self.blueprint[ key ]
			datatype.value 	= kwargs[ key ]
			kwargs[ key ] 	= datatype
		
		if self.local:
			datatype 			= self.blueprint[ "_local" ]
			datatype.execute_before_append()
			kwargs[ "_local" ]	= datatype
		
		kwargs.update( { "_id" :{ "$ne": self._root_id} } )
		results = []
		
		for item in self.database[ self.name ].find( kwargs, sort = [ self._sort ], limit = self._limit ):
			doc = self.blueprint
			doc.create_from_dict( item )
			results.append( doc )
		
		return results


	def find_one( self, **kwargs ):
		keys = list( kwargs.keys() )
		for key in keys:
			datatype 		= self.blueprint[ key ]
			datatype.value 	= kwargs[ key ]
			kwargs[ key ] 	= datatype
		
		if self.local:
			datatype 			= self.blueprint[ "_local" ]
			datatype.execute_before_append()
			kwargs[ "_local" ]	= datatype
		
		
		kwargs.update( { "_id" :{ "$ne": self._root_id} } )
		
		result = self.database[ self.name ].find_one( kwargs )
		doc = self.blueprint
		
		if result == None:
			doc = None
		else:
			doc.create_from_dict( result )

		return doc


#-----------------------------------------------------------------------
#
# document, blueprint class
#
#-----------------------------------------------------------------------
class Document( dict ):
	def __init__( self ):
		dict.__init__( self )
		self.set_local( False )
		
	def __repr__( self ):
		return str( { key:self[key] for key in self.keys() } )


	def __str__( self ):
		return str( { key:self[key] for key in self.keys() } )


	def __setattr__( self, key, value ):
		if key in ["local"]:
			self.set_local( value )
		elif isinstance( value, Datatype ):
			self[ key ] = value
		else:
			raise AttributeError( "Not a datatype" )


	def __getattr__( self, key ):
		if key in self.keys():
			return self[ key ]
		else:
			return self.__dict__[ key ]


	def __getitem__( self, key ):
		if key == "_id" :
			return dict.__getitem__( self, key )
		else:
			result = dict.__getitem__( self, key )
			if isinstance( result, Datatype ):
				return result
			else:
				instance 	= getattr( sys.modules[__name__], key )()
				instance.update( dict.__getitem__( self, key ) )
				return instance

	def copy( self ):
		document = Document()
		document.create_from_dict( self )
		return document


	@property
	def id( self ):
		if "_id" in self.keys():
			return self[ "_id" ]
		else:
			return None
		
	@property
	def local( self ):
		return isinstance( self._local, Userhost )
		

	def set_local( self, value:bool ):
		if value   == True:
			datatype	= Userhost()		
		elif value == False:
			datatype	= Null()
		
		datatype.hidden		= True
		self._local 		= datatype
		

	def delete( self ):
		self["_id"] = None
		# ~ delete it from collection


	def update( self, kwargs ):
		for key in kwargs.keys():
			if key in self.keys():
				if key == "_id":
					self[ key ] = kwargs[ key ]
				else:
					self.__getattr__( key )[ "_value" ] = kwargs[ key ][ "_value" ]
			else:
				self[ key ] = kwargs[ key ]


	def create_from_dict( self, kwargs: dict = {} ):
		self.update( kwargs )
		for key in kwargs.keys():
			if key != "_id":
				class_name = kwargs[ key ][ "_class" ]
				attr = getattr( sys.modules[__name__], class_name )
				instance = attr()
				instance.update( kwargs[ key ] )
				setattr( self, key, instance )


	def keys( self ):
		return [ item for item in dict.keys( self ) ]


	def as_dict( self ):
		result = {}
		for key in self.keys():
			if key != "_id":
				if self[key].hidden == False:
					 result[ key ] = self[ key ].value
				else:
					 result[ key ] = self[ key ]
		
		return result

	
	def as_html( self ):
		result = {}
		for key in self.keys():
			if key != "_id":
				if self[ key ].hidden == False:
					 result[ key ] = self[ key ].as_html()
			else:
				 result[ key ] = self[ key ]
		
		return result
		
		
		

#-----------------------------------------------------------------------
class Blueprint( Document ):
	def __init__( self ):
		Document.__init__( self )


	@Document.id.getter
	def id( self ):
		return  ObjectId( b"%012d" % 0 )
	

#-----------------------------------------------------------------------
#
# datatype classes
#
#-----------------------------------------------------------------------
class Datatype( dict ):
	def __init__( self, **kwargs ):
		dict.__init__(self)
		self._collection 	= None
		self.default		= ""
		self.unique 		= False
		self.locked 		= False
		self.hidden 		= False
		self.html			= None
		self._value 		= None
		self._class 		= self.__class__.__name__
		self.update( kwargs )


	#-------------------------------------------------------------------
	def __getattr__( self, key ):
		if key in self.keys() and key != "value" :
			return self[ key ]
		
		elif key == "value":
			if self[ "_value" ] is not None:
				return self.decode( self["_value" ] )
			else:
				return self.decode( self[ "default" ] )


	#-------------------------------------------------------------------
	def __setattr__( self, key, value ):
		if key not in  [ "value", "default" ]:
			self[ key ] = value
		
		elif key == "default":
			self[ "default" ] =  self.encode( value )
			if self._value is None:
				self._value = self.encode( value )
		
		elif key == "value":
			self._value = self.encode( value )


	def execute_before_append(self):
		pass


	def execute_before_update(self):
		pass


	def encode( self, value ):
		return value


	def decode( self, value ):
		return value


	def get_value( self ):
		return self.value
		
	
	def set_value( self, value ):
		self.value = value


	def as_html( self ):
		if self.html == None:
			return self.value
		else:
			return Markup( self.html % self.value  )
		
		
#-----------------------------------------------------------------------
class Dictionary( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )
		
#-----------------------------------------------------------------------
class List( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )


#-----------------------------------------------------------------------
class Integer( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )


#-----------------------------------------------------------------------
class Boolean( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )
		self.default = False


#-----------------------------------------------------------------------
class Float( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )


#-----------------------------------------------------------------------
class String(Datatype):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )


#-----------------------------------------------------------------------	
class Null( Datatype ):
	def __init__( self, **kwargs ):
		Datatype.__init__( self, **kwargs )
	
	def encode( self, value ):
		return None

	def encode( self, value ):
		return None


#-----------------------------------------------------------------------
class Date(String):
	def __init__( self, **kwargs ):
		String.__init__( self, **kwargs )


	def execute_before_append(self):
		now = datetime.now()
		self.value = now.strftime("%d/%m/%Y %H:%M:%S")


#-----------------------------------------------------------------------
class Path( String ):
	def __init__( self, **kwargs ):
		String.__init__( self, **kwargs )


	def encode( self, value ):
		return "%s:<%s>:%s" % ( config.USER, config.PROJECT, value )


	def decode( self, value ):
		return value.split( ":" )[-1]


	@property
	def exists( self ):
		return os.path.exists( self.value )


	@property
	def absolute_path( self ):
		return "abs_path for: %s" % self.value


	@property
	def relative_path( self ):
		return "rel_path for: %s" % self.value

		
	@property
	def base_name( self ):
		return "base_name for: %s" % self.value

	
	def as_html( self ):
		return self.base_name


#-----------------------------------------------------------------------
class Directory( Path ):
	def __init__( self, **kwargs ):
		Path.__init__( self, **kwargs )


class File( Path ):
	def __init__( self, **kwargs ):
		Path.__init__( self, **kwargs )

	@property
	def extension( self ):
		return os.path.splitext( self.value )[-1]


#-----------------------------------------------------------------------
class Userhost( String ):
	def __init__( self, **kwargs ):
		String.__init__( self, **kwargs )
		self.default = config.USER, config.HOST
	
	@property
	def user( self ):
		return self._value.split(":")[0]
		
	@property
	def host( self ):
		return self._value.split(":")[1]


	def encode( self, value ):
		return ":".join( value )

	def execute_before_append( self ):
		self.execute_before_update()

	def execute_before_update( self ):
		self.value =  config.USER, config.HOST


class User( String ):
	def __init__( self, **kwargs ):
		String.__init__( self, **kwargs )
		self.default = config.USER	
	
	def execute_before_append( self ):
		self.execute_before_update()

	def execute_before_update( self ):
		self.value = config.USER


class Host( String ):
	def __init__( self, **kwargs ):
		String.__init__( self, **kwargs )
		self.default = config.HOST

	def execute_before_append( self ):
		self.execute_before_update()

	def execute_before_update( self ):
		self.value = config.HOST


#-----------------------------------------------------------------------
#
# helper functions
#
#-----------------------------------------------------------------------
def database_is_running():
	connection = pymongo.MongoClient( "%s" % config.DATABASE_IP, config.DATABASE_PORT, serverSelectionTimeoutMS = 2000 )
	try:
		return connection.server_info() # will throw an exception
	
	except Exception as e:
		return False


def connect_to_database( ):
	connection = pymongo.MongoClient( "%s" % config.DATABASE_IP, config.DATABASE_PORT )
	return connection[ config.GESTION_DB ]


def list_databases():
	connection = pymongo.MongoClient( "%s" % config.DATABASE_IP, config.DATABASE_PORT )
	return [ db["name"] for db in connection.list_databases() if db["name"] not in [ "admin", "config", "local" ] ]



def list_collections( ):
	database = connect_to_database( )
	return database.collection_names()


def collection_exists( name:str ):
	return name in list( list_collections() )


def create_collection( name:str, blueprint:Blueprint ):
	coll = Collection( name )
	if not coll.exists:
		coll.blueprint = blueprint
		coll.create()
		return coll
	else:
		raise Exception( "Collection %s already exists" % name )
		return None


def get_collection( name:str ):
	if name in list_collections( ):
		coll = Collection( name )
		return coll
	else:
		raise Exception( "Collection %s does not exist in database %s" % ( name, config.GESTION_DB ) )


def load():
	if database_is_running():
		pass

	else:
		raise Exception( "Cannot connect to database on: %s" % config.DATABASE_IP )
	

#-----------------------------------------------------------------------
if __name__ == "__main__":
	pass
