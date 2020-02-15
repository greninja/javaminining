# About

This repository contains code for analyzing a git repository and fetching commits within it that consist of atleast one file wherein a new argument was added to an existing method. The file extension/type that needs to be analyzed can be passed as a command line argument, along with the local absolute path or remote github url of the git repository. The fetched commits are exported to a csv file. This repo chiefly makes use of [PyDriller](https://pydriller.readthedocs.io/en/latest/intro.html), which is a python framework that helps developers with mining software repositories.

# Install prerequisites

Firstly, install the prereqs using 'requirements.txt':
```
pip3 -r install requirements.txt
```

# How to run the code?
	
The main script used to retrieve the commits is `scripts/fetch_commits.py`. It requires two command line arguments:

- `file_extension`: commits including instances of adding arguments to an existing method within files with  `file_extension` will be fetched 
- `repo_path`: local absolute path or remote github url of the git repository. This is because `PyDriller` supports both.


Template of the command to run `fetch_commits.py`:
```
python3 scripts/fetch_commits.py --repo_path /local path or remote url/to/git/repo --file_extension .java/.py
```

Specific instance using absolute local path:
```
python3 scripts/fetch_commits.py --repo_path /home/shadab/sample-code-java --file_extension .java
```
Specific instance using remote url:
```
python3 scripts/fetch_commits.py --repo_path https://github.com/socketio/socket.io-client-java --file_extension .java
```

Please note you can also pass multiple file extensions at the same time with a comma seperated list. The script will fetch commits for all those file types. Eg:
Specific instance using remote url:
```
python3 scripts/fetch_commits.py --repo_path https://github.com/socketio/socket.io-client-java --file_extension .java,.py
```

The generated CSV file will be stored in `csv_reports/` and it's name will be the name of the git repository itself or a substring of it.

# Two Java repositories considered:

1) https://github.com/AuthorizeNet/sample-code-java : CSV report is in 'csv_reports/sample-code-java.csv'
2) https://github.com/socketio/socket.io-client-java : CSV report is in 'csv_reports/socket.csv'

Note: Preferably use Libreoffice Calc or any other spreadsheet software to view the csv better.