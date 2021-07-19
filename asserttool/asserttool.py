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

import os
import sys

import click


def eprint(*args, **kwargs):
    if 'file' in kwargs.keys():
        kwargs.pop('file')
    print(*args, file=sys.stderr, **kwargs)


try:
    from icecream import ic  # https://github.com/gruns/icecream
    from icecream import icr  # https://github.com/jakeogh/icecream
except ImportError:
    ic = eprint
    icr = eprint


def validate_slice(slice_syntax):
    assert isinstance(slice_syntax, str)
    for c in slice_syntax:
        if c not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '[', ']', ':']:
            raise ValueError(slice_syntax)
    return slice_syntax


def click_validate_slice(ctx, param, value):
    #ic(param, value)
    if value is not None:
        validate_slice(value)
        return value


def embed_ipdb():
    import ipdb
    ipdb.set_trace()


def pause(message='', ipython=False):
    assert isinstance(message, str)
    if ipython:
        message += " (type 'ipython' to enter shell or 'ipdb' to enter debugger): "
    response = input(message)
    if response == "ipdb":
        embed_ipdb()
        pause("press enter to continue execution")
    elif response == "ipython":
        from IPython import embed; embed()
        pause("press enter to continue execution")


def root_user():
    if os.getuid() == 0:
        return True
    return False


def not_root():
    if root_user():
        ic('Dont run this as root!')
        sys.exit(1)
        #raise ValueError('Dont run this as root!')


#def am_root():
#    if not root_user():
#        ic('You must run this as root!')
#        sys.exit(1)
#        #raise ValueError('Dont run this as root!')

def one(thing, *, msg=None):
    count = 0
    for x in thing:
        #eprint("x:", x, bool(x))
        if bool(x):
            count += 1
    #count = sum(1 for x in thing if bool(x))
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


def minone(thing,
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


def verify(thing):
    if not thing:
        raise ValueError(thing)

#def verify(thing, *, msg=None):
#    if not thing:
#        if msg:
#            if '{}' in msg:
#                msg = msg.format(thing)
#            raise ValueError(msg)
#        raise ValueError(thing)


def nl_iff_tty(*,
               printn: bool,
               ipython: bool,
               ):
    null = not printn
    end = b'\n'
    if null:
        end = b'\x00'
    if sys.stdout.isatty():
        end = b'\n'
        assert not ipython
    return end


def nevd(*,
         ctx,
         printn: bool,
         ipython: bool,
         verbose: bool,
         debug: bool,
         ):

    ctx.ensure_object(dict)
    null = not printn
    end = nl_iff_tty(printn=printn, ipython=False)
    if verbose:
        ctx.obj['verbose'] = verbose
    try:
        verbose = ctx.obj['verbose']
    except KeyError:
        ctx.obj['verbose'] = verbose

    if debug:
        ctx.obj['debug'] = debug
    try:
        debug = ctx.obj['debug']
    except KeyError:
        ctx.obj['debug'] = debug

    return null, end, verbose, debug


@click.command()
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.pass_context
def cli(ctx,
        verbose: bool,
        debug: bool,
        ):

    minone([True, False])
    maxone([True, False, False])
    verify(True)

