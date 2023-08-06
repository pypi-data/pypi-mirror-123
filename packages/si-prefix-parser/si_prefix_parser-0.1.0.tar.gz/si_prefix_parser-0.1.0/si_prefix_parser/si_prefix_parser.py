import re


def prefix_float(number: str):
    prefixes = ['K', 'M', 'G', 'T', 'P']

    val = float(re.search(r'-?\d+\.?\d*', number).group())

    for i, p in enumerate(prefixes):
        if p in number:
            return val * 1000**(i + 1)

    return val
