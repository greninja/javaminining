import argparse

parser = argparse.ArgumentParser(description="Fetching commits in which new method arguments are introduced")

parser.add_argument('--url', type=str,
                    help='url of the github code repository')
parser.add_argument('--file_extension', type=str, default='.java',
                    help='extension of the files that you wish to fetch commits from')