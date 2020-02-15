# TODO List:
# (2) Check all corner cases; if any   NOT DONE
# branch commits?

import os
from pydriller import RepositoryMining
from arguments import parser
from generate_csv import csv_report

def get_modified_files(commit, file_extension):
    """
    Only consider modified files with extension 'file_extension'
    """
    modified_files = [f for f in commit.modifications if file_extension in f.filename]
    return modified_files

def function_signature(method, params_dict):
    """
    """
    return params_dict[method.name][1]         

def fetch(commit, modified_files, existing_methods):
    """
    """
    current_methods = dict()
    data_to_add = list()

    for modified_file in modified_files:  
        for method in modified_file.methods: 
            current_methods[method.name] = (set(method.parameters), 
                                            method.long_name)
            
            # checking if a new argument has been added to any method 
            # by comparing the number of parameters in this commit
            # vs previous commit and repeating it for all methods.
            if method.name in existing_methods.keys():
                num_of_prev_params = len(existing_methods[method.name][0])
                num_of_curr_params = len(current_methods[method.name][0])
                
                if num_of_curr_params > num_of_prev_params:
                    
                    # get function signatures
                    old_signature = function_signature(method, existing_methods)
                    new_signature = function_signature(method, current_methods)

                    t = [commit.hash, modified_file.filename, 
                         old_signature, new_signature]
                    data_to_add.append(t)

    return current_methods, data_to_add

def get_commits_in_CSV(args):
    """
    Main function to mine commits which add a function argument 
    from a given git repository into a csv file.
    """
    repo_path = args.repo_path
    file_extension = args.file_extension
    existing_methods = dict()
    csv_data = list()

    for commit in RepositoryMining(repo_path, 
                    only_modifications_with_file_types=
                    [file_extension]).traverse_commits():
        
        # fetch files with extension 'file_extension' that were modified 
        # in the current commit
        modified_files = get_modified_files(commit, file_extension)
        
        # fetch methods with updated set of parameters and data to
        # add to a csv file (if new function parameters were added)
        current_methods, data_to_add = fetch(commit, 
                                             modified_files,
                                             existing_methods)
        # update existing methods       
        for key, value in current_methods.items():
            existing_methods[key] = value

        # accumulating data to be added to csv report
        for d in data_to_add:
            csv_data.append(d)
    
    # generate csv report
    csv_report(repo_path, csv_data)

if __name__=="__main__":
    args = parser.parse_args()      
    get_commits_in_CSV(args)