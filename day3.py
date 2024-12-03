import numpy as np
import sys
import logging
import re
logging.basicConfig(level=logging.DEBUG)
from pathlib import Path

input_file=sys.argv[1]
content = Path(input_file).read_text()

total = 0
do_pattern = re.compile(r'do\(\)')
donot_pattern = re.compile(r'don\'t\(\)')
mul_pattern = re.compile(r'mul\([0-9]{1,3},[0-9]{1,3}\)')
found1 = re.search(do_pattern, content)
found2 = re.search(donot_pattern, content)
found3 = re.search(mul_pattern, content)
enabled=True
while found1 or found2 or found3:
    fs = [found1, found2, found3]
    fs_valid = [f for f in fs if f is not None]
    fs_valid.sort(key=lambda x: x.start())
    found = fs_valid[0]
    if found is None:
        break

    if found.group() == 'do()':
        enabled = True
    elif found.group() == 'don\'t()':
        enabled = False
    elif found.group().startswith('mul'):
        if enabled:
            nums = re.findall(r'\d+', found.group())
            if len(nums) != 2:
                logging.debug(f'Error: {nums}')
                break
            product = int(nums[0]) * int(nums[1])
            total = total + product
    print(f'{found.group()} at {found.start()}, ended at {found.end()}')
    found1 = do_pattern.search(content, found.end())
    found2 = donot_pattern.search(content, found.end())
    found3 = mul_pattern.search(content, found.end())

logging.debug(f'total = {total}')