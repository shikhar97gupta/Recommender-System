from wsgiref import headers
from flask import Flask, request, jsonify
import pandas as pd
import json
import time
import sys
import os
import RecommenderScriptFinal


sys.path.append('CollaborativeFiltering/')

from flask_cors import CORS

# init app
app = Flask(__name__)
CORS(app)

link_df = pd.read_csv("ml-latest-small/links.csv")


def get_movielensID_from_tmdbID(tmdbID):
    link_df = pd.read_csv("ml-latest-small/links.csv")
    row = link_df[link_df["tmdbId"] == tmdbID]
    if (len(row["movieId"]) == 0):
        return -1
    return int(row["movieId"])



def get_tmdbID_from_movielensTD(ML_ID):
    link_df = pd.read_csv("ml-latest-small/links.csv")
    row = link_df[link_df["movieId"] == ML_ID]
    #print("-------------------row=", row)
    if (len(row["tmdbId"]) == 0):
        return -1
    try:
        return int(row["tmdbId"])
    except:
        return



def counvert_ratings_to_tuple_format(userID, user_ratings):
    # given the ratings in form of lists [tmdbID, rating] --> [ML_ID, ratind]
    temp_ratings = []
    for [tmdbID, rating] in user_ratings:
        # print("rating = ", rating)
        temp_ratings.append([userID, get_movielensID_from_tmdbID(tmdbID), rating])
    return temp_ratings


def add_user_to_dataset(userID, user_ratings):
    # userID --> actual userID
    # user_ratings = [ [ML_movieID, rating] ]
    ratings = pd.read_csv("ml-latest-small/ratings.csv")
    d = {"userId": [], "movieId": [], "rating": [], "timestamp": []}
    for rating in user_ratings:
        d["userId"].append("672")
        d["movieId"].append(rating[0])
        d["rating"].append(rating[1])
        d["timestamp"].append(time.time())
    d_df = pd.DataFrame(d)
    ratings = pd.concat([ratings, d_df], axis=0)
    ratings.to_csv("ml-latest-small/ratings.csv", index=False)
    return "672"


def reset_files():
    reset_ratings = pd.read_csv("reset_ratings.csv")
    reset_ratings.to_csv("ml-latest-small/ratings.csv", index=False)
    #print("Ratings file reset")


def colaborativeFiltering_ItemBased(userID, user_ratings):# user_ratings
    # the ids returned are from the movielens dataset
    recommendatons_movieLens = RecommenderScriptFinal.runItemBasedColaborativeFiltering(testSubject=userID, curr_user_ratings=user_ratings)
    #print(recommendatons_movieLens)
    recommendations_tmdb = []
    for recommendation in recommendatons_movieLens[-21:]:
        recommendations_tmdb.append(get_tmdbID_from_movielensTD(int(recommendation)))
    return recommendations_tmdb


@app.route("/")
def index():
    return "This is the home route"


@app.route("/recommendations/itemcolaborativefiltering", methods=["POST"])
def item_colaborativefiltering():
    userID = request.json["userID"]
    user_ratings = request.json["ratings"]
    #recommender_type = request.json["recommender_type"]
    #print("user id = ", userID)
    #print("user_ratings = ", user_ratings)
    #print("recommender_type = ", recommender_type)
    user_ratings = json.loads(user_ratings)
    user_ratings = counvert_ratings_to_tuple_format(userID, user_ratings)
    #print("user Rating in tuple format = ", user_ratings)
    #userID = add_user_to_dataset(userID, user_ratings)
    pd.DataFrame(user_ratings).to_csv('ml-latest-small/added_ratings.csv', header = False, mode='a', index = False)
    recommendations = colaborativeFiltering_ItemBased(userID, user_ratings) #user_ratings
    #print(recommendations)
    #reset_files()
    return jsonify(recommendations)


# RunServer
if __name__ == "__main__":
    app.run()