"""
generate verify codes
"""

import random

DIC = {}


def new_code(email):
    """
    generate new code
    """
    code = random.randint(100000, 999999)
    DIC[email] = code
    return code


def verify(email, code):
    """
    verify
    """
    try:
        if str(DIC[email]) == str(code):
            del DIC[email]
            return True
        return False
    except KeyError:
        return False
