import time
from Constant import PATH
import json

def write_log(log_str):
    with open(PATH + "/log.txt", 'a+', encoding='utf-8') as f:
        if type(log_str)==list:
            log_str=",".join([str(item) for item in log_str])
        if type(log_str)==dict:
            log_str = str(log_str)
        f.write("[LOG]" + str(time.time()) + ": " + log_str + "\n" )