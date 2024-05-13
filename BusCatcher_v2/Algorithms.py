"""
File: my_script.py
Author: Barkın Saday
Date: 15.03.2024
Description: Contains algorithms to assess a score to authors
Note: Check method3, logic not quite right (100e tamamlamıyo)
"""
from collections import defaultdict

def m1_last_takes_all(line_authors):
    authors_scores = defaultdict(float)
    for line in line_authors:
        for author in line: # To add non-last contributor with 0 score
            authors_scores[author] += 0
        authors_scores[line[-1]] += 1.0
    total = sum(authors_scores.values())
    for key, val in authors_scores.items():
        authors_scores[key] = val / total * 100.0
    return authors_scores


def m2_split_equal(line_authors):
    authors_scores = defaultdict(float)
    for line in line_authors:
        for author in line:
            authors_scores[author] += 1.0
    total = sum(authors_scores.values())
    for key, val in authors_scores.items():
        authors_scores[key] = val / total * 100.0
    return authors_scores


def m3_weighted_changes(line_authors):
    authors_scores = defaultdict(float)
    for line in line_authors:
        weight = 1.0
        for author in line:
            authors_scores[author] += weight
            weight += 1.0
    for key, val in authors_scores.items():
        total = sum(authors_scores.values())
        authors_scores[key] = val / total * 100.0
    return authors_scores

def get_prim_and_second_authors(line_authors, method=None):
    if method is None:
        author_scores = m3_weighted_changes(line_authors)
    prim_authors = []
    second_authors = []
    for author in author_scores:
        author_count = len(author_scores)
        if author_scores[author] >= 100/author_count:
            prim_authors.append(author)
        elif author_scores[author] >= 50/author_count:
            second_authors.append(author)
    return prim_authors, second_authors

#Takes dictionary of {author:score}, takes list of all code files, takes total num of contributers
def get_bus_factor_authors(file_scores, files, number_of_contributers):
    bus_factor = []
    for author in file_scores:
        if file_scores[author] >= len(files)/len(file_scores):
            bus_factor.append(author)
    return bus_factor

'''
10 file




'''






