"""
description: this module provides report for each step.
"""
import inspect
from pathlib import Path
from typing import Dict

from _pistar.pistar_pytest.utils import uuid4
from _pistar.utilities.condition.condition import ConditionManager
from _pistar.utilities.constants import \
    PISTAR_TESTCASE_EXECUTION_STATUS as STATUS
from _pistar.utilities.constants import STEP_TYPE
from _pistar.utilities.testcase.case import TestCase


def duration_amend(duration):
    if duration > 0:
        return duration
    else:
        return 1


def _get_post_condition_info(con_manager: ConditionManager,
                             step_info: Dict,
                             step_record: Dict) -> None:
    step_info['after'] = list()
    for after in step_record.get('after', []):
        after_name = list(after.keys())[0]
        duration = con_manager.name2confunc.get(
            after_name).after_end_time - con_manager.name2confunc.get(
            after_name).after_start_time
        step_info['after'].append({
            'name': after_name,
            'result': STATUS.PASSED
            if not after.get(after_name) else STATUS.FAILED,
            'duration': duration_amend(duration)
        })


def _get_pre_condition_info(con_manager: ConditionManager,
                            step_info: Dict,
                            step_record: Dict) -> None:
    step_info['before'] = list()
    conditions_result = step_record.get('before', {})
    for before in conditions_result:
        _, conditions_exception = conditions_result.get(before)
        duration = con_manager.name2confunc.get(
            before).before_end_time - con_manager.name2confunc.get(
            before).before_start_time
        step_info['before'].append({
            'name': before,
            'result': STATUS.PASSED if not conditions_exception else STATUS.FAILED,
            'duration': duration_amend(duration)
        })


def _get_attachments(step_info: Dict, teststep: str,
                     testcase: TestCase) -> None:
    step_info['attachments'] = list()
    log_path = Path(testcase.testcase.logger_path)
    testcase_filename = Path(
        inspect.getfile(testcase.testcase_class)
    ).stem
    lastest_step = list(testcase.execute_records.keys())[-1]
    if log_path.is_file() and \
            teststep == lastest_step:
        step_info['attachments'].append({
            'name': testcase_filename + '.log',
            'type': 'text',
            'path': log_path
        })


def _get_actions(step_info: Dict, teststep: str, testcase: TestCase) -> None:
    step_info['actions'] = list()
    actions = testcase.testcase.action_word_information
    for action_caller in actions:
        if teststep in action_caller:
            duration_list = actions.get(action_caller)
            execute_times = len(duration_list)
            avg_duration = sum(duration_list) // execute_times
            step_info['actions'].append({
                'name': action_caller.split('.')[-1],
                'execute_times': execute_times,
                'avg_duration': duration_amend(avg_duration)
            })


class PistarReportInfo(dict):
    """
    description:new report class to create and save
    """

    def __init__(self, testcase, con_manager: ConditionManager):
        super().__init__()
        if getattr(testcase, 'testcase', None):
            self._get_case_execution_info(testcase, con_manager)
        else:
            self._get_case_unexecution_info()

    def _get_case_unexecution_info(self):
        self['details'] = list()

    def _get_case_execution_info(
            self,
            testcase,
            con_manager: ConditionManager):
        reports = getattr(testcase.testcase, 'reports', None)
        self['details'] = list()
        for teststep in testcase.execute_records:
            step_record = testcase.execute_records.get(teststep)
            step_info = dict()
            if reports and teststep in reports:
                step_info['report'] = reports.get(teststep)
            step_info['name'] = teststep
            step_info['start_time'] = step_record['start_time']
            step_info['end_time'] = step_record['end_time']
            duration = step_info['end_time'] - step_info['start_time']
            step_info['duration'] = duration_amend(duration)

            step_info['result'] = STATUS.PASSED if \
                step_record.get('status_code') == '0' else STATUS.FAILED
            step_info['description'] = teststep
            step_info['fullName'] = '::'.join(
                [testcase.testcase_class.__name__, teststep])
            step_info['uuid'] = uuid4()

            step_info['testCaseId'] = inspect.getfile(
                testcase.testcase_class
            )
            if teststep == 'setup':
                step_info['step_type'] = STEP_TYPE.SETUP
            elif teststep in ['teardown', 'failure']:
                step_info['step_type'] = STEP_TYPE.TEARDOWN
            else:
                step_info['step_type'] = STEP_TYPE.TESTSTEP

            step_info['labels'] = [
                {
                    'name': 'suite',
                    'value': testcase.testcase_class.__name__
                }
            ]

            _get_pre_condition_info(con_manager, step_info, step_record)
            _get_post_condition_info(con_manager, step_info, step_record)
            _get_attachments(step_info, teststep, testcase)
            _get_actions(step_info, teststep, testcase)

            exception = step_record.get('exception', None)
            step_info['exception'] = list()
            if exception:
                step_info['exception'].append(exception)

            self['details'].append(step_info)
