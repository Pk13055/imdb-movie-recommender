import json
import hashlib

from flask import (Blueprint, abort, flash, g, jsonify, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import app.user.helper as helper
from app import db, models, requires_auth, csrf

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/signup/', methods=['GET', 'POST'])
def signup_route():
	if request.method == "POST":
		email = request.form['email']
		existing = db.users.find_one({'email' : email })
		if existing:
			flash('User already exists!')
		else:
			picture = f"https://www.gravatar.com/avatar/{hashlib.md5(email.encode()).hexdigest()}?s=200&d=identicon&r=PG"
			data = {
				'name': request.form['name'],
				'email': email,
				'age': request.form['age'],
				'gender': request.form['gender'],
				'password': generate_password_hash(request.form['password']),
				'picture': picture,
				'Genre': {
					'liked': [],
					'disliked': [],
				},
				'ratings': []
			}
			db.users.insert_one(data)
			session['user_uid'] = email
			return redirect(url_for('user.profile_route'))
	context_kwargs = {
		'title': "Signup",
		'include_nav': False,
	}
	return render_template('user/signup.html.j2', **context_kwargs)

@user.route('/', methods=['GET','POST'])
@requires_auth
def profile_route():
	user = db.users.find_one({'email': session['user_uid']})
	categories = ['name', 'email', 'age', 'gender']
	genres = ["Animation", "Family", "Drama", "Sport", "Comedy", "Romance","Crime",
			"Mystery", "Film-Noir", "Biography", "Western", "Horror", "Musical","Action",
			"Adventure", "Music", "War", "Fantasy", "History", "Thriller", "Sci-Fi"]

	if request.method == "POST":
		new_list = request.form.getlist('updatedList[]')
		liked = 'liked' if request.form['likedOrNot'] == 'true' else 'disliked'
		db.users.update_one({
			'_id': user['_id']
		},{
			'$set': {
				f'Genre.{liked}': new_list
			}
		}, upsert=True)
		user = db.users.find_one({'email': session['user_uid']})

	data = db.movies.find({
		'raters': {
			'$elemMatch': {
				'name': 'id',
				'value': session['user_uid']
			}
		}
	})

	context_kwargs = {
		'title': f"User - {user['name']}",
		'include_nav': True,
		'user' : user,
		'categories': categories,
		'genres': genres,
		'user_liked': user['Genre']['liked'],
		'user_disliked': user['Genre']['disliked'],
		'data': data
	}
	return render_template('user/profile.html.j2', **context_kwargs)




@user.route('/signin/', methods=['GET', 'POST'])
def signin_route():
	if request.method == "POST":
		email = request.form['email']
		exists = db.users.find_one({ 'email' : email })
		if exists and check_password_hash(exists['password'], request.form['password']):
			session['user_uid'] = request.form['email']
			return redirect(url_for('user.recommend_route'))
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
	return redirect(url_for('main_route'))


@user.route('/recommend/', methods=['GET', 'POST'])
@requires_auth
def recommend_route():
	user = db.users.find_one({'email': session['user_uid']})
	already_rated = db.users.aggregate([{ '$match': { 'email': session['user_uid'] }}, { '$project': { '_id': 0, 'ratings': { '$map': {
                    'input': "$ratings",
                    'as': "rating",
                    'in': "$$rating.id" }}}}])
	if request.method == "POST":
		req_type = request.form['type']
		movie_set = helper.process_movie(user, req_type)
		return jsonify({
			'status': True,
			'data': movie_set,
			'ratings': user['ratings'],
			'type': req_type
		})
	context_kwargs = {
		'title': "Recommendations",
		'include_nav': True,
		'data': movies,
		'user' : user,
	}
	return render_template('user/recommend.html.j2', **context_kwargs)
