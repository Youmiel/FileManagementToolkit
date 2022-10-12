import sys
from enum import Enum
from typing import Dict

sys.path.insert(1, 'modules')
from class_scanner import LanguageParser


class LangType(Enum):
    JAVA = 'JAVA'
    C_SHARP = 'C_SHARP'

    def __str__(self) -> str:
        return self.value


class LangRegistry():
    REG = {}

    def _config(file_ext: str, parser: LanguageParser) -> Dict:
        return {
            'file_ext': '\.' + file_ext,
            'parser': parser
        }
    
    REG[LangType.JAVA] = _config('java', LanguageParser(('package (.*);', 1),
                                            [('class ([A-Z]\w+)', 1), ('enum ([A-Z]\w+)', 1)]))
    REG[LangType.C_SHARP] = _config('cs', LanguageParser(('namespace (.*)', 1),
                                            [('class ([A-Z]\w+)', 1), ('enum ([A-Z]\w+)', 1), ('struct ([A-Z]\w+)', 1)]))

    def get(lang: LangType) -> Dict:
        return LangRegistry.REG[lang]
