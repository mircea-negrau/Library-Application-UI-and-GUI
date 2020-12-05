def print_red(text, ending):
    print("\033[91m{}\033[00m".format(text), end=ending)


def print_error(text, ending):
    print("\033[1m\033[91m{}\033[00m".format(text), end=ending)


def print_yellow(text, ending):
    print("\033[93m{}\033[00m".format(text), end=ending)


def print_green(text, ending):
    print("\033[32m{}\033[00m".format(text), end=ending)


def print_successful(text, ending):
    print("\033[1m\033[32m{}\033[00m".format(text), end=ending)


def print_cyan(text, ending):
    print("\033[96m{}\033[00m".format(text), end=ending)


def print_orange(text, ending):
    print("\033[33m{}\033[00m".format(text), end=ending)


def print_blue(text, ending):
    print("\033[34m{}\033[00m".format(text), end=ending)


def print_white(text, ending):
    print("\033[67m{}\033[00m".format(text), end=ending)