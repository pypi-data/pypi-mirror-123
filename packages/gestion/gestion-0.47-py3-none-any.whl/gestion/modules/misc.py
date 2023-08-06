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


