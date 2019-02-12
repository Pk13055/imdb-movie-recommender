from flask import (Blueprint, request, render_template,
                  flash, g, session, redirect, url_for, jsonify, abort)
from app import db, models
import app.home.helper as helper


home = Blueprint('home', __name__, url_prefix='/home')


@home.route('/', methods = ['GET'])
def home_route():
	context_kwargs = {
		'title': "Homepage",
		'data': db.movies.find()
	}
	return render_template('home/index.html.j2', **context_kwargs)


@home.route('/movies/<imdbid>', methods = ['GET'])
def mov_info(imdbid):
	movie = db.movies.find_one( {"imdbID" : imdbid})
	if movie is None:
		abort(404) 
	context_kwargs = {
		'title': "MovieInfo",
		'movie' : movie,
	}
	return render_template('home/movinfo.html.j2', **context_kwargs)