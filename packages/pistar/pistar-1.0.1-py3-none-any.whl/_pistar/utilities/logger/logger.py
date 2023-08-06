"""
description: this module provides the class Logger.
"""

import os
import logging
import logging.handlers
import sys

import colorlog

from _pistar.utilities.constants import LOGGING_LEVEL
from _pistar.utilities.constants import ENCODE


class Logger(logging.Logger):
    """
    description: this class is the user logger of pistar.
    """

    __output_path = None
    __level = None
    __format = None
    __colors = None

    def __init__(self, name, level=LOGGING_LEVEL.DEBUG, logger_format=None,
                 output_path=None):
        super().__init__(name)

        self.__format = logger_format if logger_format else ' '.join(
            [
                '[%(asctime)s]',
                '[%(levelname)s]',
                '[%(name)s]',
                '[%(pathname)s:%(lineno)d]',
                '[%(message)s]'
            ]
        )
        self.__level = level
        self.__colors = {
            'DEBUG': 'fg_cyan',
            'INFO': 'fg_green',
            'WARNING': 'fg_yellow',
            'ERROR': 'fg_red',
            'CRITICAL': 'fg_purple'
        }

        self.__create_stream_handler()
        self.__output_path = output_path
        self.__create_file_handler()

    def __create_stream_handler(self):
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s' + self.__format + '%(reset)s',
            log_colors=self.__colors
        )

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(self.__level)
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def __create_file_handler(self):
        if not self.__output_path:
            return

        directory = os.path.dirname(self.__output_path)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)

        formatter = logging.Formatter(self.__format)

        handler = logging.FileHandler(
            self.__output_path,
            encoding=ENCODE.UTF8,
            delay=True
        )
        handler.setLevel(self.__level)
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def __delete_handlers(self, types):
        for handler in self.handlers:
            if not isinstance(handler, types):
                continue
            self.removeHandler(handler)

    @property
    def output_path(self):
        """
        description: return the private member __output_path.
        """

        return self.__output_path

    @output_path.setter
    def output_path(self, value):
        self.__output_path = value
        self.__delete_handlers(types=logging.FileHandler)
        self.__create_file_handler()


class ExecuteLogger(logging.Logger):
    """
        description: this class is the frame logger of pistar.
    """

    def __init__(self, name, level=LOGGING_LEVEL.DEBUG, logger_format=None,
                 output_path=None):
        super().__init__(name)

        self.__format = logger_format if logger_format else ' '.join(
            [
                '[%(asctime)s]',
                '[%(levelname)s]',
                '[%(name)s]',
                '[%(pathname)s:%(lineno)d]',
                '[%(message)s]'
            ]
        )
        self.__level = level

        self.__output_path = output_path
        self.__create_file_handler()

    def __create_file_handler(self):
        if not self.__output_path:
            return

        directory = os.path.dirname(self.__output_path)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)

        formatter = logging.Formatter(self.__format)

        handler = logging.FileHandler(
            self.__output_path,
            encoding=ENCODE.UTF8
        )
        handler.setLevel(self.__level)
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def __delete_handlers(self, types):
        for handler in self.handlers:
            if not isinstance(handler, types):
                continue
            self.removeHandler(handler)

    @property
    def output_path(self):
        """
        description: return the private member __output_path.
        """

        return self.__output_path

    @output_path.setter
    def output_path(self, value):
        self.__output_path = value
        self.__delete_handlers(types=logging.FileHandler)
        self.__create_file_handler()
