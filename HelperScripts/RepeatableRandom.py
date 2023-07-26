from numpy import random, format_float_positional
from HelperScripts.FindSigFigs import find_sigfigs

import hashlib


def repeatable_random(passed_seed, min_percent_range, passed_value, number_returned, random_sigfigs=False,
                      random_sigfig_range=1, whole_numbers=False):
    sigfigs = find_sigfigs(passed_value)
    int_seed = int(hashlib.md5(passed_seed.encode('utf-8')).hexdigest(), 16)
    rng = random.default_rng(seed=int_seed)
    negative_count = rng.integers(0, number_returned + 1, 1)
    range_min = passed_value - (passed_value * 2)
    range_max = passed_value - (passed_value * min_percent_range)
    negative_list = rng.uniform(range_min, range_max, negative_count)
    range_max = passed_value + (passed_value * 2)
    range_min = passed_value + (passed_value * min_percent_range)
    positive_list = rng.uniform(range_min, range_max, number_returned - negative_count)
    pre_format_list = (negative_list.tolist() + positive_list.tolist())
    pre_format_list.sort()
    formatted_list = []
    if sigfigs:
        for item in pre_format_list:
            if whole_numbers:
                item = round(item)
            formatted_item = None
            if random_sigfigs:
                up_or_down = rng.random()
                temp_sigfigs = sigfigs
                if up_or_down >= (2 / 3):
                    temp_sigfigs += rng.integers(0, random_sigfig_range + 1, 1)
                elif up_or_down <= (1 / 3):
                    temp_sigfigs -= rng.integers(0, random_sigfig_range + 1, 1)
                else:
                    pass
                if temp_sigfigs <= 0:
                    temp_sigfigs = 1
                temp_sigfigs = int(temp_sigfigs)
                formatted_item = format_float_positional(item, precision=temp_sigfigs, unique=False, fractional=False,
                                                         trim='k')
            else:
                formatted_item = format_float_positional(item, precision=sigfigs, unique=False, fractional=False,
                                                         trim='k')
            formatted_list.append(formatted_item)

    return formatted_list
