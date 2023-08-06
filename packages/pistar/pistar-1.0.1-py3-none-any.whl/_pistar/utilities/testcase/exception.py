import inspect
import sys
from traceback import format_exception_only, format_exception
from types import TracebackType, CodeType
from typing import Optional, Tuple, Type, TypeVar, List, Iterable, Generic

import attr
import py

_E = TypeVar("_E", bound=BaseException, covariant=True)


def get_tb_source_code(tb: TracebackType):
    try:
        sources, lineno = inspect.findsource(tb.tb_frame.f_code)
    except Exception:
        return None, -1
    lines = [line.rstrip() for line in sources]
    return lines, lineno


class TracebackItem:
    """A single entry in a Traceback."""

    __slots__ = "_origin_tb"

    def __init__(self, origin_tb: TracebackType) -> None:
        self._origin_tb = origin_tb

    @property
    def lineno(self) -> int:
        """Crash line of the traceback"""
        return self._origin_tb.tb_lineno

    @property
    def path(self) -> str:
        """Path to the source code."""
        return self._origin_tb.tb_frame.f_code.co_filename

    def get_first_line_source(self) -> int:
        """Get the first line of this callable object"""
        return self._origin_tb.tb_frame.f_code.co_firstlineno

    @property
    def full_source(self) -> List[str]:
        full, _ = get_tb_source_code(self._origin_tb)
        return full

    @property
    def crash_source(self) -> List[str]:
        code_first_lineno = self.get_first_line_source() - 1
        crash_line = self.lineno - 1

        return self.full_source[code_first_lineno : crash_line + 1]

    @property
    def origin_tb(self):
        return self._origin_tb


class TraceBack(List[TracebackItem]):
    def __init__(self, tb: TracebackType):
        if isinstance(tb, TracebackType):

            def trace_gen(cur: Optional[TracebackType]) -> Iterable[TracebackItem]:
                _cur = cur
                while _cur is not None:
                    yield TracebackItem(_cur)
                    _cur = _cur.tb_next

            super().__init__(trace_gen(tb))

    def pure(self, path, first_lineno) -> "TraceBack":

        for tb in self:
            code_path = tb.path
            code_first_lineno = tb.get_first_line_source()
            if path == code_path and first_lineno == code_first_lineno:
                return TraceBack(tb.origin_tb)
        return self


@attr.s(repr=False)
class ExceptionInfo(Generic[_E]):
    """Wraps sys.exc_info() objects and offers help for navigating the traceback."""

    _exc_info = attr.ib(type=Optional[Tuple[Type["_E"], "_E", TracebackType]])

    _traceback = attr.ib(type=TraceBack, default=None)

    @classmethod
    def from_exc_info(
        cls,
        exc_info: Tuple[Type[_E], _E, TracebackType],
    ) -> "ExceptionInfo[_E]":
        """Return an ExceptionInfo for an existing exc_info tuple."""

        return cls(exc_info)

    @classmethod
    def from_current(cls) -> "ExceptionInfo[BaseException]":
        """Return an ExceptionInfo matching the current traceback."""
        exc = sys.exc_info()
        if exc[0] is None or exc[1] is None or exc[2] is None:
            raise AssertionError("no current exception")
        exc_info = (exc[0], exc[1], exc[2])
        return ExceptionInfo.from_exc_info(exc_info)

    @property
    def type(self) -> Type[_E]:
        if self._exc_info is None:
            raise AssertionError(".type can only be used after the exception exits")
        return self._exc_info[0]

    @property
    def value(self) -> _E:
        if self._exc_info is None:
            raise AssertionError(".value can only be used after the exception exits")
        return self._exc_info[1]

    @property
    def tb(self) -> TracebackType:
        if self._exc_info is None:
            raise AssertionError(".tb can only be used after the exception exits")
        return self._exc_info[2]

    @property
    def traceback(self) -> TraceBack:
        if self._traceback is None:
            self._traceback = TraceBack(self.tb)
        return self._traceback

    @traceback.setter
    def traceback(self, value):
        self._traceback = value

    @property
    def type_name(self) -> str:
        return self.type.__name__

    def exc_only(self) -> str:
        lines = format_exception_only(self.type, self.value)
        text = "".join(lines)
        text = text.rstrip()

        return text

    def exc_with_tb(self) -> str:
        lines = format_exception(self.type, self.value, self.tb)
        text = "".join(lines)
        text = text.rstrip()

        return text


class ExcInfoFormatter:
    """
    Format an ExceptionInfo to get caller stack we really concern about.
    """

    def __init__(self, exc_info: ExceptionInfo, func: object, abspath: bool = False):
        self._exc_info = exc_info
        self._func = func
        self.flow_marker = ">"
        self.error_marker = "E"
        self._abspath = abspath

    def pure_traceback(self) -> None:
        """
        Try to cut traceback from the target function.Nothing to do if ExceptionInfo
        does not contain target function.
        """

        code = get_origin_code(self._func)
        file_name = code.co_filename
        lineno = code.co_firstlineno
        traceback = self._exc_info.traceback

        new_traceback = traceback.pure(path=file_name, first_lineno=lineno)

        if new_traceback is not traceback:
            self._exc_info.traceback = new_traceback

    def get_formatted_exc_info(self):
        # now we only show the first traceback only

        tb = self._exc_info.traceback[0]
        res = self.get_source(tb)
        res = res + self.error_marker + "   " + self._exc_info.exc_only()

        path = self._makepath(tb.path)
        res = res + "\n\n" + path + ":" + str(tb.lineno) + " " + self._exc_info.type.__name__

        return res

    def get_source(self, tb: TracebackItem):
        """
        Get an formatted string of crash code.
        :param tb: The tracebackItem to get its formatted source
        :return: formatted string of crash code
        """
        focus_source = tb.crash_source
        space_prefix = "    "
        res = ""

        source_index = len(focus_source) - 1
        for line in focus_source[:source_index]:
            res = f"{res}{space_prefix}{line}\n"
        res = res + f"{self.flow_marker}   {focus_source[source_index]}\n"

        return res

    def _makepath(self, path):
        if not self._abspath:
            try:
                best_rel_path = py.path.local().bestrelpath(path)
            except OSError:
                return path
            if len(best_rel_path) < len(str(path)):
                path = best_rel_path
        return path


def get_origin_code(obj: object) -> CodeType:
    try:
        return obj.__code__  # type: ignore[attr-defined]
    except AttributeError:
        raise TypeError("no code object found!")
