import sys

sys.path.insert(1, 'modules')
from code.class_scanner import run as _scan_classes_run
from code.line_counter import run as _line_counter_run
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
