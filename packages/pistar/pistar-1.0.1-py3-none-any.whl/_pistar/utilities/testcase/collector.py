import importlib
import inspect
import os
import sys
from pathlib import Path
from typing import List, Generator, Optional
import yaml

from _pistar.utilities import BaseTestCase
from _pistar.pistar_pytest.utils import now, sha256
from _pistar.utilities.constants import PISTAR_TESTCASE_EXECUTION_STATUS as PISTAR_STATUS
from _pistar.utilities.condition.condition import ConditionManager, ConditionDef
from _pistar.utilities.report.report_factory import generate_finish_file
from _pistar.utilities.testcase import has_teststep
from _pistar.utilities.testcase.terminal import console_output
from _pistar.utilities.exceptions import UsageError

CONDITION_FILE = "condition.py"


def pi_environment():
    workspace = Path(os.getcwd())
    env_path = workspace.joinpath("environment.yaml")
    if not env_path.is_file():
        raise IOError("Cannot find the file environment.yaml")
    with open(env_path, mode="r", encoding="utf-8") as f:
        env = yaml.load(f, Loader=yaml.SafeLoader)
        return env


def hasinit(obj: object) -> bool:
    init: object = getattr(obj, "__init__", None)
    return init != object.__init__


def hasnew(obj: object) -> bool:
    new: object = getattr(obj, "__new__", None)
    return new != object.__new__


def has_para_init(obj: object) -> bool:
    if hasinit(obj):
        new = getattr(obj, "__init__", None)
        sig = inspect.signature(new)
        return len(sig.parameters) > 1
    return False


def get_module_name(rel_path: Path):
    """
    description: the function is used to convert a path to a module.
    """
    if not (rel_path.is_file() and rel_path.match("*.py")):
        return None
    names = list(rel_path.with_suffix("").parts)

    if names[-1] == "__init__":
        names.pop()
    module_name = ".".join(names)

    return module_name


def get_testcase_from_module(module, abs_path):
    """
    description: the function is used to get the testcase class in the module
    """
    for item in dir(module):
        if item.startswith("_"):
            continue
        obj = getattr(module, item, None)
        if is_test_case(obj) and inspect.getfile(obj) == abs_path:
            return obj
    return None


def is_test_case(obj) -> bool:
    """Return True is the object is a Pistar TestCase and has test_step function."""
    return inspect.isclass(obj) and issubclass(obj, BaseTestCase) and has_teststep(obj)


def import_module(module_name):
    """
    description: the function is used to import the module
    """
    try:
        module = importlib.import_module(module_name)
        return module
    except BaseException as exception:
        console_output(f"fail to import {module_name}: {exception}")
        raise exception


def get_result_path(output_path, rel_path):
    result_path = output_path.joinpath(sha256(str(rel_path.absolute())))
    result_path.mkdir(parents=True, exist_ok=True)
    return result_path


def load_test_case(rel_path: Path, output_path: Path):
    if rel_path.name == CONDITION_FILE:
        return None
    module_name = get_module_name(rel_path)
    if not module_name:
        return None
    try:
        module = import_module(module_name)
    except BaseException as excpetion:
        result_path = get_result_path(output_path, rel_path)
        current_time = now()
        generate_finish_file(result_path, current_time, current_time, PISTAR_STATUS.ERROR, str(excpetion))
        return None

    testcase = get_testcase_from_module(module, str(rel_path.absolute()))
    if testcase:
        if has_para_init(testcase) or hasnew(testcase):
            abs_path = rel_path.absolute()
            msg = (
                f"{abs_path}:Warning: cannot collect case {testcase.__name__},"
                f"because it has a parameterized __init__ or __new__ constructor. "
            )
            console_output(msg)
            result_path = get_result_path(output_path, rel_path)
            current_time = now()
            generate_finish_file(result_path, current_time, current_time, PISTAR_STATUS.ERROR, msg)
            return None

    return testcase


def get_test_cases_from_path(rel_path: Path, output_path: Path):
    """
    description: the function is used to collect the testcases in the path
    """
    test_cases = list()
    if rel_path.is_file():
        test_case = load_test_case(rel_path, output_path)
        if test_case:
            test_cases.append(test_case)
    if rel_path.is_dir():
        for path in rel_path.iterdir():
            if path.is_file() and path.match("*.py"):
                test_case = load_test_case(path, output_path)
                if test_case:
                    test_cases.append(test_case)

    return test_cases


def collect_condition(module) -> Generator[None, None, None]:
    """
    description: the function is used to collect the conditions in the path
    """
    for item in dir(module):
        if item.startswith("_"):
            continue
        obj = getattr(module, item, None)
        if hasattr(obj, "_pistarconditionmarker"):
            yield obj


def get_condition_from_path(scope_dir: Path):
    """
    description: the function is used to find the condition.py in the directory.
                 now the condition must be defined in the condition.py and must in
                 the same directory as the testcases call it.
    """
    condition_path = scope_dir.joinpath(CONDITION_FILE)
    if not condition_path.exists():
        return []

    module_name = get_module_name(condition_path)

    if not module_name:
        return []
    module = import_module(module_name)
    condition = list(collect_condition(module))
    return condition


class Collector:
    """
    Collector instances collect test case and conditions from specific scope.

    In pistar,test cases own same parent directory have same scape.

    Condition.py in this scope will be collected,while test cases can use

    conditions in this scope.

    Because pistar only support files or ONLY ONE directory,suppose the parameter

    is legal.

    :param scope:
        The scope of the paths list.
    :param paths:
        The files path list.Same as scope if paths is directory.
    """

    def __init__(self, scope: Path, paths: List[Path], output_path: Path):

        self.testcases = list()
        self.condition_list: Optional[List] = None
        self.scope = scope.absolute()
        self.condition_manager = ConditionManager()

        workspace = os.getcwd()
        if workspace not in str(self.scope):
            msg = "the case path is not in workspace directory"
            raise UsageError(msg)

        if str(scope) not in sys.path:
            sys.path.append(str(scope))
        if workspace not in sys.path:
            sys.path.append(workspace)

        for path in paths:
            rel_path = path.relative_to(workspace)
            self.testcases += get_test_cases_from_path(rel_path, output_path)

        if not self.testcases:
            return
        try:
            self.condition_list = get_condition_from_path(scope.relative_to(workspace))
        except BaseException:
            msg = "import condition failed! please check the condition.py"
            raise UsageError(msg)

        self._inject_conditions()

    def _inject_conditions(self):

        if self.condition_list:
            for condition in self.condition_list:
                scope = getattr(condition, "_pistarconditionmarker", None)
                confunc = ConditionDef(
                    self.condition_manager,
                    condition.__name__,
                    condition.__origin_func__,
                    scope,
                )
                self.condition_manager.add(confunc)
        self.condition_manager.add(
            ConditionDef(
                self.condition_manager,
                pi_environment.__name__,
                pi_environment,
                "session",
            )
        )
