# About

This repository contains code for analyzing and fetching commits from a git repository that modify atleast one file by adding a new argument to an existing method. The file extension/type that need to be analyzed can be passed as a command line argument, along with the absolute path of the git repository. The fetched commits are exported in a csv file.  

This repo chiefly makes use of [PyDriller](https://pydriller.readthedocs.io/en/latest/intro.html), which is a python framework that helps developers with mining software repositories. 

# Install prerequisites

Firstly, install the prereqs using 'requirements.txt':
```
pip3 -r install requirements.txt
```

# Run main script

The main script used to retrieve the commits is `fetch_commits.py`. It requires two command line arguments:

- `file_extension`: commits including instances of adding arguments to an existing method within files with  `file_extension` will be fetched 
- `repo_path`: absolute path of the git repository (fetching uses local git commit history)

Format of the command to run `fetch_commits.py`:
```
python3 fetch_commits.py --repo_path /path/to/git/repo --file_extension [.java, .py etc.]
```

For eg:
```
python3 fetch_commits.py --repo_path /home/shadab/sample-code-java --file_extension .java
```

Eventually, there'll be a CSV file with same filename as that of the git repo.

# Two Java repositories considered: 

1) "https://github.com/AuthorizeNet/sample-code-java" : It's CSV report is in 'sample-code-java.csv'
2) "https://github.com/socketio/socket.io-client-java" : It's CSV report is in 'socket.io-client-java.csv'

Note: Preferably use 'libreoffice calc' or any other spreadsheet software to view the csv better.