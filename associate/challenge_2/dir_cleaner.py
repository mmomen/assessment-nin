import os
import argparse
import time
import syslog
import sys


def find_files(dir_path, script_start, seconds_offset):
    # Files older than than time set are saved into an array and returned
    old_files = []
    for f in os.listdir(dir_path):
        file_path = os.path.join(dir_path, f)
        if os.stat(file_path).st_mtime < script_start - seconds_offset:
            old_files.append(file_path)
    return old_files


def delete_and_log(arr_old_files):
    # Take in a list of filenames to be deleted and logged
    for old_file in arr_old_files:
        syslog.syslog("Attempting to delete file: " + old_file)
        if os.path.isfile(old_file):
            # Catch if error in deleting file
            try:
                os.remove(old_file)
            except:
                syslog.syslog("Failed to delete file: " + old_file)
            else:
                syslog.syslog("Successfully deleted: " + old_file + " at " + str(time.time()))
        else:
            syslog.syslog(old_file + " is not a file.")


if __name__ == "__main__":
    script_start = time.time()
    parser = argparse.ArgumentParser(
        description="Delete files in specified directory older than desired amount of time.")
    parser.add_argument("dir_path",
                        help="The directory path to scan files to be processed.")
    parser.add_argument("seconds",
                        help="The amount of time, in seconds, files older than should be deleted. Default is 1800.",
                        default=1800)
    arguments = parser.parse_args()

    if os.path.isdir(arguments.dir_path):
        syslog.syslog("Script " + sys.argv[0] + " executing at " +
                      time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(script_start)) +
                      " on directory " + arguments.dir_path + " for files older than " +
                      arguments.seconds + " seconds.")
        # Main execution starts here
        files_to_delete = find_files(arguments.dir_path, script_start, int(arguments.seconds))
        delete_and_log(files_to_delete)
        syslog.syslog("Script complete.")
    else:
        print "ERROR: " + arguments.dir_path + " is not a directory."
