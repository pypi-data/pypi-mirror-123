#-----------------------------------------------------------------------
import sys
import os
import traceback
from flask import Flask
from flask import Response
from flask import stream_with_context
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import json
from markupsafe import Markup


#-----------------------------------------------------------------------
server = None


#-----------------------------------------------------------------------
if "." in __name__:
	from modules import config
	from modules import database
else:
	import config
	import database


#-----------------------------------------------------------------------
def init( name ):
	setattr( sys.modules[__name__], "server", Flask( name, static_folder = config.STATIC_FOLDER, template_folder = config.TEMPLATE_FOLDER ) ) # static folder default in home static


#-----------------------------------------------------------------------
def start_server( debug = True, use_reloader = False ):
	threaded = False
	server.run(debug = debug, host = config.WEB_IP, port = config.WEB_PORT, threaded = threaded, use_reloader = use_reloader)
	
#-----------------------------------------------------------------------\
#
# helper functions
#
#-----------------------------------------------------------------------
def available_templates():
	pass


#-----------------------------------------------------------------------
class Page( object ):
	def __init__( self, name:str = None ):
		self.name 		= name
		self.methods	= [ "GET", "SET" ] 
		self._parent	= None
		self._children	= []
		self._routes	= []
		

	@property
	def route( self ):
		return "/%s" % self.name.lower()
		
	
	@property
	def parent( self ):
		return self._parent
		

	@parent.setter
	def parent( self, page ):
		self._parent = page


	def add_route( self, route:str ):
		self._routes.append( route )


	def wrapper_function( self, *args, **kwargs ):
		result = self.function( *args, **kwargs )
		if isinstance( result, Template ):
			return render_template( result.html_template, page = self, config = config, data = result.data ) 

		elif isinstance( result, Redirect ):
			# moet nog een manier verzinnen om arguments toe te voegen
			return redirect( result.url )
		
		else:
			return results


	def function( self ):
		return Template( "test", self.name )


#-----------------------------------------------------------------------
#
#
#
#-----------------------------------------------------------------------
class Data( object ):
	def __init__( self, content ):
		self.__blueprint	= None
		self.__content 		= content
		self.__keys			= None
		self.__keys_set		= False
		
		
	@property
	def content( self ):		
		if self.is_list:
			if len( self.__content ) > 0 and isinstance( self.__content[ 0 ], database.Document ):
				return [ item.as_html() for item in self.__content ]
					# ~ yield item.as_html()
			else:
				return [ item for item in self.__content ]
					# ~ yield item
					
		elif self.is_dict:
			if isinstance( self.__content, database.Document ):
				return self.__content.as_html()
			else:
				return self.__content
				

	@property
	def is_list( self ):
		return isinstance( self.__content, list )


	@property
	def is_dict( self ):
		return isinstance( self.__content, dict )


	@property
	def keys( self ):
		return self.__keys


	@property
	def blueprint( self ):
		return self.__blueprint

		
	@blueprint.setter
	def blueprint( self, blueprint:database.Document ):
		self.__blueprint = blueprint
		self.set_keys( [ key for key in blueprint.as_html().keys() ] )


	@property
	def has_keys( self ):
		return isinstance( self.__keys, list )


	def set_keys( self, keys ):
		self.__keys 	= keys
		self.__keys_set = True


#-----------------------------------------------------------------------
#
#
#
#-----------------------------------------------------------------------
class Template():
	def __init__( self, template:str = "default", data:Data = None ):
		self.__html_template	= template
		self.__data				= data


	@property
	def html_template( self ):
		return "%s.html" % self.__html_template


	@property
	def data( self ):
		return self.__data	
	

#-----------------------------------------------------------------------
class FormTemplate():
	def __init__( self, template:str = "form", data:Data = None ):
		# ~ check if template is a form
		self.__html_template	= template
		self.__data				= data


	@property
	def html_template( self ):
		return "%s.html" % self.__html_template


	@property
	def data( self ):
		return self.__data



#-----------------------------------------------------------------------
class Redirect():
	def __init__( self, url:str = "test", data:Data = None ):
		self.__url 		= url
		self.__data		= data
		
	@property
	def url( self ):
		return  "/%s" % self.__url
		return url_for( "/%s" % self.__url )
	
	@property
	def data( self ):
		return self.__data


#-----------------------------------------------------------------------
def create_route( page:Page ):
	func_name 		= "%s_function" % page.name
	try:
		routes = [ item for item in page._routes ]
		routes.insert( 0, page.route )
		for route in routes:
			server.add_url_rule( route, func_name, page.wrapper_function, methods = page.methods )
			server.view_functions[ route ] = page.wrapper_function
		print( "Created route(s) for: %s " % page.route )
	
	except Exception as e:
		print( "Error creating route(s) for: %s " % page.route )
		print( str( e ) )


