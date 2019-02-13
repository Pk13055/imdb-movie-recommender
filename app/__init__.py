from functools import wraps

# Import flask and template operators
from flask import Flask, render_template,session, blueprints,jsonify, redirect
from flask_wtf.csrf import CSRFProtect,CSRFError
import pymongo

from config import MONGO_URI

# Define the WSGI application object
app = Flask(__name__, static_url_path = '/static')
client = pymongo.MongoClient(MONGO_URI)
DATABASE = MONGO_URI.split('/')[-1]
db = client[DATABASE]

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers

# csrf protection
csrf=CSRFProtect(app)
@app.errorhandler(CSRFError)
def csrf_error(reason):
    # return jsonify(success=True,error=reason)
    return render_template('error.html.j2', error=reason), 400

# HTTP error handling route
@app.errorhandler(404)
def not_found(error):
	return render_template('error.html.j2', error=error) , 404

# authorization for the logged in state
# modify this according to your needs
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if 'user_uid' not in session:
			return redirect('/user/signin/')
		return f(*args, **kwargs)
	return decorated

@app.route('/', methods=['GET'])
def main_route():
	return redirect('/movies/')

# Import a module / component using its blueprint handler variable (mod_auth)
from app.home.controller import home
from app.user.controller import user

# Register blueprint(s)
app.register_blueprint(home)
app.register_blueprint(user)

