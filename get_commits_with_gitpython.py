"""
pip3 install gitpython==2.1.7
"""
import os
from git import Repo

url1 = "https://github.com/greninja/NPLM.git"
dir1 = "NPLM"

os.system("git clone "+url1)
pwd = os.getcwd()
repo_path = os.path.join(pwd, dir1)

repo = Repo(repo_path)
commits = list(repo.iter_commits('master'))
check_keywords = ["add", "paramter"]
final_commits = []
for commit in commits:
	if all(x in commit.message for x in check_keywords):
		final_commits.append(commit)	
print(final_commits)

# take a java github repo and see what the commits for adding parameters are like