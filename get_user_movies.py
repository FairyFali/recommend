import pandas as pd
import sys 

params = sys.argv[1]

def get_movie(movie_id):
    frame = pd.read_csv('data/movies.csv')
    result = frame[frame['MovieID']==movie_id]
    return result['Title'].values[0] + result['Genres'].values[0]


def get_movies(movie_ids):
    return [get_movie(i) for i in movie_ids]


def get_user_movies(user_id):
    frame = pd.read_csv('data/Ratings.csv')
    return list(frame[frame['UserID'] == user_id]['MovieID'])

params = int(params)
print(get_movies(get_user_movies(params)))


