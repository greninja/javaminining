import numpy as np
from cosine_sim import get_cosine

def get_entry_of_nonoverloaded_func(commit, old_path, filename, method_name,
                                    existing_methods, current_methods):
    """
    Uses a combination of file path and method name as access keys to fetch
    information about non-overloaded methods from `existing` and `current` methods 
    dictionaries in order to compare the number of arguments. 

    Returns the csv entry of the method if new arguments are added to it.
    """
    entry = None
    num_of_prev_params = len(existing_methods[old_path][method_name][0]['parameters'])
    num_of_curr_params = len(current_methods[method_name][0]['parameters'])

    # Compare num of parameters of the method in current commit vs previous commit
    if num_of_curr_params > num_of_prev_params:
        
        # get function signatures
        old_signature = existing_methods[old_path][method_name][0]['signature']
        new_signature = current_methods[method_name][0]['signature']

        # entry for CSV report
        entry = [commit.hash, filename, old_signature, new_signature, 'No']

    return entry

def get_entries_via_sort_and_map(commit, old_path, filename, overloaded_keys, 
                                 existing_methods, current_methods):
    """
    Sorts the signatures of overloaded methods in two different commmits  
    and then maps one-to-one in that sorted order. 

    Returns the csv entries of all the overloaded methods of a modified file.
    """
    entry_data = []
    
    for overloaded_key in overloaded_keys:

        prevmethods = existing_methods[old_path][overloaded_key]
        currmethods = current_methods[overloaded_key]

        # sort the list of dictionaries
        prevmethods = sorted(prevmethods, key = lambda i: i['signature'], 
                             reverse=True)           
        currmethods = sorted(currmethods, key = lambda i: i['signature'], 
                             reverse=True)

        for (prevmethod, currmethod) in zip(prevmethods, currmethods):
            num_of_prev_params = len(prevmethod['parameters'])
            num_of_curr_params = len(currmethod['parameters'])

            if num_of_curr_params > num_of_prev_params:
                
                # get function signatures
                old_signature = prevmethod['signature']
                new_signature = currmethod['signature']

                # entry for CSV reports
                entry = [commit.hash, filename, old_signature, new_signature, 'Yes']
                entry_data.append(entry)
    
    return entry_data            

def get_entries_via_similarity_map(commit, old_path, filename, overloaded_keys, 
                                      existing_methods, current_methods):
    """
    Computes cosine similarity between source code (text) of overloaded 
    functions in current commit with those from previous commits. The function 
    from previous commit are mapped to the one in current commit with maximum 
    similarity.  
    """
    entry_data = []

    for overloaded_key in overloaded_keys:  
        curr_methods = current_methods[overloaded_key].copy()
        for prev_method in existing_methods[old_path][overloaded_key]:
            if len(curr_methods) > 0:
                similarity_scores = []
                
                # get the method from current methods which is maximally similar
                # to prev_method
                for curr_method in curr_methods:
                    prev_source_code = prev_method['source_code']
                    curr_source_code = curr_method['source_code']
                    similarity = get_cosine(prev_source_code, curr_source_code)
                    similarity_scores.append(similarity)
                max_similar = np.argmax(similarity_scores)
                
                num_of_prev_params = len(prev_method['parameters'])
                num_of_curr_params = len(curr_methods[max_similar]['parameters'])

                if num_of_curr_params > num_of_prev_params:
                    
                    # get signatures
                    old_signature = prev_method['signature']
                    new_signature = curr_methods[max_similar]['signature']

                    entry = [commit.hash, filename, old_signature, new_signature, 'Yes']
                    entry_data.append(entry)

                # delete the current method which had highest similarity 
                del(curr_methods[max_similar])

    return entry_data          

def get_entries_of_overloaded_func(args, commit, old_path, filename, overloaded_keys,
                                   existing_methods, current_methods):
    """
    Fetches entries for csv report from overloaded functions according to 
    approach dictated by the command line argument 'overloading_approach'
    """
    if args.overloading_approach == 'similarity_map':
        entries = get_entries_via_similarity_map(commit, 
                                                 old_path,
                                                 filename,
                                                 overloaded_keys,
                                                 existing_methods,
                                                 current_methods)                        
    elif args.overloading_approach == 'sort_and_map':
        entries = get_entries_via_sort_and_map(commit, 
                                               old_path,
                                               filename, 
                                               overloaded_keys, 
                                               existing_methods, 
                                               current_methods) 
    return entries