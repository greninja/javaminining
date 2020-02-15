# About

This repository contains code for analyzing and fetching commits from a git repository that modify atleast one file by adding a new argument to an existing method. The file extension/type that needs to be analyzed can be passed as a command line argument, along with the local absolute path or remote github url of the git repository. The fetched commits are exported in a csv file. This repo chiefly makes use of [PyDriller](https://pydriller.readthedocs.io/en/latest/intro.html), which is a python framework that helps developers with mining software repositories.

# Install prerequisites

Firstly, install the prereqs using 'requirements.txt':
```
pip3 -r install requirements.txt
```

# Run main script
	
The main script used to retrieve the commits is `src/fetch_commits.py`. It requires two command line arguments:

- `file_extension`: commits including instances of adding arguments to an existing method within files with  `file_extension` will be fetched 
- `repo_path`: local absolute path or remote github url of the git repository. This is because `PyDriller` supports both.

Format of the command to run `fetch_commits.py`:
```
python3 src/fetch_commits.py --repo_path /local path or remote url/to/git/repo --file_extension [.java, .py etc.]
```

For eg using absolute local path:
```
python3 src/fetch_commits.py --repo_path /home/shadab/sample-code-java --file_extension .java
```
or using remote url:
```
python3 src/fetch_commits.py --repo_path https://github.com/socketio/socket.io-client-java --file_extension .java
```

# Two Java repositories considered: 

1) https://github.com/AuthorizeNet/sample-code-java : CSV report is in 'csv_reports/sample-code-java.csv'
2) https://github.com/socketio/socket.io-client-java : CSV report is in 'csv_reports/socket.csv'

Note: Preferably use Libreoffice Calc or any other spreadsheet software to view the csv better.