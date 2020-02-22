import os
import csv 

def get_parameters(string):
    return string[string.find("(")+1:string.find(")")].split(",")

def csv_report(args, repo_path, csv_data):
    csv_file = repo_path.rstrip("/").split("/")[-1].split(".")[0]+'.csv'
    csv_file = os.path.join(os.getcwd(), 
                            'csv_reports', 
                            args.overloading_approach, 
                            csv_file)

    with open(csv_file, "w", newline="") as f:
        column_names = ["Commit SHA",
                        "Filename",
                        "Old function signature", 
                        "New function signature",
                        "Overloaded"]
        writer = csv.writer(f, delimiter=',')
        writer.writerow(column_names)
        writer.writerows(csv_data)

def get_modified_files(commit, file_extension):
    """
    Only consider modified files with extension 'file_extension'
    in a particular commit
    """
    current_modified_files = [mod_file for mod_file in commit.modifications
                              if mod_file.filename.endswith(file_extension)]
    return current_modified_files

def get_frequency(modified_file):
    """
    Returns frequency table of methods present in a modified file
    """
    method_frequencies = {}
    for method in modified_file.methods:
        key = method.name
        if key not in method_frequencies:
            method_frequencies[key] = 0
        method_frequencies[key] += 1
    return method_frequencies