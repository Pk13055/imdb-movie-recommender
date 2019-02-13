import json

from flask import (Blueprint, abort, flash, g, jsonify, redirect,
                   render_template, request, session, url_for)

import app.home.helper as helper
from app import db, models, requires_auth

home = Blueprint('home', __name__, url_prefix='/home')


@home.route('/', methods = ['GET'])
def home_route():
	context_kwargs = {
		'title': "Homepage",
		'data': db.movies.find()
	}
	return render_template('home/index.html.j2', **context_kwargs)


@home.route('/movies/<imdbid>/', methods = ['GET'])
@requires_auth
def mov_info(imdbid):
	movie = db.movies.find_one( {"imdbID" : imdbid})
	if movie is None:
		abort(404)
	top_info = ['Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Language']
	more_info = ['Awards', 'imdbVotes', 'imdbID', 'Website', 'Production', 'Country']
	genres = [ 'action', 'animation', 'comedy', 'documentary', 'drama', 'horror', 'crime', 'romance', 'sci-fi']
	genres = [(cat, val) for cat, val in zip(genres, movie['onehot'])]
	ratings = movie['Ratings']
	context_kwargs = {
		'title': "MovieInfo",
		'movie' : movie,
		'top_info': top_info,
		'more_info': more_info,
		'genres' : genres,
		'ratings': ratings,
	}
	return render_template('home/movie.html.j2', **context_kwargs)
