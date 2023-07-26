def find_sigfigs(number):
    """Returns the number of significant digits in a number"""

    # Turn it into a float first to take into account stuff in exponential
    # notation and get all inputs on equal footing. Then number of sigfigs is
    # the number of non-zeros after stripping extra zeros to left of whole
    # number and right of decimal
    # Not included
    number = repr(float(number))

    tokens = number.split('.')
    whole_num = tokens[0].lstrip('0')

    if len(tokens) > 2:
        raise ValueError('Invalid number "%s" only 1 decimal allowed' % (number))

    if len(tokens) == 2:
        decimal_num = tokens[1].rstrip('0')
        return len(whole_num) + len(decimal_num)

    return len(whole_num)