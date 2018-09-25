import argparse
import os
import sys
import re


def arg_parse():
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument("log_path",
                        help="The directory path to scan files to be processed.")
    arguments = parser.parse_args()
    if os.path.isfile(arguments.log_path):
        log_path = arguments.log_path
        return log_path
    else:
        sys.exit(arguments.log_path + " is not a directory.")


def log_parse(log_path):
    pattern = r'(\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b) - - \[(.*)\] "(\w{3,5}) (\/.*) HTTP\/1.1" (\d{3}) (\d*)'
    dict_ip = {}
    dict_request_type = {}
    dict_request_path = {}
    dict_request_status_code = {}
    # dict_datetime = {}
    # dict_request_time = {}
    i = 0

    # loop over each line in log
    with open(log_path) as f:
        for line in f:
            match = re.search(pattern, line)
            dict_ip[i] = match.group(1)
            dict_request_type[i] = match.group(3)
            dict_request_path[i] = match.group(4)
            dict_request_status_code[i] = match.group(5)
            # dict_datetime[i] = match.group(2)
            # dict_request_time[i] = match.group(6)
            i += 1

    return dict_ip, dict_request_type, dict_request_path, dict_request_status_code


if __name__ == "__main__":
    outputs = log_parse(arg_parse())
