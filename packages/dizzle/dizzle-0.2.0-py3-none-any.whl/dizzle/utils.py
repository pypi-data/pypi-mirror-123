from sys import argv, stderr, exit


def get_arg(i: int, default=None):
    try:
        return argv[i]
    except IndexError:
        return default


def cry(*args, **kwargs):
    print(*args, **kwargs, file=stderr)


def fatal(exit_code, *args, **kwargs):
    cry(*args, **kwargs)
    exit(exit_code)
