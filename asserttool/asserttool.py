#!/usr/bin/env python3
# -*- coding: utf8 -*-

# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement

import inspect
import os
import sys
from math import inf
from typing import Union

import click
from epprint import epprint

try:
    from icecream import ic  # https://github.com/gruns/icecream
    from icecream import icr  # https://github.com/jakeogh/icecream
except ImportError:
    ic = epprint
    icr = epprint


def increment_debug(f):
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


def validate_slice(slice_syntax):
    assert isinstance(slice_syntax, str)
    assert slice_syntax.startswith("[")
    assert slice_syntax.endswith("[")
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
    import ipdb

    ipdb.set_trace()


def pause(message="", ipython=False):
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
        ic("Dont run this as root!")
        sys.exit(1)
        # raise ValueError('Dont run this as root!')


def am_root():
    if not root_user():
        ic("You must run this as root.")
        sys.exit(1)


def one(thing, *, msg=None):
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


def maxone(thing, *, msg=None):
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
    msg=None,
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


## this doesnt work
# def verify(thing, *, msg=None):
#    if not thing:
#        if msg:
#            if '{}' in msg:
#                msg = msg.format(thing)
#            raise ValueError(msg)
#        raise ValueError(thing)


# def nl_iff_tty(*,
#               printn: bool,
#               ipython: bool,
#               ):
#    null = not printn
#    end = b'\n'
#    if null:
#        end = b'\x00'
#    if sys.stdout.isatty():
#        end = b'\n'
#        assert not ipython
#    return end
#
#
# def _v(*,
#       ctx,
#       verbose: Union[bool, float, int],
#       verbose_inf: bool,
#       ):
#
#    ctx.ensure_object(dict)
#    if verbose_inf:
#        verbose = inf
#        return verbose
#
#    if verbose:
#        stack_depth = len(inspect.stack()) - 1
#        verbose += stack_depth
#
#    if verbose:
#        ctx.obj['verbose'] = verbose  # make sure ctx has the 'verbose' key set correctly
#    try:
#        verbose = ctx.obj['verbose']  # KeyError if verbose is False, otherwise obtain current verbose level in the ctx
#    except KeyError:
#        ctx.obj['verbose'] = verbose  # disable verbose
#
#    return verbose
#
#
# def tv(*,
#       ctx,
#       verbose: Union[bool, int, float],
#       verbose_inf: bool,
#       ) -> tuple[bool, int]:
#
#    #if sys.stdout.isatty():
#    #    assert not ipython
#    ctx.ensure_object(dict)
#    verbose = _v(ctx=ctx, verbose=verbose, verbose_inf=verbose_inf,)
#    tty = sys.stdout.isatty()
#
#    return tty, verbose
#
#
# def vd(*,
#       ctx,
#       verbose: Union[bool, float, int],
#       verbose_inf: bool,
#       debug: Union[bool, int],
#       ):
#
#    ctx.ensure_object(dict)
#    if verbose_inf:
#        verbose = inf
#        debug = True
#        return verbose, debug
#
#    if verbose:
#        stack_depth = len(inspect.stack()) - 1
#        verbose += stack_depth
#
#    if verbose:
#        ctx.obj['verbose'] = verbose  # make sure ctx has the 'verbose' key set correctly
#    try:
#        verbose = ctx.obj['verbose']  # KeyError if verbose is False, otherwise obtain current verbose level in the ctx
#    except KeyError:
#        ctx.obj['verbose'] = verbose  # disable verbose
#
#    if verbose == inf:
#        ctx.obj['debug'] = debug
#    try:
#        debug = ctx.obj['debug']
#    except KeyError:
#        ctx.obj['debug'] = debug
#
#    return verbose, debug
#
#
# def evd(*,
#        ctx,
#        printn: bool,
#        ipython: bool,
#        verbose: Union[bool, int, float],
#        verbose_inf: bool,
#        debug: Union[bool, int],
#        ):
#
#    ctx.ensure_object(dict)
#    end = nl_iff_tty(printn=printn, ipython=ipython)
#    verbose, debug = vd(ctx=ctx, verbose=verbose, verbose_inf=verbose_inf,)
#
#    return end, verbose, debug
#
#
# def nevd(*,
#         ctx,
#         printn: bool,
#         ipython: bool,
#         verbose: Union[bool, int, float],
#         verbose_inf: bool,
#         debug: Union[bool, int],
#         ):
#
#    ctx.ensure_object(dict)
#    end, verbose, debug = evd(ctx=ctx, printn=printn, ipython=ipython, verbose=verbose, verbose_inf=verbose_inf,)
#    null = not printn
#
#    return null, end, verbose, debug
#
#
# def tevd(*,
#         ctx,
#         printn: bool,
#         ipython: bool,
#         verbose: Union[bool, int, float],
#         verbose_inf: bool,
#         debug: Union[bool, int],
#         ):
#
#    ctx.ensure_object(dict)
#    end, verbose, debug = evd(ctx=ctx, printn=printn, ipython=ipython, verbose=verbose, verbose_inf=verbose_inf,)
#    #tty = True if end == b'\n' else False
#    tty = sys.stdout.isatty()
#
#    return tty, end, verbose, debug
#
#
# def tnevd(*,
#          ctx,
#          printn: bool,
#          ipython: bool,
#          verbose: Union[bool, int, float],
#          verbose_inf: bool,
#          debug: Union[bool, int],
#          ):
#
#    ctx.ensure_object(dict)
#    tty, end, verbose, debug = tevd(ctx=ctx, printn=printn, ipython=ipython, verbose=verbose, verbose_inf=verbose_inf,)
#    null = not printn
#
#    return tty, null, end, verbose, debug
