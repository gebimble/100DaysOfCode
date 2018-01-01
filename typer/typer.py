"""Function for printing in an 'as typed' fashion."""

import sys
import time
from random import normalvariate
from typing import Dict


TimeDict = Dict[str, float]

def typer(str_to_print: str, times: Dict={}) -> None:
    """Producing 'as typed' style printing.

    Args:
        to_print - string to be printed.
        times - dictionary with times associated with each character.

    Returns:
        None

    Excepts:
        None"""

    key_set = set(times.keys())

    for char in str_to_print:
        sys.stdout.write(char)
        sys.stdout.flush()

        if char in key_set:
            time.sleep(times[char])
        else:
            time.sleep(normalvariate(0.05, 0.01))

    time.sleep(.5)
    print()

    return None
