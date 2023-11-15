# Author: Kamil Kornatowski
# Author: Adrian Paczewski

# IMDB API reference: https://imdbpy.readthedocs.io/en/latest/

# pip install git+https://github.com/cinemagoer/cinemagoer
# pip install cinemagoer
# pip install numpy

# movie recommendation engine based on two counting methods : manhattan and euclidean

import json
import numpy as np
from imdb import Cinemagoer

from euclidean import euclidean_score
from manhattan import manhattan_score


# Finds users in the dataset that are similar to the input user
def find_similar_users(dataset, user, num_users):
    """
        Find similar users.
            Parameters:
                dataset (dict): File with data, json format
                user (str): User to compare
                num_users (int): Number of users

            Return:
                scores (dict): Return similar users

    """
    if user not in dataset:
        raise TypeError('Cannot find ' + user + ' in the dataset')

    # Compute score between input user
    # and all the users in the dataset

    # euclidean score
    scores = np.array([[x, euclidean_score(dataset, user,
                                            x)] for x in dataset if x != user])

    # manhattan score
    #scores = np.array([[x, manhattan_score(dataset, user,
     #                                      x)] for x in dataset if x != user])

    # Sort the scores in decreasing order
    scores_sorted = np.argsort(scores[:, 1])[::-1]

    # Extract the top 'num_users' scores
    top_users = scores_sorted[:num_users]

    return scores[top_users]


# Print recommended movies in console
def print_recommended_movies():
    print('\nRecommended movies : ')
    for i in recommended_movies:
        print('* ' + i)
        movies = ia.search_movie(i)
        movie = ia.get_movie(movies[0].movieID)
        print(' - year: ' + str(movie['year']))

        if 'rating' in movie:
            print(' - rating: ' + str(movie['rating']))
        else:
            print(' - rating: no data')

        if 'votes' in movie:
            print(' - votes: ' + str(movie['votes']))
        else:
            print(' - votes: no data')


        box_office = ''
        if 'box office' in movie:
            box_office = movie['box office']['Budget']
        else:
            box_office = ' no data '
        print(' - box office: ' + box_office)

        if 'director' in movie:
            for director in movie['directors']:
                print(' - director: ' + director['name'])
        else:
            print(' - director: no data')


if __name__ == '__main__':

    user = 'Kamil Kornatowski'

    ratings_file = 'movies.json'

    # Create connection to IMDB API
    ia = Cinemagoer()

    with open(ratings_file, 'r', encoding="UTF-8") as f:
        data = json.loads(f.read())
    similar_users = find_similar_users(data, user, 12)

    best_match_movies = data[similar_users[0][0]]
    user_movies = data[user]
    diff_dict = {}

    for key in best_match_movies.keys():
        if key not in user_movies.keys():
            diff_dict[key] = best_match_movies[key]

    # Sorting dict by values
    diff_dict = {k: v for k, v in sorted(diff_dict.items(), key=lambda item: item[1], reverse=True)}

    print("\nResults for user " + user)
    recommended_movies = list(diff_dict.keys())[:5]
    print_recommended_movies()

    not_recommended_movies = list(reversed(diff_dict.keys()))[:5]
    print('\nNot recommended movies : ')
    for j in not_recommended_movies:
        print(' - ' + j)
