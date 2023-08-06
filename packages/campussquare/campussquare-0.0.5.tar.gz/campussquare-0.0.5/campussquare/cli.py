import sys
import datetime
import argparse
import json
from .errors import CampusSquareFlowError
from .campussquare import CampusSquare
from . import parser


class Authenticator():
    def login(self) -> CampusSquare:
        '''
        use refresh() instead on exception
        '''
        pass

    def refresh(self) -> CampusSquare:
        '''
        refresh on CampusSquareFlowError
        '''
        pass


def output(path: str, message: str):
    if path:
        with open(path, 'wt', encoding='utf-8') as f:
            f.write(message)
    else:
        print(message)


def _default_handler(args, next_handler, *, authenticator: Authenticator):
    try:
        campussquare = authenticator.login()
    except:
        campussquare = authenticator.refresh()

    for _ in range(3):
        try:
            next_handler(args, campussquare)
            break
        except CampusSquareFlowError:
            if 'n' == input('refresh (Y/n)'):
                break
            campussquare = authenticator.refresh()


def _syllabus_handler(args, campussquare: CampusSquare):
    campussquare.goto_syllabus_search()

    if args.command == 'search':
        res = campussquare.search_syllabus(
            year=args.year,
            subject=args.subject,
            day_of_week=args.dayofweek,
            period=args.period)
        if args.html:
            output(args.output, res.text)
        elif args.json:
            results = parser.parse_syllabus_search_result(res.text)
            output(args.output, json.dumps(results, ensure_ascii=False, indent=4))
        else:
            results = parser.parse_syllabus_search_result(res.text)
            table = parser.format_syllabus_search_result(results)
            output(args.output, table)

    elif args.command == 'get':
        assert args.code and args.affiliation
        res = campussquare.syllabus_detail(args.year, args.affiliation, args.code)
        if args.html:
            output(args.output, res.text)
        elif args.markdown:
            results = parser.parse_syllabus_detail(res.text)
            md = parser.format_syllabus_detail_markdown(results)
            output(args.output, md)
        else:
            results = parser.parse_syllabus_detail(res.text)
            output(args.output, json.dumps(results, ensure_ascii=False, indent=4))


def _grades_handler(args, campussquare: CampusSquare):
    campussquare.goto_grades()
    if args.command == 'get':
        res = campussquare.grades_detail(args.year, args.semester)
        if args.html:
            output(args.output, res.text)
        elif args.json:
            results = parser.parse_grades_detail(res.text)
            output(args.output, json.dumps(results, ensure_ascii=False, indent=4))
        elif args.markdown:
            raise RuntimeError('cannot format to markdown')
        else:
            results = parser.parse_grades_detail(res.text)
            table = parser.format_grades_detail(results)
            output(args.output, table)


def get_parser(*, authenticator: Authenticator):
    parser = argparse.ArgumentParser('campussquare')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--html', action='store_true')
    parser.add_argument('--markdown', '--md', action='store_true')
    parser.add_argument('--output', '-o', default='')
    subparser = parser.add_subparsers()

    syllabus = subparser.add_parser('syllabus')
    syllabus.add_argument('command', choices=['search', 'get'])
    syllabus.add_argument('--year', type=int, default=datetime.datetime.today().year)
    syllabus.add_argument('--subject', '-s')
    syllabus.add_argument('--code', '-c')
    syllabus.add_argument('--affiliation', '-t', type=int)
    syllabus.add_argument('--semester', type=int, choices=[1, 2])
    syllabus.add_argument('--dayofweek', type=int)
    syllabus.add_argument('--period', type=int)
    syllabus.set_defaults(handler=lambda args: _default_handler(
        args,
        _syllabus_handler,
        authenticator=authenticator
    ))

    grades = subparser.add_parser('grades')
    grades.add_argument('command', choices=['get'])
    grades.add_argument('--year', type=int)
    grades.add_argument('--semester', type=int, choices=[1, 2])
    grades.set_defaults(handler=lambda args: _default_handler(
        args,
        _grades_handler,
        authenticator=authenticator
    ))

    return parser


def parse_args_with_handler(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
