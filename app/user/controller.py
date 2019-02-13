import json
import hashlib

from flask import (Blueprint, abort, flash, g, jsonify, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import app.user.helper as helper
from app import db, models, requires_auth

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/', methods=['GET'])
@requires_auth
def userpage_route():
	user = db.users.find_one({'email': session['user_uid']})
	categories = ['name', 'email', 'age', 'gender']
	context_kwargs = {
		'title': f"User - {user['name']}",
		'include_nav': True,
		'user' : user,
		'categories': categories,
	}
	return render_template('user/profile.html.j2', **context_kwargs)

@user.route('/signup/', methods=['GET', 'POST'])
def signup_route():
	if request.method == "POST":
		email = request.form['email']
		picture = f"https://www.gravatar.com/avatar/{hashlib.md5(email.encode()).hexdigest()}?s=200&d=identicon&r=PG"
		data = {
			'name': request.form['name'],
			'email': email,
			'age': request.form['age'],
			'gender': request.form['gender'],
			'password': generate_password_hash(request.form['password']),
			'picture': picture
		}
		existing = db.users.find_one({'email' : email })
		if existing:
			flash('User already exists!')
		else:
			db.users.insert_one(data)
			session['user_uid'] = email
			return redirect('/user/recommend/')
	context_kwargs = {
		'title': "Signup",
		'include_nav': False,
	}
	return render_template('user/signup.html.j2', **context_kwargs)


@user.route('/signin/', methods=['GET', 'POST'])
def signin_route():
	if request.method == "POST":
		email = request.form['email']
		exists = db.users.find_one({ 'email' : email })
		if exists and check_password_hash(exists['password'], request.form['password']):
			session['user_uid'] = request.form['email']
			return redirect('/user/recommend/')
		else:
			flash("Incorrect email/password combination")

	context_kwargs = {
		'title': "signin",
		'include_nav': False,
	}
	return render_template('user/signin.html.j2', **context_kwargs)


@user.route('/signout/', methods=['GET', 'POST'])
@requires_auth
def signout_route():
	if 'user_uid' in session:
		session.pop('user_uid')
	return redirect('/')


@user.route('/recommend/', methods=['GET', 'POST'])
@requires_auth
def recommend_route():
	# TODO: add recommendation analysis here
	context_kwargs = {
		'title': "Recommendations",
		'include_nav': True,
	}
	return render_template('user/recommend.html.j2', **context_kwargs)
