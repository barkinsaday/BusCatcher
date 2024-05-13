from flask import Flask, request, jsonify
from flask_cors import CORS
from github import Github
import config
import utils
import File_History
import Algorithms

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes and all origins by default

@app.route('/analyze', methods=['POST'])
def analyze_repo():
    data = request.json
    repo_name = data.get('repo_name')
    branch_name = data.get('branch_name', 'main')  # Default to 'main' if not specified

    if not repo_name:
        return jsonify({"error": "Repository name is required"}), 400

    my_token = config.GITHUB_TOKEN
    g = Github(my_token)
    try:
        github_repo = g.get_repo(repo_name)
        # Clone the repo and get the branch object
        clone_path = utils.clone_repo_branch(github_repo, branch_name)
        # Assuming clone_repo_branch returns the path and you still need the branch object:
        branch = github_repo.get_branch(branch_name)  # Get the specific branch object if needed
        files_to_blame = utils.find_code_files(clone_path)

        # Retrieve file and author information
        total_details = {}
        for file in files_to_blame:
            line_authors = File_History.get_file_line_authors(branch, file)  # Now branch should be valid
            authors_scores = Algorithms.m1_last_takes_all(line_authors)
            total_details[file] = authors_scores
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(total_details)

if __name__ == '__main__':
    app.run(debug=True)

