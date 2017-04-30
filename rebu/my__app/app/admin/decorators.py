from functools import wraps

from flask import g, flash, redirect, url_for, request

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user is None:
			flash(u'Please sign in')
			return redirect(url_for('admin.login', next=request.path))	
		return f(*args, **kwargs)
	return decorated_function


def logged_in_already(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user:
			return redirect(url_for('admin.index'))
		return f(*args, **kwargs)
	return decorated_function
