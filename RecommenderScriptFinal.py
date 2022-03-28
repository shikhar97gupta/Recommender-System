
#request below
#{'recommender_type': '"itemBasedCF"', 'userID': '"6225fd130e1cf306f061fd19"', 'ratings': '[[634649,4],[566525,2],[24428,4],[109445,4]]'}#

import numpy as np
import pandas as pd
import math
import demoMF 
from utils import quickselect
from utils import quicksort
from utils import binarySearch
#import dask.dataframe as dd
#from sklearn.utils.extmath import randomized_svd
#from sklearn.decomposition import TruncatedSVD

path_ratings = 'ml-latest-small/ratings.csv'
path_movies = 'ml-latest-small/movies.csv'

rating_df = pd.read_csv(path_ratings)
movie_df = pd.read_csv(path_movies)

combine_movie_rating = pd.merge(rating_df, movie_df, on='movieId')

columns = ['timestamp', 'genres', 'title']
user_movie_rating = combine_movie_rating.drop(columns, axis=1)

def removeDuplicates(indices, recomm):
    for index in indices:
        while True:
            try:
                recomm.remove(index)
            except ValueError:
                break
    return recomm

def add_added_ratings(user_movie_rating):
    path_added_ratings = 'ml-latest-small/added_ratings.csv'
    added_ratings_df = pd.read_csv(path_added_ratings)
    user_movie_rating = pd.concat([user_movie_rating,added_ratings_df])
    return user_movie_rating

def data(user_movie_rating):
    user_movie_rating.drop_duplicates(['userId','movieId'], keep='last', inplace=True)
    rating_pivot = user_movie_rating.pivot(index = 'userId', columns = 'movieId', values = 'rating').fillna(0)
    X = rating_pivot.values
    objMF = demoMF.ExplicitMF(X,20,0.1,0.1,verbose=True)
    objMF.train(5)
    U = objMF.user_vecs
    V = objMF.item_vecs
    V.shape
    matrix = V
    print("Matrix: ", matrix.shape)
    corr = np.corrcoef(matrix)
    movie_ids = rating_pivot.columns
    movie_ids_list = list(movie_ids)
    return corr, movie_ids_list, rating_pivot

#print(corr)
def runSingleItem(corr, movie_ids_list, movie_index):
    coffey_hands = movie_ids_list.index(movie_index)
    corr_coffey_hands  = list(corr[coffey_hands])
    k = 10
    n_corr = len(corr_coffey_hands)-1
    quickselect.kthLargest(corr_coffey_hands, movie_ids_list, 0, n_corr - 1, k)
    selected_corr = corr_coffey_hands[:k]
    selected_movie_ids = movie_ids_list[:k]
    return selected_movie_ids, selected_corr


def runFullItem(corr, movie_ids_list, indices):
    movieIds = []
    corrs = []
    for index in indices:
        selected_movie_ids, selected_corr = runSingleItem(corr, movie_ids_list, index)
        movieIds.extend(selected_movie_ids)
        corrs.extend(selected_corr)
    quicksort.quicksort(corrs, movieIds, 0, len(corrs) - 1)
    i1 = binarySearch.binarySearch(corrs, 0, len(corrs)-1, 1.0)
    corrs = corrs[:i1]
    movieIds = movieIds[:i1]
    return movieIds

def runItemBasedColaborativeFiltering(testSubject, user_movie_rating=user_movie_rating):
    user_movie_rating = add_added_ratings(user_movie_rating)
    user_movie_rating['userId'] =  user_movie_rating['userId'].astype(str)
    corr, movie_ids_list, rating_pivot = data(user_movie_rating)
    user_data = rating_pivot.loc[testSubject]
    indices = list(user_data[1:].index[user_data[1:]>0])
    recomm = runFullItem(corr, movie_ids_list, indices)
    print("Recomm: ",recomm)
    processed_recomm = removeDuplicates(indices, recomm)
    print("Processed recomm: ",processed_recomm)
    return processed_recomm
    

#print(runItemBasedColaborativeFiltering(1)[-21:])
