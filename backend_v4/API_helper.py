from github import Github

import Algorithms
import File_History
import utils
import config
from git import Repo as GitRepo


def get_Branches(github_repo):
    return github_repo.get_branches()


# def get_Clone_Branch(github_repo):
#     return utils.clone_repo_branch(github_repo)

def get_Files_to_Blame(clone_path):
    return utils.find_code_files(clone_path)


def get_Contributer_Count(github_repo):
    contributers = github_repo.get_contributors()
    return contributers.totalCount


def get_Prim_Second_LineCount(github_repo, files_to_blame, method=3):
    """
    @return: local_prim, local_second, total_prim, total_second, total_line_count
    """
    total_num_of_lines = 0
    total_prim = []
    total_second = []
    local_prim = {}  # for file
    local_second = {}  # for file

    print("AAAAAAAAAAAAAAAAAAAA:", files_to_blame)
    for file in files_to_blame:
        print("XXXX:", file)
        line_authors = File_History.get_file_line_authors(github_repo, file)
        num_of_lines_in_file = len(line_authors)
        total_num_of_lines += num_of_lines_in_file
        if method == 1:
            pr, sc = Algorithms.get_prim_and_second_authors(line_authors, 1)
        elif method == 2:
            pr, sc = Algorithms.get_prim_and_second_authors(line_authors, 2)
        else:
            pr, sc = Algorithms.get_prim_and_second_authors(line_authors, 3)

        local_prim[file] = pr
        local_second[file] = sc
        total_prim += pr
        total_second += sc
        return local_prim, local_second, total_prim, total_second, total_num_of_lines


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
    # Access Token
    my_token = github_token  # Can put your own token instead

    # GitHub Repo
    g = Github(my_token)
    github_repo = g.get_repo(owner + "/" + repo_name)
    branches = github_repo.get_branches()

    # Clone GitHub Repo - optional change or add branches
    branch_name = "main"
    # clone_path = "clone" + "_" + github_repo.name + "_" + branch_name
    branch = utils.clone_repo_branch(github_repo, branch_name)
    branches = [branch.name for branch in github_repo.get_branches()]

    # Get Python Files to Blame
    files_to_blame = utils.find_code_files(clone_path)

    # Get all contributers
    contributers = github_repo.get_contributors()
    number_of_contributers = contributers.totalCount

    # Number of total lines:
    total_num_of_lines = 0
    total_prim = []
    total_second = []
    local_prim = {}
    local_second = {}

    for file in files_to_blame:
        line_authors = File_History.get_file_line_authors(branch, file)
        num_of_lines_in_file = len(line_authors)
        total_num_of_lines += num_of_lines_in_file
        pr, sc = Algorithms.get_prim_and_second_authors(line_authors, method_id)
        local_prim[file] = pr
        local_second[file] = sc
        total_prim += pr
        total_second += sc

    # Get project-scaled scores
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

    bus_factor = get_Bus_Factor(normalized_scores)

    response_data = {
        "total_lines": total_num_of_lines,
        "total_contributors": number_of_contributers,
        "bus_factor_data": bus_factor,
        "bus_factor_count": len(bus_factor),
        "files_analyzed": files_to_blame,
        "branches": branches,
        "method": method_id
    }
    return response_data




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
