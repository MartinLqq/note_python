from argparse import Namespace


def print_version():
    """Print the version of my_git."""
    print('my_git version 0.0.1.windows.1')


def clone(args: Namespace):
    print('executing: mygit clone... Params: ')
    print(args)


def init(args: Namespace):
    print('executing: mygit init... Params: ')
    print(args)


def add(args: Namespace):
    print('executing: mygit add... Params: ')
    print(args)


def sub_clone_test(args: Namespace):
    print('executing: mygit clone sub-clone... Params: ')
    print(args)
