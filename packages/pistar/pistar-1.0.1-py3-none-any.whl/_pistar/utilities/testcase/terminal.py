import shutil

from colorama import Fore

from _pistar.utilities.constants import PISTAR_TESTCASE_EXECUTION_STATUS as PISTAR_STATUS

width = shutil.get_terminal_size().columns - 2
log_sep = "-"
log_sep_summary = "="


def console_output(message):
    print(message)


def console_testcase_start(testcase):
    print(f" {testcase.__name__} start ".center(width, log_sep))


def console_testcase_end(testcase):
    print(f" {testcase.__name__} end ".center(width, log_sep) + "\n")


def format_time(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f}s "

    mm, ss = divmod(int(seconds), 60)
    hh, mm = divmod(mm, 60)
    dd, hh = divmod(hh, 24)
    if hh < 1:
        return f"{mm}m{ss}s "
    if dd < 1:
        return f"{hh}h{mm}m{ss}s "
    return f"{dd} days {hh}h{mm}m{ss}s " if dd > 1 else f"{dd} day {hh}h{mm}m{ss}s "


def console_summary_collection(results, time_consuming):
    passed_num = 0
    failed_num = 0
    passed_testcases = list()
    failed_testcases = list()

    for key, value in results.items():
        if value == PISTAR_STATUS.PASSED:
            passed_num += 1
            passed_testcases.append(key)
        else:
            failed_num += 1
            failed_testcases.append(key)

    if passed_num or failed_num:
        print(" test summary info ".center(width, log_sep_summary))

    for testcase in passed_testcases:
        print(Fore.GREEN + "PASSED", end=" ")
        print(Fore.RESET + testcase)
    for testcase in failed_testcases:
        print(Fore.RED + "FAILED", end=" ")
        print(Fore.RESET + testcase)

    summary_info = ""
    summary_info += f" {failed_num} failed" if failed_num else ""
    if failed_num != 0 and passed_num != 0:
        summary_info += ","
    summary_info += f" {passed_num} passed" if passed_num else ""

    summary_info += " in " if summary_info else "no test cases ran in "
    summary_info += format_time(time_consuming * 0.001)
    print(summary_info.center(width, log_sep_summary))
