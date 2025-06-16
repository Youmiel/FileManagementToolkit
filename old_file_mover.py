from argparse import ArgumentParser, Namespace
import os
import sys
import time
from distutils import file_util
from typing import List

from modules.util import scan_folder

A_YEAR_TIME = 365 * 24 * 60 * 60

# config
MAX_DURATION = A_YEAR_TIME * 2


def parse_args(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description='Moves old files to the target folder.', add_help=True)

    parser.add_argument('source_folder', action='store', type=str)
    parser.add_argument('target_folder', action='store', type=str)

    if len(args) == 0:
        parser.print_usage()
        sys.exit(0)
    return parser.parse_args(args)


if __name__ == '__main__':
    config = parse_args(sys.argv[1:])

    source_dir, target_dir = config.source_folder, config.target_folder
    
    for i in range(5):
        target_dir_backup = target_dir
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            break
        elif os.path.isfile(target_dir):
            target_dir = f'{target_dir_backup}_{i}'
    file_list = scan_folder(source_dir)
    # print(file_list)
    current_time = time.time()

    for path in file_list:
        if current_time - os.path.getmtime(path) > MAX_DURATION:
            folders = path.replace(source_dir, '').removeprefix('\\').removeprefix('/')
            dst = os.path.join(target_dir, folders)

            mkd = os.path.dirname(dst)
            if not os.path.exists(mkd):
                os.makedirs(mkd, exist_ok=True)
            # print(target_dir, folders, dst)
            file_util.move_file(path, dst)
        else:
            pass
