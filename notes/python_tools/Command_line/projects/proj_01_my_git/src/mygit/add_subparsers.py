import argparse
from argparse import _SubParsersAction

from .tools import clone, init, add, sub_clone_test


def add_clone(subparsers: _SubParsersAction):
    """Clone a repository into a new directory."""
    clone_parser = subparsers.add_parser(
        name='clone',
        help=add_clone.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    clone_parser.add_argument(
        'path',
        action='store',
        help='The repository path.',
    )
    clone_parser.add_argument(
        '--no-tags',
        action='store_true',
        help="don't clone any tags, and make later fetches not to follow them"
    )
    clone_parser.set_defaults(func=clone)


def add_init(subparsers: _SubParsersAction):
    """Create an empty Git repository or reinitialize an existing one."""
    init_parser = subparsers.add_parser(
        name='init',
        help=add_init.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    init_parser.add_argument(
        '--bare',
        action='store_true',
        help='create a bare repository',
    )
    init_parser.set_defaults(func=init)


def add_add(subparsers: _SubParsersAction):
    """Add file contents to the index."""
    add_parser = subparsers.add_parser(
        name='add',
        help=add_add.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    add_parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='allow adding otherwise ignored files',
    )
    add_parser.set_defaults(func=add)


__all__ = [add_clone.__name__, add_init.__name__, add_add.__name__]
