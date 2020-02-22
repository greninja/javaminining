import os
import numpy as np
from pydriller import RepositoryMining

from cli_arguments import parser
from utils import csv_report, get_modified_files, get_frequency                                              
from entries import (get_entry_of_nonoverloaded_func, 
                     get_entries_of_overloaded_func)

def fetch(args, commit, current_modified_files, existing_methods):
    """
    Fetches csv entries.
    """
    data_to_add = list()

    for modified_file in current_modified_files: 
    
        # maintaining a dictionary to store info such as parameters, signatures, 
        # source code about methods present in modified file
        current_methods = dict() 
        
        old_path = modified_file.old_path # old file path of modified file
        new_path = modified_file.new_path # new file path of modified file
        source_code = modified_file.source_code # source code of modified file
        
        overloading = False # to detect if there is method overloading
        overloaded_keys = set() # to store the method names of overloaded methods

        # get frequency of each method beforehand in order to check overloading 
        method_frequencies = get_frequency(modified_file) 

        # iterate over each method in modified file to check if a new argument was added
        for method in modified_file.methods:

            method_name = method.name
            if method_name not in current_methods:
                current_methods[method_name] = []

            # fetching the source code of the method required for similarity
            # searching (if called for in the case of overloaded functions)                
            code_text = source_code[method.start_line:method.end_line]
            
            current_methods[method_name].append({'parameters': method.parameters,
                                                 'signature': method.long_name,
                                                 'source_code': code_text})

            # only check for addition of a new argument if old path exists in 
            # 'existing_methods' and if the current modified file was not deleted
            # in current commit (i.e. 'new_path' cannot be None)
            if old_path in existing_methods and new_path is not None: 
                if method_name in existing_methods[old_path]:
                    if (method_frequencies[method_name] > 1):
                        # Detected overloading (csv entries for overloaded functions
                        # are handled at the end after all the methods have been iterated
                        # over for current file; this is mainly because mapping of one 
                        # overloaded function from this commit to previous commit depends
                        # on what other overloaded functions are mapped to and hence it 
                        # requires to look at all such methods together)
                        overloading = True
                        overloaded_keys.add(method_name)
                    else:
                        entry = get_entry_of_nonoverloaded_func(commit,
                                                                old_path,
                                                                method.filename,
                                                                method_name,
                                                                existing_methods,
                                                                current_methods)
                        if entry is not None:
                            data_to_add.append(entry)
        
        # get csv entries of overloaded functions
        if(overloading):
            entries = get_entries_of_overloaded_func(args,
                                                     commit,
                                                     old_path,
                                                     method.filename,
                                                     overloaded_keys,
                                                     existing_methods,
                                                     current_methods)
            for entry in entries:
                data_to_add.append(entry)

        # Updating existing methods about current modified file
        if old_path is not None and old_path in existing_methods:
            if new_path is not None:
                if old_path != new_path:
                    # delete information about old file if its name or path was changed
                    del(existing_methods[old_path])
                existing_methods[new_path] = current_methods
            elif new_path is None: # file deleted in this commit
                del(existing_methods[old_path])
        else:
            #  'else' can lead to following cases:
            #  (a) if 'old_path' is 'None' implying file was added in current commit
            #  (b) if 'old_path' is not present in 'existing_methods'. This can
            #      happen in cases where the file was part of a merge conflict.
            #      This is because PyDriller does not parse through
            #      combined diffs to fetch information about methods affected by 
            #      merge conflicts and simply ignores them!
            #   In either of the above cases, just store information about the 
            #   methods present in current modified file in 'existing_methods'
            existing_methods[new_path] = current_methods

    return data_to_add

def get_commits(args):
    """
    Main function to mine commits
    """
    repo_path = args.repo_path
    file_extension = args.file_extension

    # dictionary to store snapshots of methods from previous commits 
    existing_methods = dict()
    
    # stores csv entries
    csv_data = list()

    for commit in RepositoryMining(repo_path, 
                                   only_modifications_with_file_types=
                                   [file_extension]).traverse_commits():

        # retrieve files with extn 'file_extension' that were modified in current commit
        current_modified_files = get_modified_files(commit, file_extension)
        
        # fetch entries for csv report 
        data_to_add = fetch(args, commit, current_modified_files, existing_methods)
        
        # accumulate csv report data
        for d in data_to_add:
            csv_data.append(d)

    # generate csv report
    csv_report(args, repo_path, csv_data)

if __name__=="__main__":
    args = parser.parse_args()      
    get_commits(args)