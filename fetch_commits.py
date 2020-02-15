# TODO List:
# (6) function signature Available: {commit hash, filename, (name+parameters, public/private, return_type) }
# (7) write README.md
# (2) Check all corner cases; if any     NOT DONE

# (6) create a requirements.txt file for installation - NOT DONE
# (4) scrap online github commit or from local git repo? NOT DONE

import csv
from pydriller import RepositoryMining

from arguments import parser

# def get_repo_path(url):
#     repodir = url.split("/")[-1].split(".")[0]
#     if not os.path.exists(repodir):
#         os.system("git clone "+url)
#     pwd = os.getcwd()
#     repo_path = os.path.join(pwd, repodir)
#     return repo_path

def get_modified_files(commit, file_type):
    """
    Only consider modified files with extension 'file_type'
    """
    modified_files = [f for f in commit.modifications if file_type in f.filename]
    return modified_files

def get_signature_tokens(method, modified_file, mode):
    """
    """
    start_line = method.start_line
    added_diff = modified_file.diff_parsed[mode]
    for ad in added_diff:
        if ad[0] == start_line:
            tokens = ad[1].split()
            access_mod = tokens[0]
            return_type = tokens[1]    
    return access_mod, return_type          

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
            # by comparing the number of parameters for each method
            # with previous commit 
            if method.name in existing_methods.keys():
                
                num_of_params_prev = len(existing_methods[method.name][0])
                num_of_params_curr = len(current_methods[method.name][0])
                if num_of_params_curr > num_of_params_prev:
                    
                    # get return type and access modified of updated method
                    old_access_mod, old_return_type = get_signature_tokens(method, modified_file, 'deleted')
                    new_access_mod, new_return_type = get_signature_tokens(method, modified_file, 'added')

                    old_function_signature = old_access_mod+' '+old_return_type+' '+existing_methods[method.name][1]
                    new_function_signature = new_access_mod+' '+new_return_type+' '+current_methods[method.name][1]
                    t = [commit.hash[:7], modified_file.filename, \
                                old_function_signature, new_function_signature]
                    data_to_add.append(t)

    return current_methods, data_to_add

def csv_report(csv_file, csv_data):
    """
    """
    with open(csv_file, "w", newline="") as f:
        column_names = ["Commit SHA", "Java File", 
                        "Old function signature", "New function signature"]
        writer = csv.writer(f, delimiter=',')
        writer.writerow(column_names)
        writer.writerows(csv_data)

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

        # accumulating data to be added to csv report
        for d in data_to_add:
            csv_data.append(d)
    
    # generate csv report
    csv_file = repo_path.split("/")[-1]+'.csv'
    csv_report(csv_file, csv_data)

if __name__=="__main__":
    args = parser.parse_args()      
    get_commits_in_CSV(args)