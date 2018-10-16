import argparse
import os
import sys
import re


'''Run script: `python parser.py <path-to-log-file>`'''


def arg_parse():
    parser = argparse.ArgumentParser(
        description="This file can be used to parse access logs.")
    parser.add_argument("log_path",
                        help="The directory path to scan files to be processed.")
    arguments = parser.parse_args()
    if os.path.isfile(arguments.log_path):
        log_path = arguments.log_path
    else:
        sys.exit(arguments.log_path + " is not a directory.")
    return log_path


def log_parse(log_path):
    ''' Use regex to parse log. Save data into relevant dictionaries.
        Key will be line number, value is the respective data type (IP, time, etc...) on that line.
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
    ''' Given a string and a dictionary (log of specific data type from log), find the string,
        and return the line numbers where string was found in log.
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
    ''' Given an array of line numbers from the log, and a dictionary of log values (of a
        different type from the log), return a dictionary of values of what appears the lines of the
        given dictionary. Example of obj returned: {"/dev/report/ec2-54-211-240-78.compute-1.amazonaws.com": [0]}
    '''

    results = {}
    for given_line_num in arr_lines_found:
        if dict_log[given_line_num] in results:
            results[str(dict_log[given_line_num])].append(given_line_num)
        else:
            results[str(dict_log[given_line_num])] = []
            results[str(dict_log[given_line_num])].append(given_line_num)
    return results


if __name__ == "__main__":
    args = arg_parse()
    outputs = log_parse(args)
    request_ips = outputs[0]
    request_types = outputs[1]
    request_paths = outputs[2]
    request_status_codes = outputs[3]

    print "1: How many times the URL '/production/file_metadata/modules/ssh/sshd_config' was fetched?"
    first_case_search_string = "/production/file_metadata/modules/ssh/sshd_config"
    first_case_lines = find_lines_of_string_in_dict_log(first_case_search_string, request_paths)
    first_case_count = len(first_case_lines)
    print str(first_case_count) + " appearances of the string: " + first_case_search_string

    print "---"

    print "2: Of those requests, how many times the return code from Apache was not 200?"
    second_case = find_lines_of_given_array_of_lines_in_dict(first_case_lines, request_status_codes)
    not_200 = 0
    for key in second_case:
        if key != "200":
            not_200 += len(second_case[key])

    print "%i instances of %s status codes returned from results of first case." % (not_200, "non-200")

    print "---"

    print "3: The total number of times Apache returned any code other than 200?"
    third_case_lines = find_lines_of_string_in_dict_log("200", request_status_codes, True)
    third_case_count = len(third_case_lines)
    print "%i appearances of non-200 HTTP status codes." % third_case_count

    print "---"

    print "4: The total number of times that any IP address sent a PUT request to a path under '/dev/report/'?"
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

    print "%i appearances of %s and %s" % (len(fourth_case_lines), fourth_search_request, fourth_search_path)

    print "---"

    print "5: A breakdown of how many times such requests (from 4th case) were made by IP address?"
    fifth_case = find_lines_of_given_array_of_lines_in_dict(fourth_case_lines, request_ips)
    print "Breakdown by IP address of %s requests to a path under %s:" % (fourth_search_request, fourth_search_path)
    for key in fifth_case:
        print "%s: %i" % (key, len(fifth_case[key]))
