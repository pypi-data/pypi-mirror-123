import inspect
import json
import os
from pathlib import Path
from typing import List, Dict

from _pistar.pistar_pytest.utils import now
from _pistar.utilities.constants import ENCODE
from _pistar.utilities.constants import FILE_MODE
from _pistar.utilities.constants import PISTAR_TESTCASE_EXECUTION_STATUS as PISTAR_STATUS
from _pistar.utilities.constants import REPORT_TYPE
from _pistar.utilities.pytest import execute_pytest_testcases
from _pistar.utilities.report import generate_report_file
from _pistar.utilities.report import get_report_info
from .case import TestCase
from .collector import Collector, UsageError
from .exception import ExceptionInfo
from .terminal import console_output
from .terminal import console_summary_collection
from .terminal import console_testcase_end
from .terminal import console_testcase_start


class TESTCASE_TYPE:
    PISTAR = "pistar"
    PYTEST = "pytest"


def init_output_dir(output_directory):
    output_abspath = os.path.realpath(output_directory)
    if not os.path.exists(output_abspath):
        os.makedirs(output_abspath)
    return output_abspath


def legal_check(paths: List[str]) -> List[Path]:
    """
    Check path arguments and return List[Path].

    Command-line arguments can point to files or ONLY ONE directory, for example:

      "pkg/tests/test_foo.py pkg/tests/test_bar.py"

    or one directory:

      "pkg/tests/"

    This function ensures the path exists, and returns a List:

        (List[Path("/full/path/to/pkg/tests/test_foo.py")]

    If the path doesn't exist, raise UsageError.

    """
    absolute_paths: List[Path] = list()

    for it in paths:
        path = Path(it)
        if path.is_dir() and len(paths) > 1:
            msg = "pistar only support one directory argument"
            raise UsageError(msg)
        if not path.exists():
            msg = f"file or directory not found: {path}"
            raise UsageError(msg)
        absolute_paths.append(path.absolute())
    return absolute_paths


def group_by_folder(paths: List[Path]) -> Dict[str, List[Path]]:
    """
    Group test case by its parent path.

    In pistar,The cases which have same parent path
    have same scope.They will be collected by the
    same Collector.

    Nothing to do if path is a directory.
    """

    path_grouped_by = dict()
    for it in paths:
        path = Path(it)
        abs_path = path.absolute()
        parent = str(abs_path.parent) if abs_path.is_file() else str(abs_path)

        if parent not in path_grouped_by:
            path_grouped_by[parent] = list()

        path_grouped_by[parent].append(abs_path)
    return path_grouped_by


def execute(arguments):
    """
    description: the function is the entry of running testcases
    """
    start_time = now()
    output_abspath = init_output_dir(arguments.output)
    if arguments.type == TESTCASE_TYPE.PISTAR:

        collectors = pistar_collection(arguments.files_or_dir, Path(output_abspath))

        all_case_results = dict()

        for collect in collectors:
            run_loop = ExecuteFactory(collect)
            all_case_results.update(run_loop.execute(arguments))

        console_summary_collection(all_case_results, now() - start_time)
    elif arguments.type == TESTCASE_TYPE.PYTEST:
        execute_pytest_testcases(arguments)


def pistar_collection(args: List[str], output_path: Path) -> List[Collector]:
    """
    Perform the collection phase for the given session.
    """

    resolved_path = legal_check(args)
    group_by_cases = group_by_folder(resolved_path)
    collectors: List[Collector] = []
    testcase_num = 0
    console_output("collecting...")
    for path in group_by_cases:
        collect = Collector(Path(path), group_by_cases.get(path), output_path)
        collectors.append(collect)
        testcase_num += len(collect.testcases)
    if testcase_num == 1:
        info = "collected 1 test case\n"
    else:
        info = f"collected {testcase_num} test cases\n"
    console_output(info)
    return collectors


def generate_start_file(testcase_path, output_dir):
    start_data = dict()
    start_data["cur_script"] = testcase_path

    with open(os.path.join(output_dir, "task_meta_info.json"), mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as file:
        file.write(json.dumps(start_data, ensure_ascii=False, indent=4, default=str))


class ExecuteFactory:
    def __init__(self, collect: Collector):
        self.testcases = collect.testcases
        self.condition_manager = collect.condition_manager

    def execute(self, arguments):
        results = dict()
        for testcase in self.testcases:
            console_testcase_start(testcase)
            generate_start_file(inspect.getfile(testcase), arguments.output)
            case = TestCase(testcase, arguments)
            try:
                case.initialize_step()
            except BaseException:
                exc = ExceptionInfo.from_current()
                case.logger.error(exc.exc_with_tb())
            else:
                case.execute(self.condition_manager)
            finally:
                if testcase is self.testcases[-1]:
                    finish_condition = self.condition_manager.finish()
                    last_step = list(case.execute_records.keys())[-1]
                    case.execute_records.get(last_step)["after"] = finish_condition

                report_info = get_report_info(case, self.condition_manager, REPORT_TYPE.SINGLE)
                generate_report_file(case, report_info)
                results["::".join([case.path, case.testcase_class.__name__])] = (
                    PISTAR_STATUS.PASSED if case.execution_status == "0" else PISTAR_STATUS.FAILED
                )
                console_testcase_end(testcase)

        return results
