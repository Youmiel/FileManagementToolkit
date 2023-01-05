import sys
from typing import Dict, List

sys.path.insert(1, 'modules')
# from code.class_scanner import run as _scan_classes_run
# from code.line_counter import run as _line_counter_run
from util import scan_folder
import code.class_scanner as class_scanner
import code.line_counter as line_counter
from code.supported_language import LangRegistry, LangType


def count_line_by_ext(path: str, file_ext: str):
    # print('count_line_by_ext', path, file_ext)
    _line_counter_run(path, file_ext)


def count_line_by_lang(path: str, lang: LangType):
    # print('count_line_by_lang', path, lang)
    _line_counter_run(path, LangRegistry.get(lang)['file_ext'])


def count_class(path: str, lang: LangType):
    # print('count_class', path, lang)
    _scan_classes_run(path, lang)


def _scan_classes_run(path: str, lang: LangType) -> None:
    lang_config = LangRegistry.get(lang)
    path_list = scan_folder(path, file_ext=lang_config['file_ext'])
    class_dict: Dict[str, List[str]] = {}
    for p in path_list:
        namespace, class_list = class_scanner.count_classes(p, lang_config['parser'])
        if namespace in class_dict.keys():
            for c in class_list:
                class_dict[namespace].append(c)
        else:
            class_dict[namespace] = class_list
    keys = list(class_dict.keys())
    keys.sort()
    print(keys)
    class_scanner.write_json('./class_scan_result.json', class_dict)


def _line_counter_run(path: str, file_ext: str):
    if file_ext.find('\\.') >= 0:
        ext = file_ext
    elif file_ext.find('.') >= 0:
        ext = file_ext.replace('.', '\\.')
    else:
        ext = '\\.' + file_ext

    path_list = scan_folder(path, file_ext=file_ext)
    count = 0
    for p in path_list:
        count += line_counter.count_line(p)
    print('Totally', len(path_list), ext.replace('\\', '*'), 'files.')
    print('Totally', count, 'lines of code.')


# if __name__ == '__main__':
#     _line_counter_run('./', '\\.cs')
#     _scan_classes_run('./', LangType.C_SHARP)
