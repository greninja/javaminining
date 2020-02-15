# TODO List:
# (1) add argv command line -			 DONE
# (2) Check all corner cases; if any	 NOT DONE
# (3) Modularize the code -			     DONE
# (4) scrap online github commit or from local git repo? 
# (5) write code for generating CSV report (function signatures);  
#	  Available: {commit hash, filename, (name+parameters, public/private, return_type) }
# (6) create a requirements.txt file for installation
# (7) write README.md

import os
import csv
import pprint
from pydriller import RepositoryMining

from arguments import parser

# def get_repo_path(url):
#	 repodir = url.split("/")[-1].split(".")[0]
#	 if not os.path.exists(repodir):
#		 os.system("git clone "+url)
#	 pwd = os.getcwd()
#	 repo_path = os.path.join(pwd, repodir)
#	 return repo_path

def get_modified_files(commit, file_type):
	"""
	Only consider modified files with extension 'file_type'
	"""
	modified_files = [f for f in commit.modifications if file_type in f.filename]
	return modified_files

def fetch(commit, modified_files, existing_methods):
	"""
	"""
	current_methods = dict()
	data_to_add = list()

	for modified_file in modified_files:  
		for method in modified_file.methods: 
			current_methods[method.name] = (set(method.parameters), method.long_name)
			
			# checking if a new argument has been added to any method 
			# by comparing the number of parameters for each method
			# with previous commit 
			if method.name in existing_methods.keys():
				num_of_params_prev = len(existing_methods[method.name][0])
				num_of_params_curr = len(current_methods[method.name][0])
				if num_of_params_curr > num_of_params_prev:
					old_function_signature = existing_methods[method.name][1]
					new_function_signature = current_methods[method.name][1]
					t = [commit.hash[:7], modified_file.filename, \
								old_function_signature, new_function_signature]
					data_to_add.append(t)

	return current_methods, data_to_add

def get_commits_in_CSV(args):
	"""
	Main function to mine commits which add a function argument 
	from a given git repository into a csv file.
	"""
	repo_path = args.repo_path
	file_type = args.file_type
	existing_methods = dict()
	csv_data = list()

	for commit in RepositoryMining(repo_path, 
					only_modifications_with_file_types=
					[file_type]).traverse_commits():
		
		# fetch files with extension 'file_type' that were modified 
		# in the current commit
		modified_files = get_modified_files(commit, file_type)
		
		# fetch methods with updated set of parameters and data to 
		# add to a csv file (if new function parameters were added)
		current_methods, data_to_add = fetch(commit, 
										  	 modified_files,
										  	 existing_methods)
		# update existing methods	   
		for key, value in current_methods.items():
			existing_methods[key] = value

		# Add data from current commit to csv file
		for d in data_to_add:
			csv_data.append(d)
	
	# write to a csv file
	with open("out.csv", "w", newline="") as f:
		 writer = csv.writer(f)
		 writer.writerows(csv_data)

if __name__=="__main__":
	args = parser.parse_args()	  
	get_commits_in_CSV(args)