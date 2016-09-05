from sqlalchemy import (create_engine, Table, Column, Integer, String, MetaData)
import settings
import sys

#create a connection to the database
#format engine = create_engine('mysql://user:pasword@host/foo')
try:
	db = create_engine('mysql://daniel:dani@localhost/test')
	db.connect()
	print('uhul')
except:
	print('opps ', sys.exc_info()[1])
