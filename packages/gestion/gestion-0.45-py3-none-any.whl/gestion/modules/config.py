import os
import sys
import inspect
from socket import gethostname
from getpass import getuser
from configparser import ConfigParser


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import cli
	# ~ from modules import node
else:
	import cli
	# ~ import node


#-----------------------------------------------------------------------
#
# which keys need to be saved, does home need to be saved
# I think so, so we can change where the static folder resides,
# or perhaps that would be another key in the dict
# sommige attributes kunnen al in de class zitten, zoals USER, en HOST, andere 
# attributeen worden maar 1 keer ingelezen, zoals ip adressen en poorten en config file.
# de andere attributen zijn dynamischer en kunnen vaker geschreven en gelezen worden van disk
#
#-----------------------------------------------------------------------
#
# config based functions and periphelia
#
#-----------------------------------------------------------------------
defaults = 	{
				"_user" 			: getuser(),
				"_host" 			: gethostname().split( "." )[ 0 ],
				"_home" 			: os.path.expanduser( "~" ),
				"_gestion_folder"	: os.path.join( os.path.expanduser( "~" ), "gestion" ),
				"_template_folder"	: os.path.join( os.path.split( os.path.split( __file__ )[ 0 ] )[ 0 ], "web", "templates" ),
				"_static_folder"	: os.path.join( os.path.expanduser( "~" ), "gestion", "static" ),
				"_static_folder"	: os.path.join( os.path.split( os.path.split( __file__ )[ 0 ] )[ 0 ], "web", "static" ), # deze is even voor 
				"_config_file"		: os.path.join(os.path.expanduser("~"), "gestion", "config.ini" ),
				"database_ip" 		: "127.0.0.1", 
				"database_port"		: 27017,
				"web_ip" 			: "127.0.0.1",
				"web_port" 			: 5000,
				"node_type"			: "client",
				"project"			: "default",
				"gestion_db"		: "gestion_db_new_1",
				"first_run"			: True,
				"status"			: "available"
			}


#-----------------------------------------------------------------------
class Config( dict ):
	def __init__( self ):
		dict.__init__( self, defaults )
		self.file = self.pop( "_config_file" )

		if not self.file_exists:
			self.create_file()
		
	def __getattr__( self, key ):
		env 	= None
		# ~ keys	= defaults.keys()
	
		if "_" + key.lower() in self.keys():
			env = "_" + key.lower()
		elif key.lower() in self.keys():
			env = key.lower()
		if env:
			return type( defaults[ env ] )( self[ env ] )
		else:
			return self.__dict__[ key ]


	def __setattr__( self, key, value ):
		env 	= None
		
		if key.lower() in self.keys():
			env = key.lower()
		
		elif "_" + key.lower() in self.keys():
			env = "_" + key.lower()

		if env:
			self[ env ] = value
		else:
			dict.__setattr__( self, key, value )


	def __setitem__( self, key, value ):
		dict.__setitem__( self,  key, value )
		if self.file_exists:
			self.save_to_file()
		
		
	def __getitem__( self, key ):
		if self.file_exists:
			self.load_from_file()
		return dict.__getitem__( self,  key )
		
	
	@property
	def file_exists( self ):
		return os.path.exists( self.file )
		

	@property
	def is_first_run( self ):
		if self.file_exists:
			return self[ "first_run" ]
	

	def create_file( self ):
		if not os.path.exists( os.path.split( self.file )[ 0 ] ):
			os.makedirs( os.path.split( self.file )[ 0 ] )
		self.save_to_file()
		
		
	def save_to_file( self ):
		kwargs = {}
		for key in [ key for key in dict.keys( self ) if not key.startswith("_") ]:
			kwargs[ key ] = dict.__getitem__( self, key )

		configparser 				= ConfigParser()
		configparser[ "global" ] 	= kwargs
		
		with open( self.file, 'w' ) as f:
			configparser.write( f )


		
	def load_from_file( self ):
		configparser = ConfigParser()
		configparser.read( self.file )
		self.update( **configparser[ "global" ] )
		
		# ~ if defaults[ "config_file" ] != self[ "config_file" ]:
			# ~ config = ConfigParser()
			# ~ config.read( self[ "config_file" ] )
			# ~ self.update( **config["global"] )
		

	def reset( self, hard_reset = True ):
		pass


#-----------------------------------------------------------------------
# ~ if not os.path.exists( defaults[ "config_file" ] ):
	# ~ os.makedirs( os.path.split( config_file )[0] )
	

config = Config()
sys.modules[__name__] = config


