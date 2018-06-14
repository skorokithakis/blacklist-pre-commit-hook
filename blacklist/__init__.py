#!/usr/bin/env python

from __future__ import unicode_literals

import argparse
import ast
import collections
import sys

Infraction = collections.namedtuple("Infraction", ["name", "line", "column"])


class ASTVisitor(ast.NodeVisitor):
    def __init__(self, blacklisted_names, source_lines, ignore=None):
        self.infractions = []
        self.source_lines = source_lines
        self.blacklisted_names = blacklisted_names
        self.ignore = set(ignore) if ignore else set()

    def visit_Call(self, node):
        super(self, visit_Call).generic_visit(node)
        func = node.func

        if hasattr(func, "attr"):
            name = func.attr
        elif hasattr(func, "id"):
            name = func.id
        else:
            return

        if name in self.blacklisted_names and b"noqa" not in self.source_lines[node.lineno - 1]:
            self.infractions.append(Infraction(name, node.lineno, node.col_offset))


def check_file_for_infractions(filename, blacklisted_names, ignore=None):
    source = open(filename, "rb").read()
    tree = ast.parse(source, filename=filename)
    visitor = ASTVisitor(blacklisted_names, source_lines=source.split(b"\n"), ignore=ignore)
    visitor.visit(tree)
    return visitor.infractions


def parse_args(argv):
    def parse_ignore(value):
        return set(value.split(","))

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    parser.add_argument("--ignore", type=parse_ignore, default=set())
    parser.add_argument("-b", "--blacklisted-names", default="eval")

    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    blacklisted_names = args.blacklisted_names.split(",")
    rc = 0
    for filename in args.filenames:
        calls = check_file_for_infractions(filename, blacklisted_names, ignore=args.ignore)
        if calls:
            rc = rc or 1
        for call in calls:
            print(
                "{filename}:{call.line}:{call.column} - Blacklisted function: {call.name}".format(
                    filename=filename, call=call
                )
            )
    return rc


if __name__ == "__main__":
    sys.exit(main())
