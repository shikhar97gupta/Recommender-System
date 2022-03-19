import numpy as np
import pandas as pd
import demoMF
from utils import quickselect
from utils import quicksort
from utils import binarySearch


'''
#corr = pd.read_csv("D:\Kaggle\VS\Git\Recommender-System\Recommendercorr.csv")
movie_user_rating_pivot = pd.read_csv("D:\Kaggle\VS\Git\Recommender-System\RecommenderPivot.csv")
print(movie_user_rating_pivot.head())
movie_ids = movie_user_rating_pivot.columns[1:]
movie_ids_list = list(map(int,movie_ids))
corr = list(corr.values)

def runSingleItem(corr, movie_ids_list, index):

    coffey_hands = movie_ids_list.index(index)
    corr_coffey_hands  = list(corr[coffey_hands])
    k = 10
    n_corr = len(corr_coffey_hands)-1
    quickselect.kthLargest(corr_coffey_hands, movie_ids_list, 0, n_corr - 1, k)
    selected_corr = corr_coffey_hands[:k]
    selected_movie_ids = movie_ids_list[:k]
    #quicksort.quicksort(selected_corr, selected_movie_ids, 0, len(selected_corr) - 1)
    return selected_movie_ids, selected_corr

def runFullItem(corr, movie_ids_list, indices):
    movie_ids = []
    corrs = []
    for index in indices:
        selected_movie_ids, selected_corr = runSingleItem(corr, movie_ids_list, index)
        movie_ids.extend(selected_movie_ids)
        corrs.extend(selected_corr)
    #print(corrs[-21:])
    #print(movie_ids[-21:])
    quicksort.quicksort(corrs, movie_ids, 0, len(corrs) - 1)
    #print("after QuickSort")
    #print(corrs[-21:])
    #print(movie_ids[-21:])
    i1 = binarySearch.binarySearch(corrs, 0, len(corrs)-1, 1.0)
    corrs = corrs[:i1]
    movie_ids = movie_ids[:i1]
    return movie_ids

def runItemBasedColaborativeFiltering(testSubject):
    user_data = movie_user_rating_pivot.loc[testSubject]
    indices = list(user_data[1:].index[user_data[1:]>0])
    indices = list(map(int,indices))
    return runFullItem(corr, movie_ids_list, indices)

#len(movie_user_rating_pivot.loc[1].values)
#user_data = movie_user_rating_pivot.loc[0]
#print(user_data.index[1:][user_data>0])
#mIds = runItemBasedColaborativeFiltering(2)
#print(corrs[-21:])
#print(mIds[-21:])

''' 
