import os
import csv 

def csv_report(repo_path, csv_data):
    csv_file = repo_path.split("/")[-1].split(".")[0]+'.csv'
    csv_file = os.path.join(os.getcwd(), 'csv_reports', csv_file)

    with open(csv_file, "w", newline="") as f:
        column_names = ["Commit SHA", "Filename", 
                        "Old function signature", "New function signature"]
        writer = csv.writer(f, delimiter=',')
        writer.writerow(column_names)
        writer.writerows(csv_data)