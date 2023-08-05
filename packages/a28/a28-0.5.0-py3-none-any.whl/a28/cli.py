#!/usr/bin/env python
# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
#    _                ___ ___   _____       _             _           _
#   /_\  _ _ ___ __ _|_  | _ ) |_   _|__ __| |_  _ _  ___| |___  __ _(_)___ ___
#  / _ \| '_/ -_) _` |/ // _ \   | |/ -_) _| ' \| ' \/ _ \ / _ \/ _` | / -_|_-<
# /_/ \_\_| \___\__,_/___\___/   |_|\___\__|_||_|_||_\___/_\___/\__, |_\___/__/
#                                                               |___/
"""Build packages to be submitted to Area28."""
import argparse
import sys
from a28 import __version__, package, system


def main(args=None):
    """Main command line entry point."""
    args = args or sys.argv[1:]
    parser = argparse.ArgumentParser(
        'a28',
        description='Area28 development kit'
    )
    app = '%(prog)s version ' + __version__
    parser.add_argument('-v', '--version', action='version', version=app)
    sub = parser.add_subparsers(dest='action', required=True, help='actions')
    package.options(sub)
    system.options(sub)
    args = parser.parse_args(args)
    args.func(args)
