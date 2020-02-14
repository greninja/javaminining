# import os
# url1 = "https://github.com/HouariZegai/Calculator.git"
# os.system("git clone "+url1)

# sys.argv

import os
from pydriller import RepositoryMining
dir1 = "Calculator"

pwd = os.getcwd()
repo_path = os.path.join(pwd, dir1)

commits = []
existing_methods = dict()

for commit in RepositoryMining(repo_path, only_modifications_with_file_types=['.java']).traverse_commits():
	current_modified_methods = dict()
	for modified_file in commit.modifications: # each 'mod' is a file that is modified in the current commit
		if '.java' in modified_file.filename:  # this is required to check if the file that has been modified is java file or not
			for method in modified_file.methods: 
				current_modified_methods[method.name] = set(method.parameters)

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

# intersection = set(current_modified_methods).intersection(set(existing_methods))
# methods_to_add = set(current_modified_methods) - intersection
# for method_name in methods_to_add:
# 	existing_methods[method_name] = current_modified_methods[method_name]	