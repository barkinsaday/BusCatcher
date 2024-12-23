
from github import Github

import Algorithms
import File_History
import utils
import config

def get_Repo(local_path):
    github_repo = g.get_repo(local_path)
    return github_repo
def get_Branches(github_repo):
    return github_repo.get_branches()

def get_Clone_Branch(github_repo):
    return utils.clone_repo_branch(github_repo)

def get_Files_to_Blame(clone_path):
    return utils.find_code_files(clone_path)

def get_Contributer_Count(github_repo):
    contributers = github_repo.get_contributors()
    return contributers.totalCount

def get_TOTAL_Prim_Second_LineCount(github_repo, files_to_blame, method=3):
    total_num_of_lines = 0
    total_prim = []
    total_second = []
    for file in files_to_blame:
        line_authors = File_History.get_file_line_authors(get_Clone_Branch(github_repo), file)
        num_of_lines_in_file = len(line_authors)
        total_num_of_lines += num_of_lines_in_file
        if method == 1:
            pr, sc = Algorithms.get_prim_and_second_authors(line_authors, 1)
        elif method == 2:
            pr, sc = Algorithms.get_prim_and_second_authors(line_authors, 2)
        else:
            pr, sc = Algorithms.get_prim_and_second_authors(line_authors, 3)

        total_prim += pr
        total_second += sc
        return total_prim, total_second, total_num_of_lines

def get_Project_Scores(total_prim, total_second):
    file_scores = {}
    for author in total_prim:
        if author in file_scores:
            file_scores[author] += 1
        else:
            file_scores[author] = 1

    for author in total_second:
        if author in file_scores:
            file_scores[author] += 1
        else:
            file_scores[author] = 1
    normalized_scores = utils.normalize_scores(file_scores)
    return normalized_scores

def get_Bus_Factor(normalized_scores):
    return Algorithms.get_bus_factor_authors(normalized_scores)

def API(clone_path, owner, repo_name, github_token, method_id):
    # GitHub Repo
    g = Github(github_token)
    github_repo = g.get_repo(owner+"/"+repo_name)
    number_of_contriboters = get_Contributer_Count(github_repo)
    branches = get_Branches(github_repo)

    files_to_blame = get_Files_to_Blame(clone_path)
    total_prim, total_second, total_num_of_lines = get_TOTAL_Prim_Second_LineCount(github_repo, files_to_blame, method_id)
    normalized_scores = get_Project_Scores(total_prim, total_second) # Clustered Data
    bus_factor = get_Bus_Factor(normalized_scores)

    print("Primary Author List: ", total_prim)
    print("Secondary Author List:", total_second)
    print("Total Number of Lines: ", total_num_of_lines)
    print("Total number of Contributors: ", number_of_contriboters)
    print("Normalized Score: ", normalized_scores) # Clustered Data
    print("Bus Factor Cluster Data: ", bus_factor)
    print("Bus Factor Number: ", len(bus_factor))


'''
Param:
 1. path
2. name
3. owner
4. github token
5. number of users for clusters
6. method id

Return:
a. number of contributors
    b. file extension
    c. bus factor name
2. user cluster data
    a. name
    b. percentage
3. branch list
4. directory list
5. file list
6. line count
7. method id
8. developer count
9. bus factor name (repeated, can be omitted)
10. bus factor number
'''