import os
from pydriller import RepositoryMining
from arguments import parser
from generate_csv import csv_report

def get_modified_files(commit, file_extension):
    """
    Only consider modified files with extension 'file_extension'
    in a particular commit
    """
    modified_files = [mod_file for mod_file in commit.modifications 
                        if any(f in mod_file.filename for f in file_extension)]
    return modified_files

def function_signature(method, params_dict):
    """
    Returns the signature of the function which includes:
    the name of the class the method belongs to, name of the method
    and its parameters and their type 
    """
    return params_dict[method.name][1]

def fetch(commit, modified_files, existing_methods):

    current_methods = dict()
    data_to_add = list()

    for modified_file in modified_files:  
        for method in modified_file.methods: 
            current_methods[method.name] = (set(method.parameters), 
                                            method.long_name)
            
            # Compare the number of parameters of existing methods 
            # in this commit vs previous commit
            if method.name in existing_methods.keys():
                num_of_prev_params = len(existing_methods[method.name][0])
                num_of_curr_params = len(current_methods[method.name][0])
                
                if num_of_curr_params > num_of_prev_params:
                    
                    # get function signatures and filename
                    filename = modified_file.filename
                    old_signature = function_signature(method, existing_methods)
                    new_signature = function_signature(method, current_methods)

                    entry = [commit.hash, filename, old_signature, new_signature]
                    data_to_add.append(entry)

    return current_methods, data_to_add

def get_commits_in_CSV(args):
    """
    Main function to mine commits which add a function argument 
    from a given git repository into a csv file.
    """
    repo_path = args.repo_path
    file_extension = args.file_extension.split(",") # to split if multiple extensions are passed
    existing_methods = dict()
    csv_data = list()

    for commit in RepositoryMining(repo_path, 
                    only_modifications_with_file_types=
                    file_extension).traverse_commits():
        
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