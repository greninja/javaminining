# About

This repository contains code for analyzing and fetching commits from a git repository that modify atleast one file by adding a new argument to an existing method. The file extension/type that need to be analyzed can be passed as a command line argument, along with the absolute path of the git repository. The fetched commits are exported in a csv file.  

This repo chiefly makes use of [PyDriller](https://pydriller.readthedocs.io/en/latest/intro.html), which is a python framework that helps developers with mining software repositories. 

## How to run?
Firstly, install the prereqs using 'requirements.txt':
```
pip3 -r install requirements.txt
```

The main file to retrieve the commits is `fetch_commits.py`. It needs two command line arguments:

- `file_type`: all commits which include an instance of adding an argument to an existing method within files with  `file_extension` will be fetched 
- `repo_path`: absolute path of the git repository

The code was tested on 2 Java repositories. Their Github urls are: 

1) https://github.com/HouariZegai/Calculator.git
2) https://github.com/AmbalviUsman/Billing-System.git

Sample script to run `fetch_commits.py` on 1:
```
python3 fetch_commits.py --repo_path /home/shadab/javaminining/Calculator --file_extension .java
```
Eventually, there'll be a CSV file with same filename as that of the git repo.