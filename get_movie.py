import pandas as pd
import sys 

params = sys.argv[1]

def get_movie(movie_id):
    frame = pd.read_csv('data/movies.csv')
    result = frame[frame['MovieID']==movie_id]
    return result['Title'].values[0] + result['Genres'].values[0]

params = int(params)
print(get_movie(params))


