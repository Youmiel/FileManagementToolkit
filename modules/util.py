from math import floor
from operator import truediv
import os
import re
import sys
from typing import Any, Callable, Union


def file_operation(path: str, mode: str, function: Callable) -> Any:
    flags = [False]
    try:
        with open(path, mode, encoding="utf-8") as f:
            ret_val = function(f, flags)
    except Exception as e:
        print(path, e, file=sys.stderr)

    if flags[0]:
        return ret_val
    else:
        try:
            with open(path, mode, encoding="gbk") as f:
                ret_val = function(f, flags)
        except Exception as e:
            print(path, e, file=sys.stderr)
    if flags[0]:
        return ret_val
    else:
        return None


def scan_folder(path: str, max_recursion: int = 15, file_ext='.*', file_regex: str = '.*', log: bool = True) -> list[str]:
    pattern_ext = re.compile(file_ext)
    pattern_file = re.compile(file_regex)
    result = []
    sub_path = os.listdir(path)
    if log:
        print('Scanning', path, '...', len(sub_path), 'files/directories')
    for sub in sub_path:
        full_path = os.path.join(path, sub)
        if os.path.isfile(full_path) and \
                re.match(pattern_ext, os.path.splitext(sub)[1]) is not None and \
                re.match(pattern_file, sub) is not None:
            result.append(full_path)
        elif max_recursion != 0 and os.path.isdir(full_path):
            result.extend(scan_folder(
                full_path, max_recursion-1, file_ext, file_regex, log))
    return result


def print_progress_bar(current_value, max_value, bar_length: int = 10, back_length: int = 0):
    print('\b' * back_length, end='', flush=True)
    bar_count = round(current_value / max_value * bar_length)
    print_string = "({} / {}) {} ({:.1f} % / 100 %)".format(
        current_value, max_value, '|' * bar_count + '-' * (bar_length - bar_count), current_value / max_value * 100)
    print(print_string, end='', flush=True)

    return len(print_string)


def check_and_write_file(path: str, content: Union[str, bytes], overwrite: bool = False):
    actual_path = path
    if os.path.exists(path):
        if overwrite and os.path.isfile(path):
            pass
        else:
            root, ext = os.path.splitext(path)
            rename = 1
            while(os.path.exists(actual_path)):
                actual_path = root + '_{}'.format(rename) + ext
                rename += 1
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    if type(content) is bytes:
        with open(actual_path, 'bw') as bin_file:
            bin_file.write(content)
    elif type(content) is str:
        with open(actual_path, 'w') as file:
            file.write(content)
    else:
        print('Unknown content.')
