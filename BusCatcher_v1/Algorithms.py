"""
File: my_script.py
Author: Barkın Saday
Date: 15.03.2024
Description: Contains algorithms to assess a score to authors
Note: Check method3, logic not quite right
"""
from collections import defaultdict

def m1_last_takes_all(line_authors):
    authors_scores = defaultdict(float)
    for line in line_authors:
        authors_scores[line[-1]] += 1
    total = sum(authors_scores.values())
    for key, val in authors_scores.items():
        authors_scores[key] = val / total * 100
    return authors_scores


def m2_split_equal(line_authors):
    authors_scores = defaultdict(float)
    for line in line_authors:
        for author in line:
            authors_scores[author] += 1
    total = sum(authors_scores.values())
    for key, val in authors_scores.items():
        authors_scores[key] = val / total * 100
    return authors_scores


def m3_weighted_changes(line_authors):
    authors_scores = defaultdict(float)
    for line in line_authors:
        weight = 1
        for author in line:
            authors_scores[author] += weight
            weight += 1
    for key, val in authors_scores.items():
        total = sum(authors_scores.values())
        authors_scores[key] = val / total * 100
    return authors_scores
