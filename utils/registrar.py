"""
Decorators for registering tests in different dictionaries.

This simplifies running all the tests as a group, since different tests may
need to be run in different ways.
"""
from functools import wraps

WORD_TESTS = {}
WORD_SET_TESTS = {}
PARAGRAPH_TESTS = {}


def word_test(fn):
    WORD_TESTS[fn.__name__] = fn
    return fn


def word_set_test(fn):
    WORD_SET_TESTS[fn.__name__] = fn
    return fn


def paragraph_test(fn):
    PARAGRAPH_TESTS[fn.__name__] = fn
    return fn
