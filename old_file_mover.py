import os
import sys
import time
from distutils import file_util
from typing import List

from modules.util import scan_folder

A_YEAR_TIME = 365 * 24 * 60 * 60

MAX_DURATION = A_YEAR_TIME * 1

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 3 or sys.argv[1] == '-h':
        print('usage: [program.py] <source_folder> <target_folder>')

    source_dir, target_dir = sys.argv[1], sys.argv[2]
    for i in range(5):
        if not os.path.exists(target_dir):
            os.makedirs(source_dir,exist_ok=True)
            break
        elif os.path.isfile(target_dir):
            source_dir = source_dir + '_copy'
    file_list = scan_folder(source_dir)
    # print(file_list)
    current_time = time.time()

    for path in file_list:
        if current_time - os.path.getmtime(path) > MAX_DURATION:
            folders = path.replace(source_dir, '').removeprefix('\\')
            dst = os.path.join(target_dir, folders)

            mkd = os.path.dirname(dst)
            if not os.path.exists(mkd):
                os.makedirs(mkd, exist_ok=True)
            # print(target_dir, folders, dst)
            file_util.move_file(path, dst)
        else:
            pass
