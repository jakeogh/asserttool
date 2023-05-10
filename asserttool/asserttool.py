#!/usr/bin/env python3
# -*- coding: utf8 -*-
# disable: byte-vector-replacer

# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=fixme                           # [W0511] todo is encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement

from __future__ import annotations

import inspect
import os
import sys
from typing import Any

from epprint import epprint
from globalverbose import gv
from globalverbose import gvd

# enable other apps to "from asserttool import ic" with failback to epprint
ic: Any = None
icr: Any = None
icp: Any = None
try:
    from icecream import ic  # https://github.com/gruns/icecream
except ImportError:
    ic = epprint

try:
    from icecream import IceCreamDebugger

    icp = IceCreamDebugger()
except ImportError:
    icp = epprint

try:
    from icecream import icr  # https://github.com/jakeogh/icecream
except ImportError:
    icr = epprint

# def all_none(obj: object, verbose: bool|int|float):
#    for i in obj:
#        if i:
#            return False


# woah... sloooooo
def disable_increment_debug(f):
    def inner(*args, **kwargs):
        stack = inspect.stack()
        depth = len(stack)
        # ic(depth, f)
        # if 'verbose' in kwargs.keys():
        #    ic(depth, kwargs['verbose'])

        # ic(depth, args, kwargs)  # gonna break stuff when this is used for __init__
        if "verbose" in kwargs.keys():
            if not isinstance(kwargs["verbose"], bool):
                current_verbose = kwargs["verbose"]
                # ic(depth, current_verbose)
                kwargs["verbose"] = max(current_verbose - depth, 0)
                # ic(depth, kwargs['verbose'])
            # ic(kwargs['verbose'])
        if "debug" in kwargs.keys():
            if not isinstance(kwargs["debug"], bool):
                current_verbose = kwargs["debug"]
                kwargs["debug"] = max(current_verbose - depth, 0)
            # ic(kwargs['debug'])
        return f(*args, **kwargs)

    return inner


def validate_slice(slice_syntax: str):
    assert isinstance(slice_syntax, str)
    assert slice_syntax.startswith("[")
    assert slice_syntax.endswith("]")
    for c in slice_syntax[1:-1]:
        if c not in [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "-",
            ":",
        ]:
            raise ValueError(slice_syntax)
    return slice_syntax


def click_validate_slice(ctx, param, value):
    # ic(param, value)
    if value is not None:
        validate_slice(value)
        return value


def embed_ipdb():
    # pylint: disable=import-error
    import ipdb

    # pylint: enable=import-error

    ipdb.set_trace()


def pause(message: str = "", ipython: bool = False):
    assert isinstance(message, str)
    if ipython:
        message += " (type 'ipython' to enter shell or 'ipdb' to enter debugger): "
    response = input(message)
    if response == "ipdb":
        embed_ipdb()
        pause("press enter to continue execution")
    elif response == "ipython":
        from IPython import embed

        embed()
        pause("press enter to continue execution")


def root_user():
    if os.getuid() == 0:
        return True
    return False


def not_root():
    if root_user():
        epprint("Dont run this as root!")
        sys.exit(1)
        # raise ValueError('Dont run this as root!')


def am_root():
    if not root_user():
        epprint("You must run this as root.")
        sys.exit(1)


def one(thing, *, msg: None | str = None):
    count = 0
    for x in thing:
        # eprint("x:", x, bool(x))
        if bool(x):
            count += 1
    # count = sum(1 for x in thing if bool(x))
    if count == 1:
        return True
    if msg:
        raise ValueError(thing, msg)
    raise ValueError(thing)


def maxone(thing, *, msg: None | str = None):
    count = 0
    for x in thing:
        if bool(x):
            count += 1
    if count in [0, 1]:
        return True
    if msg:
        raise ValueError(thing, msg)
    raise ValueError(thing)


def minone(
    thing,
    *,
    msg: None | str = None,
):
    count = 0
    for x in thing:
        if bool(x):
            count += 1
    if count >= 1:
        return True
    if msg:
        raise ValueError(thing, msg)
    raise ValueError(thing)
