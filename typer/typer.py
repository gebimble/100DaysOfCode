#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Function for printing in an 'as typed' fashion."""
import sys
import time
from random import choice, normalvariate, uniform
from typing import Dict


TimeDict = Dict[str, float]

# create list of letters a-z
alphas = [chr(x) for x in range(97, 123)]


def del_mistake(mistakes: int = 1) -> None:
    """Delete's mistake."""
    sys.stdout.write(mistakes*'\b')
    sys.stdout.write(' \b')
    sys.stdout.flush()
    time.sleep(normalvariate(0.2, 0.01))

    return None


def mistake(correct: str, incorrect: str) -> True:
    """Write's the incorrect character, then deletes it, writing the correct
    one."""
    sys.stdout.write(incorrect)
    sys.stdout.flush()

    time.sleep(normalvariate(0.5, 0.01))

    del_mistake()
    sys.stdout.write(correct)
    sys.stdout.flush()

    return True


def typer(str_to_print: str, times: Dict = {}) -> None:
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

        if uniform(0, 1) >= 0.9:

            mistake_char = choice(alphas)

            while mistake_char is char:
                mistake_char = choice(alphas)
            else:
                mistake(char, choice(alphas))

        else:
            sys.stdout.write(char)

        sys.stdout.flush()

        if char in key_set:
            time.sleep(times[char])
        else:
            time.sleep(normalvariate(0.05, 0.01))

    time.sleep(.5)
    print()

    return None


if __name__ == '__main__':
    string_to_print = "Hello, dog.\nWho's a good boy? Is it you?\nYes. Yes it is."
    time_dictionary = {
        '.': 1.,
        ',': .5,
        ';': .7,
        ':': .8,
        '?': 1.,
        '!': 1.,
        ' ': .1,
    }

    typer(string_to_print, time_dictionary)
