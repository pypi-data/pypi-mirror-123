#-----------------------------------------------------------------------
import argparse
import importlib

#-----------------------------------------------------------------------
available_commands = {}


#-----------------------------------------------------------------------
def add_command(function):
	# check doen of function ook echt een function is
	# en iets doen met de arguments, dus kijken welke arguments in 
	# de functie gevraagd worden en deze niet invoeren als dat niet nodig is
	#
	available_commands[ function.__name__ ] = function.__module__


#-----------------------------------------------------------------------
def add_commands( *functions ):
	for function in functions:
		add_command( function )



#-----------------------------------------------------------------------
def parse_args_and_execute( argv ):
	# ~ print( args )
	gestion_path 	= argv.pop( 0 )
	command 		= argv.pop( 0 ) 

	args 	= []
	kwargs 	= {}

	index = 0
	while len( [ item for item in argv if item is not None  ] ) != 0:
		if argv[ index ].startswith( "-" ):
			kwargs[ argv[ index ][ 1: ] ] = argv[ index+1 ]
			argv[ index ] 	 = None
			argv[ index+ 1 ] = None
			index += 2
		else:
			args.append( argv[ index ] )
			argv[ index ] = None
			index += 1

	module			= importlib.import_module( available_commands[ command ] )
	func			= getattr( module, command )
	# ~ func.__code__.co_varnames	
	
	return func( *args, **kwargs )

