"""Mygit Init."""
import argparse
import collections

# from .add_subparsers import add_clone, add_init, add_add

from . import add_subparsers
from .tools import print_version


def main():
    """These are common Git commands used in various situations."""
    # 创建命令解析器
    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # 添加主命令参数
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help=print_version.__doc__
    )
    # 将主命令绑定到特定的函数
    parser.set_defaults(func=parser.print_help)

    # 添加子命令
    subparsers = parser.add_subparsers()
    # funcs = [add_clone, add_init, add_add]
    # for func in funcs:
    #     func(subparsers)
    for func_name in add_subparsers.__all__:
        getattr(add_subparsers, func_name)(subparsers)

    # 解析所有参数
    cli_args = collections.namedtuple('cli_args', ['parsed', 'extra'])
    parsed, extra = parser.parse_known_args()
    args = cli_args(parsed, extra)
    if args.parsed.version:
        args.parsed.func = print_version

    # 执行命令对应的函数
    try:
        args.parsed.func(args)
    except (AttributeError, TypeError):
        # AttributeError: 'cli_args' object has no attribute 'write'
        args.parsed.func()


if __name__ == '__main__':
    main()
