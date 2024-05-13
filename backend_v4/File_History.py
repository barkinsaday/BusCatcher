"""
File: my_script.py
Author: Barkın Saday
Date: 15.03.2024
Description: Check the authors of a file
Check: Currently looks at all line in all commit - try looking at diffs instead
"""
import re

def get_file_line_authors(repo, file):
    """
    :param repo: git.Repo object
    :param file: file path of a code file in the give repo
    :return: 2D array of Line_Authors[i][j] ->[ [author1, author2, author3...], [...], [...], ... ] where inner list
            corresponds to the line, both lines and authors are ordered
    """
    Line_Authors = []
    file_commits = list(repo.iter_commits(paths=file))  # Add skip=1 on diff version
    file_commits.sort(key=lambda x: x.committed_date, reverse=False)
    for commit in file_commits:
        try:
            blame = repo.git.blame("--line-porcelain", commit.hexsha, "--", file)
        except Exception as e:
            return []
        # prev_commit = repo.commit(commit.parents[0].hexsha)
        # diff = repo.git.diff(prev_commit.hexsha, commit.hexsha, "--", file)
        authors = re.findall(r'^author (.*)$', blame, re.MULTILINE)
        line_no = 0
        for author in authors:  # size of {authors} = size of {lines}
            if len(Line_Authors) <= line_no:  # New line to add, always append
                Line_Authors.append([author])
            else:
                inner_list_size = len(Line_Authors[line_no - 1])
                if Line_Authors[line_no - 1][inner_list_size - 1] != author:
                    Line_Authors[line_no - 1].append(author)
            line_no += 1
    return Line_Authors


'''
CHECK:  diff options (below)
GOAL: Instead of checking each line in each commit, check
        -Append Author_List from diff. 
        -Try to get diff in form of @@...@@ only (or a better version that gives direct access to modified lines).
        -Check lines from @@ and use blame with option (l1 or something) which gives blame for a single specific line
        -Use blame-l1 with value from @@ and change->AuthorList[@@-1] if author is different than last A_list[][-1]
        -Possible indexing problem: we do not look all lines one by one if commit2 has more lines than commit1 it is 
            possible to exceed the list size. since format @@-123, +123@ means -old, -new. For extra line there might
            not be a "-" and instead just @@+new@@ directly (or similar logic). In that case make use of that and append 
            AuthorList (on line scale, first index).
            
IDEA:   -If an option for only @@ is not found, use -U3 option and look every third line to get @@ only
        - "--numstat" show number of add/del, maybe useful for index problem (seems costly and hard)

common diff options:
  -z            output diff-raw with lines terminated with NUL.
  -p            output patch format.
  -u            synonym for -p.
  --patch-with-raw
                output both a patch and the diff-raw format.
  --stat        show diffstat instead of patch.
  --numstat     show numeric diffstat instead of patch.
  --patch-with-stat
                output a patch and prepend its diffstat.
  --name-only   show only names of changed files.
  --name-status show names and status of changed files.
  --full-index  show full object name on index lines.
  --abbrev=<n>  abbreviate object names in diff-tree header and diff-raw.
  -R            swap input file pairs.
  -B            detect complete rewrites.
  -M            detect renames.
  -C            detect copies.
  --find-copies-harder
                try unchanged files as candidate for copy detection.
  -l<n>         limit rename attempts up to <n> paths.
  -O<file>      reorder diffs according to the <file>.
  -S<string>    find filepair whose only one side contains the string.
  --pickaxe-all
                show all files diff when -S is used and hit is found.
  -a  --text    treat all files as text.  
'''
