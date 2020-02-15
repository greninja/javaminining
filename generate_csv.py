import csv 

def csv_report(csv_file, csv_data):
    with open(csv_file, "w", newline="") as f:
        column_names = ["Commit SHA", "Java File", 
                        "Old function signature", "New function signature"]
        writer = csv.writer(f, delimiter=',')
        writer.writerow(column_names)
        writer.writerows(csv_data)