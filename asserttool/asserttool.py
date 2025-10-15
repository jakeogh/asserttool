#!/usr/bin/env python3
# -*- coding: utf8 -*-
# disable: byte-vector-replacer

from __future__ import annotations

import inspect
import os
import sys
from typing import Any

from epprint import epprint

# enable other apps to "from asserttool import ic" with failback to epprint
ic: Any = None
icr: Any = None
icp: Any = None
try:
    from icecream import ic  # https://github.com/gruns/icecream

    ic.configureOutput(includeContext=True)
except ImportError:
    ic = epprint

try:
    from icecream import IceCreamDebugger

    icp = IceCreamDebugger()
    icp.configureOutput(includeContext=True)
    icp.enable()
except ImportError as e:
    epprint(f"{e=}")
    icp = epprint

    # try:
    #    from icecream import icr  # https://github.com/jakeogh/icecream
    # except ImportError:
    #    icr = epprint


def embed_ipdb():
    # pylint: disable=import-error
    import ipdb

    # pylint: enable=import-error

    ipdb.set_trace()


def pause(
    message: str = "",
    ipython: bool = False,
):
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
    return True


def am_root():
    if not root_user():
        epprint("You must run this as root.")
        sys.exit(1)
    return True


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
    if count in {0, 1}:
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


def all_or_none(
    thing,
    *,
    msg: None | str = None,
):
    target = len(thing)
    count = 0
    for x in thing:
        if bool(x):
            count += 1
    if count in {0, target}:
        return True
    if msg:
        raise ValueError(thing, msg)
    raise ValueError(thing)
