import os
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABSE_URL'))
else:
	DATABASE = SqliteDatabase('emptysills.sqlite')

class User(UserMixin, Model):
	email = CharField(unique=True)
	password = CharField()
	display_name = CharField()

	def __str__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	def __repr__(self):
		return '<User: {}, id: {}>'.format(self.email, self.id)

	class Meta:
		db_table = 'users'
		database = DATABASE

class Plant(Model):
	plant_id = IntegerField
	user = ForeignKeyField(User, backref='plants')  

	class Meta:
		db_table = 'plants'
		database = DATABASE

def initialize(): 
	DATABASE.connect()
	DATABASE.create_tables([User, Plant], safe=True)

	print("Database tables and data have been created")
	DATABASE.close()
