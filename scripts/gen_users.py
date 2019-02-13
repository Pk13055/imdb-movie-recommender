#!/usr/bin/env python3
"""
Average	    12 - 14	    14 - 24	    24-34   Ratio       Category        Male        Female      Ratio
15	        22	        8	        15	    1	        Animation	    75	        65	        1.153846154
33.5	    35	        32	        30	    1.1166      Comedy	        90	        91	        0.989010989
8.5	        5	        12	        11	    0.7727      Crime	        79	        84	        0.9404761905
4	        0.5	        7.5	        5.5	    0.7272      Horror	        57	        47	        1.212765957
40	        40	        40	        40	    1	        Action	        90	        86	        1.046511628
18	        18	        18	        18	    1	        SciFi	        76	        62          1.225806452
23.5	    20	        27	        27	    0.8703  	Drama	        80	        89	        0.8988764045
10.5        8	        13	        11	    0.9545  	Romance	        55	        77	        0.7142857143
"""
import json
import string
import random
from sys import argv as rd

from werkzeug.security import generate_password_hash

ran_n = lambda n: ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(n))


def gen_genres(n: int) -> list:
    """Generate the liked and disliked genres on the basis of statistics

    :param age: str -> 0/1 12 - 24 / 24 - 34
    :param gender: str -> male/female
    :param name_: str -> random name
    :return genres: dict -> liked and disliked
    """
    choices = [
        'Action',
        'Adventure',
        'Animation',
        'Biography',
        'Comedy',
        'Crime',
        'Drama',
        'Family',
        'Fantasy',
        'Film-Noir'
        'History',
        'Horror',
        'Music',
        'Musical',
        'Mystery',
        'Romance',
        'Sci-Fi',
        'Sport',
        'Thriller',
        'War',
        'Western',
    ]
    genres = []
    for _ in range(n):
        print(f"Building genres {_}/{n}", end="\r", flush=True)
        likes = set(random.sample(choices, random.randint(0, int(2 * len(choices) / 3))))
        dislikes = list(random.sample(list(set(choices) - likes), random.randint(0, int(len(likes) / 3))))
        genres.append({
            'liked': list(likes),
            'disliked': dislikes
        })
    return genres


def gen_users(n: int) -> dict:
    """Generate random users
    :param n: int -> number of users to generate
    :return users: dict -> set of users with unique emails
    {
        'email': 'abc@email.com',
        'password': 'abc',
        'name' : 'abc xyz',
        'gender' : 'male/female',
        'age' : '0/1',
    }
    """
    emails = ['gmail', 'yahoo', 'hotmail', 'icloud']
    genders = ['male', 'female']
    ages = ['0', '1']
    users = []
    genres = gen_genres(n)
    for _ in range(n):
        print(f"Building users {_}/{n}", end="\r", flush=True)
        name_ = ran_n(random.randint(5, 10))
        name = name_ + " " + ran_n(random.randint(5, 20))
        password = generate_password_hash(name_)
        email = f"{name_}@{random.choice(emails)}.com"
        age = ages[_ % 2]
        gender = genders[_ % 2]
        users.append({
            'email': email,
            'name': name,
            'age': age,
            'gender': gender,
            'password': password,
            'Genre': genres[_],
            'picture': f"https://www.gravatar.com/avatar/{ran_n(32)}?s=200&d=identicon&r=PG%22"
        })
    return users

def main():
    users = gen_users(int(rd[1]))
    json.dump(users, open('users.json', 'w'))

if __name__ == "__main__":
    main()
