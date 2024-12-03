import numpy as np
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

input_file=sys.argv[1]
with open(input_file) as f:
    lines = f.readlines()
lines = [x.strip() for x in lines]

def is_safe_report(report):
    consec_diff = np.diff(report)
    cond1 = np.where(consec_diff < 1)
    cond2 = np.where(consec_diff > 3)
    cond = np.concatenate((cond1[0], cond2[0]))
    return cond1[0], cond2[0]

def is_safe_conds(cond1, cond2):
    if cond1.size == 0 and cond2.size == 0:
        return True
    elif (cond1.size + cond2.size) > 1:
        return False
    return False

def check_deleting_element(report, index):
    logging.debug(f'removing at: {index}: {report[index]}')
    new_report = np.delete(report, index)
    cond11,cond12 = is_safe_report(new_report)
    if is_safe_conds(cond11, cond12):
        return True
    return False
    
num_reports = 0
for l in lines:
    safe_report = False
    report = l.split(sep=' ')
    report = [int(r) for r in report]
    report = np.flip(report) if report[0] > report[-1] else report
    cond1, cond2 = is_safe_report(report)
    logging.debug(f'{report},{cond1},{cond2}')
    if is_safe_conds(cond1, cond2):
        safe_report = True
    elif cond1.size == 1:
        if check_deleting_element(report, cond1[0]):
            safe_report = True
        elif check_deleting_element(report, cond1[0]+1):
            safe_report = True
    if not safe_report and cond2.size == 1:
        if check_deleting_element(report, cond2[0]):
            safe_report = True
        elif check_deleting_element(report, cond2[0]+1):
            safe_report = True
    if safe_report:
        logging.debug(f'{report=} is safe')
        num_reports = num_reports + 1
    else:
        logging.debug(f'{report=} is not safe')
        pass
    logging.debug('-------------------')

print('number of safe reports:', num_reports)