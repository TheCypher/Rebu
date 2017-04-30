import datetime
from time import strftime
from sqlalchemy import desc

from app import db

#dateNow = datetime.datetime.now()
dateNow = strftime("%a, %d %b %Y")

class Blogs(db.Model):
	__tablename__ = 'blogs'
	id  = db.Column('id', db.Integer, primary_key=True)
	title = db.Column('title', db.String(80))
	post = db.Column('post', db.String(255))
	blog_img = db.Column('blog_img', db.String(255))
	#posted_on = db.Column('posted_on', db.DateTime)
	posted_on = db.Column('posted_on', db.String(255))
	
	
	# param -> (self, dic)
	def __init__(self, **blog):
		if blog:
			self.title = blog['title']
			self.post = blog['post']
			self.blog_img = blog['blog_img']
			self.posted_on = dateNow


	# param -> (self, dic)
	def read(self, blog=False):
		if not blog:
			return self.query.order_by(desc('id'))
		
		return self.query.get(blog['id'])
	

	# param -> (self, dic)
	def update(self, blog):
		self.query.filter_by(id=blog['id']).update()
		db.session.commit()


	# param -> (self, dic)
	def delete(self, blog):
		self.query.filter_by(id=blog['id']).delete()
		db.session.delete(blog)
		db.session.commit()
