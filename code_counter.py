import sys
from argparse import ArgumentParser, Namespace
from typing import List

from modules.export import LangType, count_class, count_line_by_ext


def parse_args(args: List[str]) -> Namespace:
    parser = ArgumentParser(description='line / class counter for coding.', add_help=True)
    subparsers = parser.add_subparsers(dest='sub', title='Sub arguments')
    
    parser_line = subparsers.add_parser('count_line')
    parser_line.set_defaults(func = lambda config: count_line_by_ext(config.path, config.ext))
    parser_line.add_argument('path', action='store', type=str)
    parser_line.add_argument('ext', action='store', metavar='file_ext', type=str)

    parser_class = subparsers.add_parser('count_class')
    parser_class.set_defaults(func = lambda config: count_class(config.path, config.lang))
    parser_class.add_argument('path', action='store', type=str)
    parser_class.add_argument('lang', action='store', type=LangType, choices=[LangType.C_SHARP, LangType.JAVA])

    if len(args) == 0:
        parser.print_usage()
        sys.exit(0)
    return parser.parse_args(args)


if __name__ == '__main__':
    config = parse_args(sys.argv[1:])
    # print(config.__dict__)
    config.func(config)
