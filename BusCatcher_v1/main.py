"""
File: my_script.py
Author: Barkın Saday
Date: 15.03.2024
Description: Calculates developer knowledge on a project (acts as main for now).
"""
from github import Github

import Algorithms
import File_History
import utils
import config

# Access Token
my_token = config.GITHUB_TOKEN  # Can put your own token instead

# GitHub Repo
g = Github(my_token)
github_repo = g.get_repo("PyGithub/PyGithub")
branches = github_repo.get_branches()

# Clone GitHub Repo - optional change or add branches
branch_name = "main"
print(branch_name)
clone_path = "clone" + "_" + github_repo.name + "_" + branch_name
branch = utils.clone_repo_branch(github_repo, branch_name)
print("Clone Repo-Branch Path: " + clone_path)

# Get Python Files to Blame
files_to_blame = utils.find_code_files(clone_path)
print(files_to_blame)

for file in files_to_blame:
    print("=========================================="+file+"===============================================")
    line_authors = File_History.get_file_line_authors(branch, file)
    # print(line_authors)
    authors_scores1 = Algorithms.m1_last_takes_all(line_authors)
    authors_scores2 = Algorithms.m2_split_equal(line_authors)
    author_scores3 = Algorithms.m3_weighted_changes(line_authors)
    print("------------------------ Method 1 -----------------------------")
    for author, score in authors_scores1.items():
        print(f"Author: {author}, Count: {score}")
    print("------------------------ Method 2 -----------------------------")
    for author, score in authors_scores2.items():
        print(f"Author: {author}, Count: {score}")
    print("------------------------ Method 3 -----------------------------")
    for author, score in author_scores3.items():
        print(f"Author: {author}, Count: {score}")

#  Get remaining limit of requests from PyGithub
print(g.get_rate_limit())
