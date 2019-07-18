import re

def num_validator(num):
    match = re.match(r"^[0-9]+",num)
    if match:
        return int(match.group())
    else:
        return False
