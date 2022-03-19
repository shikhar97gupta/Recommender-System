
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import demoMF 
from utils import quickselect
from utils import quicksort
from utils import binarySearch
#import dask.dataframe as dd
#from sklearn.utils.extmath import randomized_svd
#from sklearn.decomposition import TruncatedSVD

path_ratings = 'ml-latest-small/ratings.csv'
path_movies = 'ml-latest-small/movies.csv'

#df_gscore = dd.read_csv(gspath)
#df_gtag = dd.read_csv(gtpath)
#df_tags = pd.read_csv(path_tags)
rating_df = pd.read_csv(path_ratings)
movie_df = pd.read_csv(path_movies)

combine_movie_rating = pd.merge(rating_df, movie_df, on='movieId')

columns = ['timestamp', 'genres']
combine_movie_rating = combine_movie_rating.drop(columns, axis=1)
combine_movie_rating.head(10)

movie_ratingCount = (combine_movie_rating.
     groupby(by = ['movieId'])['rating'].
     count().
     reset_index().
     rename(columns = {'rating': 'totalRatingCount'})
     [['movieId', 'totalRatingCount']]
    )

rating_with_totalRatingCount = combine_movie_rating.merge(movie_ratingCount, left_on = 'movieId', right_on = 'movieId', how = 'left')

user_rating = rating_with_totalRatingCount.drop_duplicates(['userId','movieId'])

movie_user_rating_pivot = user_rating.pivot(index = 'userId', columns = 'movieId', values = 'rating').fillna(0)

#movie_user_rating_pivot.to_csv("D:\Kaggle\VS\Git\Recommender-System\RecommenderPivot.csv")

X = movie_user_rating_pivot.values
#dim = movie_user_rating_pivot.shape
#dim

objMF = demoMF.ExplicitMF(X,60,0.1,0.1,verbose=True)
objMF.train(10)

U = objMF.user_vecs
V = objMF.item_vecs
V.shape

matrix = V
corr = np.corrcoef(matrix)
#corr = pd.DataFrame(corr)
#corr.to_csv("D:\Kaggle\VS\Git\Recommender-System\Recommendercorr.csv", index= False)

#movie_title = movie_user_rating_pivot.columns
#movie_title_list = list(movie_title)
movie_ids = movie_user_rating_pivot.columns
movie_ids_list = list(movie_ids)
#print(corr)
def runSingleItem(corr, movie_ids_list, index):
    #print("Movie_id_len: ",len(movie_ids_list))
    #print("Index: ",index)
    coffey_hands = movie_ids_list.index(index)
    #print("Index2: ", coffey_hands)
    corr_coffey_hands  = list(corr[coffey_hands])
    k = 10
    n_corr = len(corr_coffey_hands)-1
    quickselect.kthLargest(corr_coffey_hands, movie_ids_list, 0, n_corr - 1, k)
    selected_corr = corr_coffey_hands[:k]
    selected_movie_ids = movie_ids_list[:k]
    #quicksort.quicksort(selected_corr, selected_movie_ids, 0, len(selected_corr) - 1)
    return selected_movie_ids, selected_corr


def runFullItem(corr, movie_ids_list, indices):
    movieIds = []
    corrs = []
    for index in indices:
        selected_movie_ids, selected_corr = runSingleItem(corr, movie_ids_list, index)
        movieIds.extend(selected_movie_ids)
        corrs.extend(selected_corr)
    #print(corrs[-21:])
    #print(movie_ids[-21:])
    quicksort.quicksort(corrs, movieIds, 0, len(corrs) - 1)
    #print("after QuickSort")
    #print(corrs[-21:])
    #print(movie_ids[-21:])
    i1 = binarySearch.binarySearch(corrs, 0, len(corrs)-1, 1.0)
    corrs = corrs[:i1]
    movieIds = movieIds[:i1]
    return movieIds

def runItemBasedColaborativeFiltering(testSubject):
    user_data = movie_user_rating_pivot.loc[testSubject]
    indices = list(user_data[1:].index[user_data[1:]>0])
    indices = list(map(int,indices))
    #print(indices)
    return runFullItem(corr, movie_ids_list, indices)

print(runItemBasedColaborativeFiltering(1)[-21:])

'''
watch.reset()
watch.start()
k = 100
n_corr = len(corr_coffey_hands)-1
for i in range(n_corr, n_corr-k,-1):
    mx = 0
    for j in range(i+1):
        if (corr_coffey_hands[j]>=corr_coffey_hands[mx]):
            mx = j
    corr_coffey_hands[mx], corr_coffey_hands[i] = corr_coffey_hands[i], corr_coffey_hands[mx]
    #movie_ids[mx], movie_ids[i] = movie_ids[i], movie_ids[mx]
watch.stop()
watch.duration
movie_ids[n_corr-10:n_corr]
'''