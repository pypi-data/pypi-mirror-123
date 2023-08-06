import json
import os

from _pistar.utilities.condition.condition import ConditionManager
from _pistar.utilities.constants import ENCODE
from _pistar.utilities.constants import FILE_MODE
from _pistar.utilities.constants import PISTAR_TESTCASE_EXECUTION_STATUS as PISTAR_STATUS
from _pistar.utilities.constants import REPORT_TYPE
from .pistar_report_info import PistarReportInfo


def get_report_info(testcase, con_manager: ConditionManager, report_type=REPORT_TYPE.PISTAR):
    """
    description: get report data by report_type
    parameter:
        report_type:
            description: the report_type
            type:str
    return:
        report
    """
    report_info = PistarReportInfo(testcase, con_manager)

    return report_info


def generate_report_file(testcase, report_info):
    output_path = testcase.testcase.testcase_result_path
    for teststep in report_info.get("details"):
        report_json_file = ".".join([teststep.get("uuid") + "-result", "json"])
        with open(os.path.join(output_path, report_json_file), mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as file:
            json.dump(teststep, file, ensure_ascii=False, default=str)

    generate_finish_file(
        output_path=output_path,
        start_time=testcase.start_time,
        end_time=testcase.end_time,
        status=PISTAR_STATUS.PASSED if testcase.execution_status == "0" else PISTAR_STATUS.FAILED
    )


def generate_finish_file(output_path, start_time, end_time, status, exception_info=None):
    """
    description: the finished json file is used to offer the test case basic execution info.
    """

    finish_data = dict()
    finish_data["start_time"] = start_time
    finish_data["end_time"] = end_time
    finish_data["duration"] = end_time - start_time
    finish_data["result"] = status
    if exception_info:
        finish_data["exception"] = exception_info

    with open(os.path.join(str(output_path), "finished.json"), mode=FILE_MODE.WRITE, encoding=ENCODE.UTF8) as file:
        json.dump(finish_data, file, ensure_ascii=False, default=str)
