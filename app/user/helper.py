import os
import sys
import random
import json
from bson.json_util import dumps

import numpy as np
import pandas as pd

from app import db


def user_user_filt(user):
	"""User-user collaborative filtering

	:param user: dict -> the current user
	:return recommend: list[dict] recommended movies
	"""
	genres = user['']
	return []


def item_item(user):
	"""item-item collaborative filtering

	:param user: dict -> the current user
	:return recommend: list[dict] recommended movies
	"""
	return []


def matrix_fact(user):
	"""Matrix factorization collaborative filtering

	:param user: dict -> the current user
	:return recommend: list[dict] recommended movies
	"""
	return []


def process_movie(user: dict, r_type: str, r_gen: bool=True) -> list:
	"""Process the user and type of request and recommend movies accordingly

	:param user: dict -> logged in user
	:param r_type: str -> user/item/matrix
	:return movies_recomend: list[dict] -> the recommended movies
	"""
	ratings = user['ratings']
	genres = user['Genre']
	liked, disliked = genres.values()
	if r_gen:
		movies = db.movies.aggregate([{ '$match': {
			'Genre': {
				'$in' : liked,
				'$nin': disliked,
				},
			'imdbID': {
				'$nin': list(ratings.keys())
			}}}, {
				'$sample': { 'size': 7 }
			}])
		return json.loads(dumps(movies))
	mappings = {
		'user': user_user_filt,
		'item': item_item,
		'matrix': matrix_fact
	}
	try:
		movies_recommend = mappings[r_type](user)
	except KeyError:
		movies_recommend = []
	return movies_recommend
