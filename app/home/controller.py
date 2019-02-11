from flask import (Blueprint, request, render_template,
                  flash, g, session, redirect, url_for, jsonify)
from app import mongo, models
import app.home.helper as helper


home = Blueprint('home', __name__, url_prefix='/home')


@home.route('/', methods = ['GET'])
def home_route():
	movies = [_ for _ in mongo.db.movies.find()]
	print(movies)
	context_kwargs = {
		'title': "Homepage",
		'data': movies
	}
	return render_template('home/index.html.j2', **context_kwargs)
