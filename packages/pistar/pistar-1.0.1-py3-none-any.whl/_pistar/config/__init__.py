import enum
import os
import sys
from typing import Optional, Union, List

from _pistar import VERSION
from _pistar.utilities.argument_parser import ArgumentParser
from _pistar.utilities.auto_generate import generate_file
from _pistar.utilities.exceptions import UsageError
from _pistar.utilities.testcase.execute_testcase import execute


class COMMANDS:
    GENERATE = "generate"
    EXECUTE = "run"


class ExitCode(enum.IntEnum):
    """Exit Code for PiStar."""

    #: run successfully.
    OK = 0
    #: misused.
    USAGE_ERROR = 4


def main(args: Optional[Union[List[str], "os.PathLike[str]"]] = None):
    argument_parser = _arg_configure()
    if args is None:
        args = sys.argv[1:]
    try:
        arguments = argument_parser.parse_args(args)
    except UsageError:
        return ExitCode.USAGE_ERROR

    if arguments.version:
        print('pistar', VERSION)
    elif arguments.command == COMMANDS.EXECUTE:
        try:
            execute(arguments)
        except UsageError as e:

            for msg in e.args:
                print(f"ERROR: {msg}")

            return ExitCode.USAGE_ERROR

    elif arguments.command == COMMANDS.GENERATE:
        generate_file(arguments)
    else:
        argument_parser.print_help()
    return ExitCode.OK


def _arg_configure() -> "ArgumentParser":
    """
    description: this function is used to parse the command line arguments.
    """
    argument_parser = ArgumentParser(prog="pistar", usage="pistar [options] <command> <args>")
    argument_parser.add_argument("-v", "--version", action="store_true", help="Show the version of pistar")
    subparsers = argument_parser.add_subparsers(dest="command", metavar="")

    _run_command(subparsers)
    _gen_command(subparsers)

    return argument_parser


def _gen_command(subparsers):
    generate_parser = subparsers.add_parser(
        COMMANDS.GENERATE,
        usage="pistar generate [options]",
        help="Generate interface test cases",
    )
    generate_parser.add_argument(
        "-i",
        "--interface",
        action="store",
        type=str,
        required=True,
        metavar="",
        help="Specify an OpenAPI definition file by swagger yaml to generate interface test case files",
    )
    generate_parser.add_argument(
        "-o",
        "--output",
        action="store",
        type=str,
        required=False,
        default=os.curdir,
        metavar="",
        help="Generate case files to the specified directory, the default value is current directory",
    )


def _run_command(subparsers):
    run_parser = subparsers.add_parser(
        COMMANDS.EXECUTE, prog='pistar run', usage="pistar run [options] files_or_dir",
        help="Execute test cases"
    )
    run_parser.add_argument(
        "files_or_dir",
        action="store",
        nargs="+",
        type=str,
        metavar='files_or_dir',
        help="Specify a list or directory of test case files",
    )
    run_parser.add_argument(
        "--type",
        action="store",
        type=str,
        default="pistar",
        choices=["pistar", "pytest"],
        required=False,
        help="Specify the type of test case, the default value is pistar",
    )
    run_parser.add_argument(
        "-o",
        "--output",
        action="store",
        type=str,
        required=False,
        default=os.curdir,
        metavar="",
        help="Specify the result output directory"
    )
    run_parser.add_argument(
        "--debug",
        action="store_true",
        help="Record pistar framework log",
    )


def console_main() -> int:
    """
    The CLI entry point for pistar.

    """
    return main()
