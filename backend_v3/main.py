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
github_repo = g.get_repo("hydralauncher/hydra")
branches = github_repo.get_branches()
for branch in branches:
    print(branch)

# Clone GitHub Repo - optional change or add branches
branch_name = "main"
print(branch_name)
clone_path = "clone" + "_" + github_repo.name + "_" + branch_name
branch = utils.clone_repo_branch(github_repo, branch_name)
print("Clone Repo-Branch Path: " + clone_path)

# Get Python Files to Blame
files_to_blame = utils.find_code_files(clone_path)
print(files_to_blame)

#Get all contributers
contributers = github_repo.get_contributors()
number_of_contributers = contributers.totalCount
print("Number of Contributors: ", number_of_contributers)

# Number of total lines:
total_num_of_lines = 0
total_prim = []
total_second = []

for file in files_to_blame:
    print("=========================================="+file+"===============================================")
    line_authors = File_History.get_file_line_authors(branch, file)
    num_of_lines_in_file = len(line_authors)
    print("Number of Lines in file: ", num_of_lines_in_file)
    total_num_of_lines += num_of_lines_in_file
    print(line_authors) # See the authors
    authors_scores1 = Algorithms.m1_last_takes_all(line_authors)
    authors_scores2 = Algorithms.m2_split_equal(line_authors)
    author_scores3 = Algorithms.m3_weighted_changes(line_authors)
    print("------------------------ Method 1 -----------------------------")
    for author, score in authors_scores1.items():
        print(f"Author: {author}, Score: {score}")
    print("------------------------ Method 2 -----------------------------")
    for author, score in authors_scores2.items():
        print(f"Author: {author}, Score: {score}")
    print("------------------------ Method 3 -----------------------------")
    for author, score in author_scores3.items():
        print(f"Author: {author}, Score: {score}")
    pr, sc = Algorithms.get_prim_and_second_authors(line_authors)
    print(pr)
    print(sc)
    total_prim += pr
    total_second += sc

#Get project-scaled scores
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
print("Primary Author List: ", total_prim)
print("Secondary Author List:", total_second)
print("Total Number of Lines: ", total_num_of_lines)
print("Total number of Contributors: ", number_of_contributers)
print("Total Author Scores: ", file_scores)
print("Normalized: ", normalized_scores)
print("Bus Factor: ", Algorithms.get_bus_factor_authors(normalized_scores, files_to_blame, number_of_contributers))
#  Get remaining limit of requests from PyGithub
print(g.get_rate_limit())

"""

test: hydralauncher/hydra (>1dk), unjs/nitro (4-5 dk), PyGithub/PyGithub (8-9 dk)

Frontendten backende gidecek endpointler:
1. path
2. name
3. owner
4. github token
5. number of users for clusters
6. method id

Backendten dönmesi beklenen output kısmı enpointler:
1. generated summary text (parameters only)
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
10.bus factor number

app = Flask(_name_)
CORS(app)  # This enables CORS for all routes and all origins by default

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:")
    print(f"Path: {data.get('path')}")
    print(f"Name: {data.get('name')}")
    print(f"Owner: {data.get('owner')}")
    print(f"GitHub Token: {data.get('githubToken')}")
    print(f"Number of Users for Clusters: {data.get('numUsers')}")
    print(f"Method ID: {data.get('methodId')}")

    response = {
        "summary": {
            "number of contributors": 5,
            "file extension": ".py",
            "bus factor name": "Python"
        },
        "user cluster data": [
            {"name": "Developer A", "percentage": 50},
            {"name": "Developer B", "percentage": 30},
            {"name": "Developer C", "percentage": 20}
        ],
        "branch list": ["master", "dev"],
        "directory list": ["src", "dist"],
        "file list": ["main.py", "utils.py"],
        "line count": 1024,
        "method id": data.get('methodId'),
        "developer count": 3,
        "bus factor name": "Python",
        "bus factor number": 1
    }
    return jsonify(response)

if _name_ == '_main_':
    app.run(debug=True)
"""

