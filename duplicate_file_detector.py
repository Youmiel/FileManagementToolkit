

from concurrent.futures import ThreadPoolExecutor, thread
from encodings import utf_8
from hashlib import md5
from numbers import Integral
from operator import truediv
import sys
from time import sleep
from traceback import print_exception
from modules.data_structure import MultiValueHashMap

from modules.util import check_and_write_file, print_progress_bar, scan_folder


def insert_md5(path: str, map: MultiValueHashMap) -> None:
    with open(path, 'br') as bin_file:
        m = md5(bin_file.read())
        md5_str = m.hexdigest()
        map.add(md5_str, path)

if __name__ == '__main__':
    MAX_THREAD = 80

    print(sys.argv)
    if len(sys.argv) < 2 or sys.argv[1] == '-h':
        print('usage: [program.py] <source_folder>')
        sys.exit(0)

    source_dir = sys.argv[1]

    path_list = scan_folder(source_dir, log=False)
    
    print('Directory scan finished.' + '({} files)'.format(len(path_list)))

    print('processing for duplicate...', end='', flush=True)
    back_length = 0
    record = MultiValueHashMap()
    thread_queue = []
    with ThreadPoolExecutor(max_workers=MAX_THREAD) as pool:
        for index in range(len(path_list)):
            while(len(thread_queue) >= MAX_THREAD):
                for i in range(len(thread_queue) - 1, -1, -1):
                    if not thread_queue[i].running():
                        thread_queue.pop(i)
                sleep(0.05)
            fu = pool.submit(insert_md5, path_list[index], record)
            thread_queue.append(fu)

            back_length = print_progress_bar(index, len(path_list), 10, back_length)

        while(len(thread_queue) > 0):
            for i in range(len(thread_queue) - 1, -1, -1):
                if not thread_queue[i].running():
                    thread_queue.pop(i)
            sleep(0.05)
    
    key_set = {}
    for key in record.internal_map.keys():
        if len(record.internal_map[key]) <= 1:
            key_set[key] = True
    
    for k in key_set:
        record.internal_map.pop(k)

    # print()
    check_and_write_file('data\\record.json', record.to_json())