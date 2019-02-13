# IMDB Movie Recommender System

## Overview

- Required categories:
    - Title
    - Thumbnail
    - Year
- Various genres (_the genres used as part of this dataset can be found in
  `genres.json`_)

## Datasets

- MovieLens
- http://www.omdbapi.com/

The file `data_final.json` houses the 173 movie database that we'll be using for
the recommender system.

### Loading the database

To load the database, just run the `mongoimport` command to read form the JSON.
```bash
mongoimport --db <db_name> --collection movies --file data_final.json --jsonArray --drop
```

### Loading the users

- The users have been precreated and stored in the `users.json` file.
- Additionally, you can use the `gen_users.py` to generate new users as well
```bash
mongoimport --db <db_name> --collection users --file users.json --jsonArray
```

## Recommender System

- K movies input ratings
- Additionally harness user data (location, gender, etc)

- User user collaborative filtering
- item item collaborative filtering
- matrix factorization
