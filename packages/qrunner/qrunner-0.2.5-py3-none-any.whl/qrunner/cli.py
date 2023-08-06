import argparse
import sys
from qrunner import __version__, __description__
from qrunner.scaffold import init_parser_scaffold, init_parser_scaffold_ios, main_scaffold, main_scaffold_ios


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-V", "--version", dest="version", action="store_true", help="show version"
    )

    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_scaffold = init_parser_scaffold(subparsers)
    sub_parser_scaffold_ios = init_parser_scaffold_ios(subparsers)

    if len(sys.argv) == 1:
        # qrunner
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-V", "--version"]:
            # httprunner -V
            print(f"{__version__}")
        elif sys.argv[1] in ["-h", "--help"]:
            # httprunner -h
            parser.print_help()
        # elif sys.argv[1] == "startproject":
        #     # httprunner startproject
        #     sub_parser_scaffold.print_help()
        elif sys.argv[1] == "startproject":
            # httprunner startproject
            sub_parser_scaffold.print_help()
        elif sys.argv[1] == "start_ios_project":
            # httprunner startproject
            sub_parser_scaffold_ios.print_help()
        sys.exit(0)

    args = parser.parse_args()
    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    if sys.argv[1] == "startproject":
        main_scaffold(args)
    elif sys.argv[1] == "start_ios_project":
        main_scaffold_ios(args)


if __name__ == "__main__":
    main()
