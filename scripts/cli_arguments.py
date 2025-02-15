import argparse

parser = argparse.ArgumentParser(description="Fetching commits in which new method arguments are introduced")

parser.add_argument('--repo_path', type=str,
                    help='absolute path of the git repository')
parser.add_argument('--file_extension', type=str, default='.java',
                    help='type (extension) of files to fetch commits from')
parser.add_argument('--overloading_approach', type=str, default='similarity_map',
                    help='how to compare overloaded functions between commits')