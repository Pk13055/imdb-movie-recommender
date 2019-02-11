from flask import (Blueprint, request, render_template,
                  flash, g, session, redirect, url_for, jsonify)
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
