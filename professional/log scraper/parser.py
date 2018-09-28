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
    ''' parse log to pull relevant data, will be saved in a dictionary
        key is line number, value is the desired value for that line
    '''

    pattern = r'(\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b) - - \[(.*)\] "(\w{3,5}) (\/.*) HTTP\/1.1" (\d{3}) (\d*)'
    log_requests_ip = {}
    # log_requests_datetime = {}
    log_requests_type = {}
    log_requests_path = {}
    log_requests_status_code = {}
    # log_requests_time = {}
    i = 0

    with open(log_path) as f:
        for line in f:
            match = re.search(pattern, line)
            log_requests_ip[i] = match.group(1)
            # log_requests_datetime[i] = match.group(2)
            log_requests_type[i] = match.group(3)
            log_requests_path[i] = match.group(4)
            log_requests_status_code[i] = match.group(5)
            # log_requests_time[i] = match.group(6)
            i += 1

    return log_requests_ip, log_requests_type, log_requests_path, log_requests_status_code


def find_lines_of_string_in_dict_log(search_string, dict_log, search_string_unary=False):
    ''' provided a string and a dictionary of values from the log, find string,
        return the line numbers where string was found in log
    '''

    lines_found = []
    if search_string_unary:
        for line_num in dict_log:
            if search_string not in dict_log[line_num]:
                lines_found.append(line_num)
    else:
        for line_num in dict_log:
            if search_string in dict_log[line_num]:
                lines_found.append(line_num)
    return lines_found


def find_lines_of_given_array_of_lines_in_dict(arr_lines_found, dict_log):
    ''' provided an array of line numbers and a dictionary of log values (ideally of a
        different log type), return a dictionary of values of what appears on those lines
        {"found_value": [1, 5, 95]}
    '''

    results = {}
    for line_num in dict_log:
        if dict_log[line_num] in results:
            results[str(dict_log[line_num])].append(line_num)
        else:
            results[str(dict_log[line_num])] = []
            results[str(dict_log[line_num])].append(line_num)
    return results


if __name__ == "__main__":
    args = arg_parse()
    outputs = log_parse(args)
    request_ips = outputs[0]
    request_types = outputs[1]
    request_paths = outputs[2]
    request_status_codes = outputs[3]

    # 1: How many times the URL "/production/file_metadata/modules/ssh/sshd_config" was fetched
    search_string = "/production/file_metadata/modules/ssh/sshd_config"
    first_case_lines = find_lines_of_string_in_dict_log(search_string, request_paths)
    first_case_count = len(first_case_lines)
    print str(first_case_count) + " appearances of the string string: " + search_string

    # 2: Of those requests, how many times the return code from Apache was not 200
    second_case = find_lines_of_given_array_of_lines_in_dict(first_case_lines, request_status_codes)
    for key in second_case:
        if key != "200":
            print key + " status code appeared " + str(len(second_case[key])) + " time(s)."

    # 3: The total number of times Apache returned any code other than 200
    third_case_lines = find_lines_of_string_in_dict_log("200", request_status_codes, True)
    third_case_count = len(third_case_lines)
    print str(third_case_count) + " appearances of non-200 HTTP status codes."

    # 4: The total number of times that any IP address sent a PUT request to a path under "/dev/report/"
    fourth_search_request = "PUT"
    fourth_search_path = "/dev/report/"

    find_puts_lines = find_lines_of_string_in_dict_log(fourth_search_request, request_types)
    find_puts_count = len(find_puts_lines)

    find_puts_by_path = find_lines_of_given_array_of_lines_in_dict(find_puts_lines, request_paths)
    fourth_case_lines = []
    for key in find_puts_by_path:
        if fourth_search_path in key:
            # for loop here handles case of multiple line number results
            for line_num in find_puts_by_path[key]:
                fourth_case_lines.append(line_num)

    print str(len(fourth_case_lines)) + " appearances of " + fourth_search_request + " and " + fourth_search_path

    # 5: A breakdown of how many times such requests (from 4th case) were made by IP address
    fifth_case = find_lines_of_given_array_of_lines_in_dict(fourth_case_lines, request_ips)
    print "Breakdown by IP address of %s requests to a path under %s:" % (fourth_search_request, fourth_search_path)
    for key in fifth_case:
        print str(key) + ": " + str(len(fifth_case[key]))
