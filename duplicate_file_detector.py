from argparse import ArgumentParser, Namespace
import json
from operator import truediv
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from hashlib import md5
import time
from typing import List

from modules.data_structure import MultiValueHashMap
from modules.util import check_and_write_file, print_progress_bar, scan_folder

# config
MAX_THREAD = 80
PRETTY = False
RECHECK_TIME = 0.05
TEMP_FILE = 'data\\temp'


def insert_md5(path: str, map: MultiValueHashMap) -> None:
    with open(path, 'br') as bin_file:
        m = md5(bin_file.read())
        md5_str = m.hexdigest()
        map.add(md5_str, path)


def parse_args(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description='Check duplicate files by comparing md5 and output reports.', add_help=True)

    parser.add_argument('source_folder', action='store', type=str)
    parser.add_argument('--restart', '-r', action='store_true', dest='restart')

    if len(args) == 0:
        parser.print_usage()
        sys.exit(0)
    return parser.parse_args(args)


if __name__ == '__main__':
    config = parse_args(sys.argv[1:])

    source_dir = config.source_folder
    restart = config.restart

    if not restart:

        path_list = scan_folder(source_dir, log=False)

        print('Directory scan finished.' + '({} files)'.format(len(path_list)))

        check_and_write_file(TEMP_FILE, json.dumps(path_list), overwrite=True)
    else:
        path_list = []
        if os.path.exists(TEMP_FILE):
            with open(TEMP_FILE, 'r') as f:
                path_list = json.load(f)
        else:
            print('Temp file not found')
            sys.exit(0)

    print('Processing for duplicate files...')
    back_length, start_time = 0, time.time()
    record = MultiValueHashMap()
    thread_queue = []
    with ThreadPoolExecutor(max_workers=MAX_THREAD) as pool:
        for index in range(len(path_list)):
            while(len(thread_queue) >= MAX_THREAD):
                for i in range(len(thread_queue) - 1, -1, -1):
                    if thread_queue[i].done():
                        thread_queue.pop(i)
                time.sleep(RECHECK_TIME)
            fu = pool.submit(insert_md5, path_list[index], record)
            thread_queue.append(fu)

            back_length = print_progress_bar(
                index, len(path_list), start_time, 20, back_length)

        while(len(thread_queue) > 0):
            for i in range(len(thread_queue) - 1, -1, -1):
                if thread_queue[i].done():
                    thread_queue.pop(i)
            time.sleep(RECHECK_TIME)

    key_set = {}
    for key in record.internal_map.keys():
        if len(record.internal_map[key]) <= 1:
            key_set[key] = True

    for k in key_set:
        record.internal_map.pop(k)

    print()
    print('Saving duplicate records...')

    check_and_write_file('data\\duplicate_index\\record.json',
                         record.to_json(pretty=PRETTY))
