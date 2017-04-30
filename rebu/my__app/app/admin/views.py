from flask import Blueprint, request, render_template, flash, g, session, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
from functools import wraps

from app import db
from app.admin.models import Blogs
from app.front.models import Users
from .decorators import login_required, logged_in_already
from .file_upload import file_upload

mod = Blueprint('admin', __name__, url_prefix="/admin")

@mod.before_request
def before_request():
	"""
	pull user's profile from the database before every request are treated
	"""
	g.user = None
	g.blogs = None
	BlogClass = Blogs()
	if 'user_id' in session:
		g.user = Users.query.get(session['user_id'])
		g.blogs = BlogClass.read()


@mod.route('/login', methods=['GET', 'POST'])
@logged_in_already
def login():
	"""Login page"""
	page = {
		'title': 'Login',
		'big_title': 'Admin Login',
		'small_tile': ''
	}

	if request.method != 'POST':
		return render_template('front/login.html', page=page)
	
	user_data = {
		'email':request.form['email'],
		'password': request.form['password']
	}

	for key, value in user_data.items():
		if value == '':
			page['error'] = 'All fields must be filled'
			return render_template('front/login.html', page=page)

	user_data.pop('password')
	user = Users.query.filter_by(**user_data).first()
	user_data['password'] = request.form['password']

	if not user or not  pbkdf2_sha256.verify(user_data['password'], user.password):
		page['error'] = 'Wrong email or password'
		return render_template('admin/login.html', page=page)

	session['user_id'] = user.id
	return redirect(url_for('admin.index'))


@mod.route('/', methods=['GET', 'POST'])
@mod.route('/home', methods=['GET', 'POST'])
@login_required
def index():
	"""Home page"""
	page = {
		'title': 'RebU',
		'name': 'Dashboard'
	}
	return render_template('admin/index.html', page=page)

@mod.route('/mygroup', methods=['GET', 'POST'])
@login_required
def my_group():
	"""My group page"""
	page = {
		'title': 'My Group',
		'name': 'My Group'
	}
	return render_template('admin/my_group.html', page=page)

@mod.route('/browse', methods=['GET', 'POST'])
@login_required
def browse():
	"""Browse Groups"""
	page = {
		'title': 'Browse Groups',
		'name': 'Browse Groups'
	}
	return render_template('admin/browse_groups.html', page=page)

@mod.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
	"""Calendar"""
	page = {
		'title': 'Calendar',
		'name': 'Calendar'
	}
	return render_template('admin/calendar.html', page=page)

@mod.route('/nearme', methods=['GET', 'POST'])
def nearme():
	"""Near me"""
	page = {
		'title': 'Near me',
		'name': 'Cars near me'
	}
	return render_template('admin/near_me.html', page=page)

@mod.route('/logout', methods=['GET'])
def logout():
	"""Logout page"""
	session['user_id'] = ''
	return redirect(url_for('admin.login'))


@mod.route('/write', methods=['GET', 'POST'])
@login_required
def write():
	"""Write a blog"""
	page = {
		'title':'Write blog'
	}

	if request.method != 'POST':
		return render_template('admin/write_blog.html', page=page)

	blog_data = {
		'title':request.form['title'],
		'post': request.form['blog'],
		'blog_img': 'none'
	}

	for key, value in blog_data.items():
		if value == '':
			page['error'] = 'Please fill all fields'
			return render_template('admin/write_blog.html', page=page)

	blog_data['blog_img'] = ''
	blog_img = request.files['blog_img']
	if blog_img.filename != '':
		if file_upload(blog_img):
			blog_data['blog_img'] = blog_img.filename
	
	blog = Blogs(**blog_data)
	db.session.add(blog)
	db.session.commit()
	return redirect(url_for('admin.index'))


@mod.route('/edit_blog/<int:blog_id>/', methods=['GET', 'POST'])
#@mod.route('/edit_blog', methods=['GET', 'POST'])
@login_required
def edit(blog_id):
	"""Edit blog"""
	blog_id = 1

	page = {
		'title':'Edit blog'
	}

	blog = Blogs.query.filter_by(id=blog_id).first()

	if not blog:
		page['error'] = 'This blog does not exist'
		return redirect(url_for('admin.index'))

	if request.method != 'POST':
		page['blog'] = blog.post
		print(page)
		return render_template('admin/edit.html', page=page)
		#return render_template('admin/edit.html', page=page)

	page['blog'] = blog
	return render_template('admin/write_blog.html', page=page)
	 
