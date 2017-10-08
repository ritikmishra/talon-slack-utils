import traceback
from inspect import getframeinfo, currentframe

from happylogger.log import properties
from datetime import datetime
import time
import os


def line_num():
    """
    Returns the line number of where the user called a logging function
    
    :return: The linenumber, unless properties.print_line_num == Falsew
    """
    if properties.print_line_num:
        # One f.back to get to build_string
        # another one too get to err()/warn()/success()
        # a third to get to user call
        return ":" + str(currentframe().f_back.f_back.f_back.f_lineno)
    else:
        return ""


def filename():
    """    
    :return: Returns the name of the file in which the logging function was called 
    """
    return getframeinfo(currentframe().f_back.f_back.f_back).filename


def build_string(mode, text):
    """
    Create most of the string for a log. 
    
    :param mode: ERR, SUC, WARN
    :param text: 
    :return: 
    """
    result = "[" + mode + "]"
    if properties.print_time:
        clock_time = datetime.now()
        hh = format(clock_time.hour, '02d')
        mm = format(clock_time.minute, '02d')
        ss = format(clock_time.second, '02d')
        result += "[" + hh + ":" + mm + ":" + ss + "]"

    if properties.print_file_name and properties.print_file_path:
        result += "[" + filename() + line_num() + "]"
    elif properties.print_file_name:
        result += "[" + os.path.basename(filename()) + line_num() + "]"
    elif properties.print_file_path:
        result += "[" + os.path.dirname(os.path.abspath(filename())) + "]"

    for func in properties.funcs:
        result += "[" + str(func()) + "]"

    result += " " + str(text)

    return result


if __name__ == '__main__':
    for i in range(10):
        print(build_string("hello"))
        time.sleep(1)
