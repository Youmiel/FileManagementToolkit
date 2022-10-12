import sys
from io import TextIOWrapper
from typing import List

sys.path.insert(1, 'modules')
from util import file_operation, scan_folder


def count_line(path: str) -> int:

    def count(f: TextIOWrapper, flag_list: List[bool]) -> int:
        lines = 0
        for line in f:
            if line != '\n':
                lines += 1
        flag_list[0] = True
        return lines

    ret_val = file_operation(path, 'r', count)
    if ret_val is not None:
        return ret_val
    else:
        return 0


def run(path: str, file_ext: str):
    if file_ext.find('\\.') >= 0:
        ext = file_ext
    elif file_ext.find('.') >= 0:
        ext = file_ext.replace('.', '\\.')
    else:
        ext = '\\.' + file_ext

    path_list = scan_folder(path, file_ext)
    count = 0
    for p in path_list:
        count += count_line(p)
    print('Totally', len(path_list), ext.replace('\\','*'), 'files.')
    print('Totally', count, 'lines of code.')

if __name__ == '__main__':
    run('./', '\\.cs')
