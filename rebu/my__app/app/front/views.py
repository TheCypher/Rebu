from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from passlib.hash import pbkdf2_sha256

from app import db
from app.front.models import Users
#from app.admin.models import Blogs

mod = Blueprint('', __name__, url_prefix="")


@mod.route('/', methods=['GET'])
@mod.route('/index', methods=['GET'])
def index():
	"""Home page"""
	page = {
		'title': "Polite",
	}
	return render_template('front/index.html', page=page)


@mod.route('/register', methods=['GET', 'POST'])
def register():
	"""Register page"""
	page = {
		'title': 'Register',
		'big_title': 'Register',
		'small_title': ''
	}

	if request.method != 'POST':
		return render_template('front/register.html', page=page)
	
	user_data = {
		'firstname':request.form['firstname'],
		'lastname':request.form['lastname'],
		'email':request.form['email'],
		'password':request.form['password']
	}
	print(user_data)

	for key, value in user_data.items():
		if value == '':
			page['error'] = 'All fields must be filled'
			return render_template('front/register.html', page=page)

	user_email = {
		'email':request.form['email']
	}
	user_data.pop('password')
	user = Users.query.filter_by(**user_email).first()

	if user:
		page['error'] = 'Aready a account under this email'
		return render_template('front/register.html', page=page)

	user_data['password'] = pbkdf2_sha256.encrypt(request.form['password'], rounds=200000, salt_size=16)
	
	user = Users(**user_data)
	db.session.add(user)
	db.session.commit()
	session['user_id'] = user.id
	return redirect(url_for('.index'))


@mod.route('/logout', methods=['GET'])
def logout():
	"""Logout page"""
	session['user_id'] = ''
	return redirect(url_for('.index'))
