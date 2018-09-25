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
    else:
        sys.exit(arguments.log_path + " is not a directory.")
    return log_path


def log_parse(log_path):
    pattern = r'(\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b) - - \[(.*)\] "(\w{3,5}) (\/.*) HTTP\/1.1" (\d{3}) (\d*)'
    dict_request_ip = {}
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
            dict_request_ip[i] = match.group(1)
            dict_request_type[i] = match.group(3)
            dict_request_path[i] = match.group(4)
            dict_request_status_code[i] = match.group(5)
            # dict_datetime[i] = match.group(2)
            # dict_request_time[i] = match.group(6)
            i += 1

    return dict_request_ip, dict_request_type, dict_request_path, dict_request_status_code


def find_count_of_string_in_dict(search_string, dict_log):
    i = 0
    lines_found = []
    for line_num in dict_log:
        if search_string in dict_log[line_num]:
            lines_found.append(line_num)
            i += 1
    return i, lines_found

if __name__ == "__main__":
    args = arg_parse()
    outputs = log_parse(args)
    # 1 -How many times the URL "/production/file_metadata/modules/ssh/sshd_config" was fetched
    search_string = "/production/file_metadata/modules/ssh/sshd_config"
    first_case = find_count_of_string_in_dict(search_string, outputs[2])
    first_case_count = first_case[0]
    first_case_lines = first_case[1]
    print str(first_case_count) + " apperances of the string string: " + search_string
    # 2- Of those requests, how many times the return code from Apache was not 200
