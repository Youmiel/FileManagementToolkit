import json
import os
import re
import sys
import time
from argparse import ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from modules.thread_util import wait_and_check_queue
from modules.util import check_and_write_file, print_progress_bar

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB']
DELETE_FORMAT = ['', '.null', '.jpg', '.bmp']

# Config
MAX_THREAD = 80
PRETTY = False
RECHECK_TIME = 0.05
REPORT_FILE = 'data/size_index.json'


def get_file_size(path: str, size_map: Dict[str, int]) -> None:
    size_map[path] = os.path.getsize(path)


def delete_dup(path_list: List[str]):
    if isinstance(path_list, List):
        file_count = len(path_list)
        ext_list = list(os.path.splitext(
            path)[1].lower() for path in path_list)
        delete_count = 0
        for format in DELETE_FORMAT:
            if delete_count >= file_count - 1:
                break

            if format in ext_list:
                os.remove(path_list[ext_list.index(format)])
                delete_count += 1
    else:
        print('path list is not a list of string.')


def parse_args(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description='Calculate duplicate file size.', add_help=True)

    parser.add_argument('index_file', action='store', type=str)
    parser.add_argument('--report', '-r', action='store_true', dest='report')
    parser.add_argument('--delete', '-d', action='store_true', dest='delete')

    if len(args) == 0:
        parser.print_usage()
        sys.exit(0)
    return parser.parse_args(args)


if __name__ == '__main__':
    config = parse_args(sys.argv[1:])

    index_file = config.index_file
    report = config.report
    delete = config.delete

    with open(index_file, 'r') as f:
        index_map = json.load(f)

    print('File index loaded')

    size_map = {}
    thread_queue = []
    back_length, start_time = 0, time.time()
    with ThreadPoolExecutor(max_workers=MAX_THREAD) as pool:
        count = 0
        for key in index_map:
            path_list = index_map[key]

            for index in range(1, len(path_list)):

                wait_and_check_queue(thread_queue, MAX_THREAD, RECHECK_TIME)

                fu = pool.submit(get_file_size, path_list[index], size_map)
                thread_queue.append(fu)

            count += 1
            back_length = print_progress_bar(count, len(
                index_map), start_time, 20, back_length)

        wait_and_check_queue(thread_queue, 1, RECHECK_TIME)

    if report:
        indent = 4 if PRETTY else None
        check_and_write_file(REPORT_FILE, json.dumps(
            size_map, indent=indent, default=lambda x: x.__dict__), False)

    total_size = 0
    for key in size_map:
        total_size += size_map[key]

    output_size = total_size
    output_unit = SIZE_UNITS[0]
    for unit in SIZE_UNITS:
        if output_size < 1024:
            output_unit = unit
            break
        else:
            output_size /= 1024

    print()
    print('Total file size: {:.2f} {}'.format(output_size, output_unit))

    if delete:
        confirm_str = input("Input anything to confirm (n to reject):\n")
        if confirm_str.lower() != 'n':
            count, back_length, start_time, total_length = 0, 0, time.time(), len(index_map)
            for key in index_map:
                path_list = index_map[key]
                delete_dup(path_list)

                count += 1
                back_length = print_progress_bar(
                    count, total_length, start_time, 20, back_length)
