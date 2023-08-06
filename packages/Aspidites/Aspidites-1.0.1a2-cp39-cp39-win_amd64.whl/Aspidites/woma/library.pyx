#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, binding=True
# THIS FILE IS GENERATED - DO NOT EDIT #

from typing import Any
from collections.abc import Generator
import cython  # type: ignore
from pyrsistent import (
    pset, 
    pmap, 
    pvector, 
    s, v, m, 
    PRecord,
    PClass
)
from Aspidites.woma import *
from Aspidites._vendor import (
    reduce,
    filterfalse,
    zip_longest,
    accumulate,
    take,
    drop,
    takelast,
    droplast,
    match,
    _,
    InstanceOf,
)
from Aspidites.monads import Maybe, Surely
from Aspidites.math import Undefined, SafeDiv, SafeExp, SafeMod, SafeFloorDiv, SafeUnaryAdd, SafeUnarySub, SafeFactorial
from Aspidites._vendor.contracts import contract, new_contract
from Aspidites._vendor.RestrictedPython import safe_builtins
safe_builtins['print'] = print
from Aspidites._vendor.RestrictedPython import compile_restricted as compile
safe_builtins['compile'] = compile
# DECLARATIONS TO ALLOW CONTRACTS TO TYPE CHECK #
procedure: None
coroutine: Generator
number: Any
globals().update(dict(__builtins__=safe_builtins))  # add all imports to globals


@contract()
@cython.binding(True)
def Add(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return x+y
    
@contract()
@cython.binding(True)
def Sub(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return x-y
    
@contract()
@cython.binding(True)
def Div(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return Maybe(SafeDiv, x, y)()
    
@contract()
@cython.binding(True)
def Exp(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return Maybe(SafeExp, x, y)()
    
@contract()
@cython.binding(True)
def Mod(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return Maybe(SafeMod, x, y)()






