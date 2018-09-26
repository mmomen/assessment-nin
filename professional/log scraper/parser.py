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
    # dict_request_datetime = {}
    # dict_request_time = {}
    i = 0

    # go through each line in log and parse out capture groups
    with open(log_path) as f:
        for line in f:
            match = re.search(pattern, line)
            dict_request_ip[i] = match.group(1)
            dict_request_type[i] = match.group(3)
            dict_request_path[i] = match.group(4)
            dict_request_status_code[i] = match.group(5)
            # dict_request_datetime[i] = match.group(2)
            # dict_request_time[i] = match.group(6)
            i += 1

    return dict_request_ip, dict_request_type, dict_request_path, dict_request_status_code


def find_count_of_string_in_dict(search_string, dict_log, search_string_unary=False):
    # provided a string and a dictionary of values from the log, find string,
    # return number of appearances and an array of the line numbers where it was found
    lines_found = []
    if search_string_unary:
        for line_num in dict_log:
            if search_string not in dict_log[line_num]:
                lines_found.append(line_num)
    else:
        for line_num in dict_log:
            if search_string in dict_log[line_num]:
                lines_found.append(line_num)
    return len(lines_found), lines_found


def find_count_of_values_of_lines_in_dict(arr_lines_found, dict_log):
    # provided an array of line numbers and a dictionary of log values
    # return a dictionary of values of what appears on those lines
    dict_results = {}
    for line_num in dict_log:
        if dict_log[line_num] in dict_results:
            dict_results[str(dict_log[line_num])].append(line_num)
        else:
            dict_results[str(dict_log[line_num])] = []
            dict_results[str(dict_log[line_num])].append(line_num)
    return dict_results


if __name__ == "__main__":
    args = arg_parse()
    outputs = log_parse(args)
    request_ips = outputs[0]
    request_types = outputs[1]
    request_paths = outputs[2]
    request_status_codes = outputs[3]

    # 1: How many times the URL "/production/file_metadata/modules/ssh/sshd_config" was fetched
    search_string = "/production/file_metadata/modules/ssh/sshd_config"
    first_case = find_count_of_string_in_dict(search_string, request_paths)
    first_case_count = first_case[0]
    first_case_lines = first_case[1]
    print str(first_case_count) + " appearances of the string string: " + search_string

    # 2: Of those requests, how many times the return code from Apache was not 200
    second_case = find_count_of_values_of_lines_in_dict(first_case_lines, request_status_codes)
    for key in second_case:
        if key != "200":
            print key + " status code appeared " + str(len(second_case[key])) + " time(s)."

    # 3: The total number of times Apache returned any code other than 200
    third_case = find_count_of_string_in_dict("200", request_status_codes, True)
    third_case_count = third_case[0]
    third_case_lines = third_case[1]
    print str(third_case_count) + " appearances of non-200 HTTP status codes."

    # 4: The total number of times that any IP address sent a PUT request to a path under "/dev/report/"
    fourth_search_request = "PUT"
    fourth_search_path = "/dev/report/"

    find_puts = find_count_of_string_in_dict(fourth_search_request, request_types)
    find_puts_count = find_puts[0]  # Count of all PUTs
    find_puts_lines = find_puts[1]  # Lines of all PUTs

    find_puts_by_path = find_count_of_values_of_lines_in_dict(find_puts_lines, request_paths)
    fourth_case_lines = []
    for key in find_puts_by_path:
        if fourth_search_path in key:
            fourth_case_lines.append(find_puts_by_path[key])
    print str(len(fourth_case_lines)) + " appearances of " + fourth_search_request + " and " + fourth_search_path
