# IMDB Movie Recommender System

- Required categories:
    - Title
    - Thumbnail
    - Year
- Rating, etc up to
  [us](https://medium.com/netflix-techblog/recommending-for-the-world-8da8cbcf051b)

- Around 200
- Various genres

## Datasets

- MovieLens
- http://www.omdbapi.com/

The file `data_final.json` houses the 173 movie database that we'll be using for
the recommender system.

## Loading the database

To load the database, just run the `mongoimport` command to read form the JSON.
```bash
mongoimport --db <db_name> --collection movies --file data_final.json --jsonArray
```

## Recommender

- K movies input ratings
- Additionally harness user data (location, gender, etc)

- User user collaborative filtering
- item item collaborative filtering
- matrix factorization
