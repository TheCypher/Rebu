from app import db

class Users(db.Model):
	
	__tablename__ = 'users'
	id = db.Column('id', db.Integer, primary_key=True)
	firstname = db.Column('firstname', db.String(80), unique=True)
	lastname = db.Column('lastname', db.String(80), unique=True)
	email = db.Column('email', db.String(80), unique=True)
	password = db.Column('password', db.String(80))
	registered_on = db.Column('registered_on', db.DateTime)

	def __init__(self, **user):
		self.firstname = user['firstname']
		self.lastname = user['lastname']
		self.email = user['email']
		self.password = user['password']
