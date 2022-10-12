import json
import re
import sys
from io import TextIOWrapper
from typing import Dict, List, Tuple

sys.path.insert(1, 'modules')
from util import file_operation, scan_folder


class LanguageParser():
    def __init__(self, namespace_pattern: Tuple[str, int], class_patterns: List[Tuple[str, int]]) -> None:
        self.namespace_pattern = (re.compile(namespace_pattern[0]), namespace_pattern[1])
        
        self.class_patterns = []
        for class_def in class_patterns:
            self.class_patterns.append((re.compile(class_def[0]), class_def[1]))

    def parse(self, f: TextIOWrapper, flag_list: List[bool]) \
        -> Tuple[List[str], List[str]]: # [namespaces, [classes]]
        namespace, class_list = 'none', []
        for line in f:
            if namespace == 'none':
                namespace_pattern, group_index = self.namespace_pattern
                result = re.search(namespace_pattern, line)
                if result is not None:
                    namespace = result.group(group_index)

            for class_pattern, group_index in self.class_patterns:
                result = re.search(class_pattern, line)
                if result is not None:
                    class_list.append(result.group(group_index))
                
        flag_list[0] = True
        return (namespace, class_list)


def count_classes(path: str, parser: LanguageParser) -> Tuple[List[str], List[str]]:
    ret_val = file_operation(path, 'r', parser.parse)
    return ret_val


def write_json(path: str, val: Dict) -> None:
    with open(path, 'w', encoding='UTF-8') as f:
        json.dump(val, f, sort_keys=True, indent=4)

from supported_language import LangRegistry, LangType

def run(path: str, lang: LangType) -> None:
    lang_config = LangRegistry.get(lang)
    path_list = scan_folder(path, file_ext=lang_config['file_ext'])
    class_dict: Dict[str, List[str]] = {}
    for p in path_list:
        namespace, class_list = count_classes(p, lang_config['parser'])
        if namespace in class_dict.keys():
            for c in class_list:
                class_dict[namespace].append(c)
        else:
            class_dict[namespace] = class_list
    keys = list(class_dict.keys())
    keys.sort()
    print(keys)
    write_json('./class_scan_result.json', class_dict)


if __name__ == '__main__':
    run('./', LangType.C_SHARP)
