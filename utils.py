"""
File: my_script.py
Author: Barkın Saday
Date: 15.03.2024
Description: Contain some utility functions that are needed for other functions
"""
import os
from git import Repo as GitRepo

def find_code_files_util(directory):
    """
    @Description: Utility function for finding filepaths of code files that is in a directory
    :param directory: Head Directory path as string to start searching from
    :return: Path of program files (can be in wrong format)
    """
    python_files = []

    # Iterate over all files and directories within the given directory
    for root, dirs, files in os.walk(directory):
        # Filter out directories starting with '.'
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        # Filter out Python files and add them to the list
        for file in files:
            if (file.endswith('.py') or file.endswith('.cpp') or file.endswith('.h') or file.endswith('.js') or
            file.endswith('.c') or file.endswith('.rb') or file.endswith('.r')):
                python_files.append(os.path.join(root, file))
    # print(python_files)
    return python_files


def find_code_files(directory):
    """
    :param directory: Head Directory path as string to start searching from
    :return: A list of file paths as string that are program files (.py, .cpp, .c, etc...)
    """
    python_files = find_code_files_util(directory)
    res = []
    for file_path in python_files:
        components = file_path.split("\\")
        components.pop(0)

        # Join the remaining components back into a path
        file_path = "\\".join(components)
        res.append(file_path)
    return res

# Change path type to match with other path
def path_reverse_slash(path):
    return path.replace("\\", "/")


def clone_repo_branch(repo, branch_name="main"):
    """
    :param repo: takes a GitHub repo object
    :param branch_name: branch to clone, default -> "main"
    :return: git.Repo object
    """
    clone_path = "clone" + "_" + repo.name + "_" + branch_name
    # Clone the Branch
    if os.path.exists(clone_path):
        clone = GitRepo(clone_path)
        return clone
    print("Pulling...")
    clone = GitRepo.clone_from(repo.clone_url, clone_path, branch=branch_name)
    return clone

def get_diff_header(diff):
    headers = []
    for line in diff.splitlines():
        if line.startswith("@@"):
            headers.append(line)
    return headers


