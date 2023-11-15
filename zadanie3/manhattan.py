# https://en.wikipedia.org/wiki/Taxicab_geometry
# https://www.analyticsvidhya.com/blog/2020/02/4-types-of-distance-metrics-in-machine-learning/
# https://numpy.org/doc/stable/index.html

import numpy as np


def manhattan_score(dataset, user1, user2):
    """
                Parameters:
                    dataset (dict): File with data, json format
                    user1 (str): User to compare
                    user2 (str): User to compare
                Return:
                    result (list): Return calculated distance
        """
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    # If there are no common movies between the users,
    # then the score is 0
    if len(common_movies) == 0:
        return 0

    result = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            result.append(np.fabs(dataset[user1][item] - dataset[user2][item]))

    return np.sum(result)
