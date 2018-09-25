import argparse
import os
import sys


def arg_parse():
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument("log_path",
                        help="The directory path to scan files to be processed.")
    arguments = parser.parse_args()
    if os.path.isdir(arguments.log_path):
        log_path = arguments.log_path
        return log_path
    else:
        sys.exit(arguments.log_path + " is not a directory.")


def log_parse(log_path):
    print log_path


if __name__ == "__main__":
    log_parse(arg_parse())
