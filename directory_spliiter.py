#!/bin/env python
"""
Directory splitter.

Group files from given directory into smaller directories, by month of modification.

Each directory is named as YYYY-MM, so it can be sorted alphabetically.
"""

import os
import shutil
import subprocess

directory_to_split_absolute_path: str = ""


FULL_TIMESTAMP_SIZE    = 31
DESIRED_TIMESTAMP_SIZE = 7


def get_files_last_modification_time(directory_to_split: str) -> list[tuple]:
    """Fetches all files (with one depth level, i.e. flat) and checks its timestamps.

    Args:
        directory_to_split (str): absolute path for given directory

    Returns:
        list[tuple]: each tuple contains (timestamp, filename)
    """
    command = f"find {directory_to_split} -maxdepth 1 -type f -printf '%T+ %p\n' | sort"
    raw_output = subprocess.run(command, capture_output=True, shell=True, text=True)
    files_timestamps = raw_output.stdout.strip().split("\n")
    output = []
    for raw_line in files_timestamps:
        timestamp = raw_line[:DESIRED_TIMESTAMP_SIZE]
        filename  = raw_line[FULL_TIMESTAMP_SIZE:]
        output.append((timestamp, filename))
    return output


def make_directories_for_each_month(files_timestamps: list[tuple]):
    timestamps = [timestamp[0] for timestamp in files_timestamps]
    timestamps = list(set(timestamps))
    for timestamp in timestamps:
        year_month = timestamp
        if not os.path.isdir(year_month):
            os.makedirs(year_month)


def move_files_for_desired_directory(directory_to_split: str, files_timestamps: list[tuple]):
    for timestamp_file in files_timestamps:
        file_path = timestamp_file[1]
        file = file_path.split("/")[-1]
        timestamp = timestamp_file[0]
        destination = f"{directory_to_split}/{timestamp}/{file}"
        shutil.move(file_path, destination)


if __name__ == "__main__":
    os.chdir(directory_to_split_absolute_path)
    files_timestamps = get_files_last_modification_time(directory_to_split_absolute_path)
    make_directories_for_each_month(files_timestamps)
    move_files_for_desired_directory(directory_to_split_absolute_path, files_timestamps)
