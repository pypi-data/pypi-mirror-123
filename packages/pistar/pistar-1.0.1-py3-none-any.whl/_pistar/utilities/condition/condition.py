import functools
import inspect
from typing import TypeVar, Callable, Optional, Union, cast, List, Dict

import attr

from _pistar.pistar_pytest.utils import now

ConditionFunction = TypeVar("ConditionFunction", bound=Callable[..., object])


@attr.s(frozen=True)
class ConditionMarker:
    """
    The real implement of condition decorator.
    """

    scope = attr.ib(type=str)

    def __call__(self, function: ConditionFunction) -> ConditionFunction:

        if inspect.isclass(function):
            raise ValueError("class conditions not supported")
        if inspect.iscoroutinefunction(function):
            raise ValueError("coroutine condition not supported")

        function = can_not_call_directly(function)

        setattr(function, "_pistarconditionmarker", self)

        return function


def condition(
    condition_function: Optional[ConditionFunction] = None, *, scope="session"
) -> Union[ConditionMarker, ConditionFunction]:
    """Decorator to mark a condition factory function.

    This decorator can be used, with or without parameters, to define a
    condition function.

    Test steps can directly use condition names as parameters in which
    step the result returned from the condition function will be
    injected.

    Conditions can provide their values to test step using ``return`` or
    ``yield`` statements. When using ``yield`` the code block after the
    ``yield`` statement is executed as teardown code regardless of the test
    outcome, and must yield exactly once.

    :param condition_function:
        This is the fixed parameter for decorator to pass the decorated function.
        DO NOT USE IT!!!
    :param scope:
        The scope for which this condition is shared;Only Support session now.
    """
    condition_mark = ConditionMarker(scope)

    if condition_function:
        return condition_mark(condition_function)

    return condition_mark


def can_not_call_directly(function: ConditionFunction) -> ConditionFunction:
    """
    Wrap a given condition function.If a function decorated by
    condition were called directly,raise an error.
    """
    message = (
        f"Condition {function.__name__} called directly.\n"
        "PiStar will schedule condition function automatically "
        "when test cases request condition as parameter"
    )

    @functools.wraps(function)
    def wrap(*args, **kwargs):
        raise ValueError(message)

    wrap.__origin_func__ = function  # type: ignore[attr-defined]

    return cast(ConditionFunction, wrap)


class ConditionDef:
    """
    A container for a factory definition.
    """

    def __init__(self, conmanager: "ConditionManager", name, func, scope):
        self._condition_manager = conmanager
        self.name = name
        self.func = func
        self.scope = scope
        self.post_func: List[Callable[[], object]] = []
        self.cache_result = None
        self.before_start_time = None
        self.before_end_time = None
        self.after_start_time = None
        self.after_end_time = None

    def execute(self):
        if self.cache_result is not None:
            return self.cache_result
        result = [None, None]

        self.before_start_time = now()
        try:
            result[0] = self.call_condition_func()
        except BaseException as e:
            result[1] = e
        self.before_end_time = now()
        self.cache_result = result
        return result

    def finish(self):
        exception = None
        try:
            while self.post_func:
                self.after_start_time = now()
                try:
                    func = self.post_func.pop()
                    func()
                except BaseException as _exception:
                    exception = _exception
        finally:
            self.after_end_time = now()
            self.cache_result = None
            self.post_func = []
        return exception

    def call_condition_func(self):
        if inspect.isgeneratorfunction(self.func):
            generator = self.func()
            try:
                result = next(generator)
            except StopIteration as e:
                raise ValueError(f"{self.name} did not yield a value") from e
            post_yield = functools.partial(post_yield_func, self.name, generator)
            self.post_func.append(post_yield)

        else:
            result = self.func()
        return result


class ConditionManager:
    """
    pistar condition definitions and information is stored and managed
    from this class.
    """

    def __init__(self):
        self.name2confunc: Dict[str, ConditionDef] = {}

    def add(self, confunc: ConditionDef):
        con_name = confunc.name
        self.name2confunc[con_name] = confunc

    def execute(self, con_name):
        if con_name in self.name2confunc:
            return self.name2confunc.get(con_name).execute()

    def finish(self):
        finish_conditions = list()
        for name, confunc in self.name2confunc.items():
            if confunc.post_func:
                result = confunc.finish()
                finish_conditions.append({name: result})
        return finish_conditions


def post_yield_func(condition_name, generator) -> None:
    try:
        next(generator)
    except StopIteration:
        pass
    else:
        raise ValueError(f"{condition_name} yield twice")
