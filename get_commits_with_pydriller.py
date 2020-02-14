# TODO List:
# (1) add argv command line
# (2) Check all corner cases; if any
# (3) Modularize the code
# (4) scrap online github commit or from local git repo?
# (5) write code for generating CSV report (function signatures)
# (6) old and new function signature might be an issue

import os
from pydriller import RepositoryMining

from arguments import parser

def get_repo_path(url):
	repodir = url.split("/")[-1].split(".")[0]
	if not os.path.exists(repodir):
		os.system("git clone "+url)
	pwd = os.getcwd()
	repo_path = os.path.join(pwd, repodir)
	return repo_path

def get_current_modified_methods(commit, file_extension):
	"""
	"""
	current_modified_methods = dict()
	for modified_file in commit.modifications: # each 'mod' is a file that has been modified 
		if file_extension in modified_file.filename:  # required for considering only files with that extension
			for method in modified_file.methods: 
				current_modified_methods[method.name] = set(method.parameters)
	return current_modified_methods

def get_commits_in_CSV(args):
	"""
	"""
	repo_path = get_repo_path(args.url)
	commits = []
	existing_methods = dict()
	file_extension = args.file_extension
		
	for commit in RepositoryMining(repo_path, 
								   only_modifications_with_file_types=[file_extension]).traverse_commits():
		current_modified_methods = get_current_modified_methods(commit, file_extension)
		common_keys = existing_methods.keys() & current_modified_methods.keys()
		to_add = False
		for key in common_keys:
			if len(current_modified_methods[key]) > len(existing_methods[key]):
				to_add = True
				break
		if(to_add):
			commits.append(commit)
		for key, value in current_modified_methods.items():
			existing_methods[key] = value
	
	for c in commits:
		print(c.msg)

	# commit csv file

if __name__=="__main__":
	args = parser.parse_args() 	 
	get_commits_in_CSV(args)