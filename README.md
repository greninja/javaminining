# About

This repository contains code for analyzing a git repository and fetching commits from it wherein there was atleast one instance of adding a new argument to an existing method. The main script to run the code is `scripts/fetch_commits.py` and the output of the analysis is exported into a csv file (in `csv_reports/` directory). In order to carry out the mining and analysis, this repo makes use of [PyDriller](https://pydriller.readthedocs.io/en/latest/intro.html), which is a python framework designed to help developers mine software repositories.

## A note for overloaded methods

For a method that is not overloaded, it's name suffices to track it and map it across different commits in order to check if new arguments are added to it. Not so for the case of overloaded methods. Although each method in a set of overloaded methods is bound to have different set of parameters in any given commit, there does not seem to be a way to map any such method back to its previous state in past commits with 100% accuracy. I looked into PyDriller's code base and also explored `lizard` (which PyDriller is built on) API's functionalities but none of them, at the moment, consist of any tool that can be used to achieve this. Hence I came up with a couple of hacky and heuristic solutions, which I lay down below:

- *Similarity map*: Overloaded methods in previous commits are mapped to methods in current commit based on the similarities of their source code text. As of now, I have only considered cosine metric for computing the similarity.
- *Sort and Map*: Overloaded methods from current and previous commit are sorted and then mapped one-to-one. There can be unequal number of methods in two seperate commits. In such cases, the ones which do no get mapped will be considered as additions or deletions. 

I thought of another solution but concluded that it was not very useful: For a modified file in a particular commit, I could parse it's `diff_parsed` dictionary to go through the added and deleted lines and check if there is an addition of a new argument to any existing method. The idea is to first fetch a method's `starting_line` and then retrieve the new and old method signatures from `diff_parsed['added']` and `diff_parsed['delete']`respectively using that `starting_line` alone. Unfortunately, this comparison approach can only be useful in scenarios where a particular method's starting line was modified on the spot without changing the line number. If the method was moved and modified, it's previous signature stored in `diff_parsed['deleted']` won't be at the same `starting_line` number. And I couldn't find a deterministic approach to fetch the old line number.

To summarize, CSV entries for overloaded functions might not be 100% correct, since currently there's only an approximate solution.

## How to run the code?
	
Firstly, install the prereqs using 'requirements.txt':
```
pip3 -r install requirements.txt
```

Then to run the main script `scripts/fetch_commits.py`, it requires three command line arguments:

- `file_extension`: only files with this extension will be analyzed (for commits where a new argument was added to an existing method). Currently the code handles java files.  
- `repo_path`: absolute local path or remote github url of the git repository. Thanks to `PyDriller` both ways are supported.
- `overloading_approach`: either of `similarity_map` or `sort_and_map` used for dealing with overloaded functions.

Template of the command to run `fetch_commits.py` from the root directory of the repo:
```
python3 scripts/fetch_commits.py \
--repo_path /local path/OR/remote url/to/git/repo \
--file_extension <file_extension> \
--overloading_approach {similarity_map, sort_and_map}
```

Specific instance using absolute local path and `sort_and_map`:
```
python3 scripts/fetch_commits.py \
--repo_path /home/shadab/sample-code-java \
--file_extension .java \
--overloading_approach sort_and_map
```
Specific instance using remote url and `similarity_map`:
```
python3 scripts/fetch_commits.py \
--repo_path https://github.com/socketio/socket.io-client-java \
--file_extension .java \
--overloading_approach similarity_map
```

## Other scripts:

Rest of the scripts are in `scripts/` folder. Also, `automate.sh` is shell script to run `scripts/fetch_commits.py` on the 5 github repos listed below on this page for both approaches for handling overloaded methods. Needless to say if the repo does not have any function overloading the csv reports will be same.

## CSV report:

The generated CSV report will be stored in `csv_reports/` in either `csv_reports/similarity_map` or `csv_reports/sort_and_map` depending on the approach you choose for handling overloaded functions. The name of the csv file will be same as that of git repository or a substring of it. For eg: for repo `https://github.com/HouariZegai/Calculator.git` using `sort_and_map` approach, it will be in `csv_reports/sort_and_map/Calculator.csv`.

## Java repositories considered:

1. https://github.com/HouariZegai/Calculator.git (20 commits; csv file is empty because there is no such commit) 
2. https://github.com/AuthorizeNet/sample-code-java (318 commits)
3. https://github.com/square/retrofit (1782 commits) 
4. https://github.com/trojan-gfw/igniter (142 commits)
5. https://github.com/socketio/socket.io-client-java (268 commits)

And lastly, I made the `toy_commits` repo to test the code on typical commit scenarios for overloaded functions. There are 7 commits for a single file named 'test_file.java'. I considered the following possible scenarios whilst overloading a method named `getEntryForXValue`:

- Added a new method with an extra argument, 
- Added a new argument to an existing method, 
- Added a new method with same number but different set of arguments (wrt to any one existing method),
- Added a new argument to an existing method + added a new method with one of the previous signatures.
 
For the above scenarios, `similarity_map` approach correctly detects the second and fourth scenario as adding a new argument to an existing method (and also gets the pairs of function signatures for both the commits right). On the other hand `sort_and_map` approach, though detected both the commits correctly, got the pairing of function signatures wrong for fourth scenario. Their csv_reports are in `'csv_reports/similarity_map/toy_commits.csv'` and `'csv_reports/sort_and_map/toy_commits.csv'`.

## Note:

1. 6<sup>th</sup> commit in `toy_commits` repo (hash `ad7f7aa`) adds an exact duplicate of an existing (overloaded) method. Though this is not possible under overloading (since the parameters have to different in number or otherwise atleast) and certainly does not warrant a commit for the csv report, sometimes `sort_and_map` approach wrongly maps this new duplicate method to an existing method with less number of arguments and detects this as a commit that added an argument to an existing method. This will only happen in rare scenarios where the author mistakenly pushes a duplicate method to the repo.
2. The code takes care of scenarios in which a method was completely removed in a particular commit and then later on added again in a new commit with more number of arguments as before. This will not be considered as addition of arguments to an "existing method".
3. I have also added an extra column titled "Overloaded" in CSV file to tell whether the method in that row was overloaded or not at the time of processing it. 
4. The number of commits given in the above list are at the time of testing this code.

## Disclaimer about merge commits:

I am using a file's full path (within a git repo) as a key to store information about methods (in `existing_methods` dictionary) present in that file. For that, I use the paths available in `old_path` and `new_path` variables provided by Pydriller's `pydriller.domain.commit.Modification` class. This makes the code robust to file name changes. More precisly, if the name of a file changes in a particular commit, then the file's `old_path` variable can still be used to fetch information (argument list and signature) about the methods present in it in previous commits and detect if there was an addition of arguments.

But in the case of merge commits, there can be situations where addition of new arguments can go undetected. Let's consider the following scenario to illustrate more clearly. 


```
                               C5 (Another new arg added to one of 'B.java's methods)
                               |
                               |
                               C4 (New arg added to one of 'B.java's methods)
                               |
                               | 
                               C3    (merge commit wherein a new file 'B.java' was added and a new arg  
                               |  \   was added to method M of 'A.java')
                               |   \  
                               |    |
('A.java' has some method M)  C1    C2 
```


C1 (from branch 1) and C2 (from branch 2) are regular commits (not merge commits). C1 has a file called '`A.java`' with method M in it. When trying to merge branch 2 into branch 1, suppose there arise certain conflicts. After resolving these conflicts and before merging the commits, suppose a user does the following two things:

1. Adds a new argument to method M of '`A.java`'.
2. Adds a new file called '`B.java`' while in branch 1 

The user can, without any issues, commit the above changes to get the merge commit C3 since the conflicts that arose when trying to merge them are already resolved. But these changes are still considered as conflicts occured in a merge commit (since according to git, a conflict is a file that is different in one of the 2 or more branches that you are merging). And the problem with PyDriller is that for merge commits, it does not provide any information about any of the files involved in the conflict. As a result, `existing_methods` dictionary won't store information (argument list of methods against the file path) about the new file '`B.java`' or the new argument added to method M in '`A.java`' when analyzing C3. 

Subseqeuntly, C3 won't be reported as a commit in which a new argument was added to method M in '`A.java`'. However it can be detected in future commits. For eg, in commit C4 if '`A.java`' was modified but the new argument was not removed. For the file '`B.java`', the undetection can happen in commits following the merge commit C3. For eg suppose in commit C4, a new argument was added to one of '`B.java`'s methods. Now this won't be detected here since previous information about methods present in '`B.java`' (from merge commit C3) was not stored (since it was not available then). This is a scenario where a file's old path won't be useful to detect a new argument (whether or not there is a change in the file's name from previous commit). However if another new argument was added to one of '`B.java`'s methods in commit C5, it will be detected here since information about '`B.java`'s methods was stored during commit C4 as the file was modified there. 

As long as your repo does not have merge commits, this should not be an issue :) The reason PyDriller does not provide the information during merge conflicts and commits is because the author has not yet written a parser for combined diffs that `git` outputs in the case of a merge commit. So, for now, it will simply ignore the conflicts and the files within them. I have opened an issue in PyDriller's repo ([link](https://github.com/ishepard/pydriller/issues/89)) to have a discussion about this feature/bug (Do check Davide's response there).