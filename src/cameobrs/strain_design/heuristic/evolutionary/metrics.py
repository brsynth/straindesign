from __future__ import absolute_import

from math import sqrt


def euclidean_distance(wt, mutant):
    return sqrt(sum([(wt[r] - mutant[r]) ** 2 for r in list(wt.keys())]))


def manhattan_distance(wt, mutant):
    return sum([(wt[r] - mutant[r]) for r in list(wt.keys())])
