"""Utilities to use in atypes functionality"""

from typing import Optional, Iterable, TypeVar, Union, NewType


def MyType(
    name: str,
    tp,
    doc: Optional[str] = None,
    aka: Optional[Union[str, Iterable[str]]] = None,
    *,
    assign_to_globals=False
):
    """
    Make a new type with (optional) doc and (optional) aka, set of var names it often appears as

    Args:
        name: Name to give the variable
        constraints: types (see typing.TypeVar)
        doc: Optional string to put in __doc__ attribute
        aka: Optional set (or any iterable) to put in _aka attribute,
            meant to list names the variables of this type often appear as.

    Returns: None

    >>> from typing import Any, List
    >>> T = MyType('T', int)
    >>> type(T)
    <class 'function'>
    >>> Key = MyType('Key', Any, aka=['key', 'k'])
    >>> type(Key._aka)
    <class 'set'>
    >>> sorted(Key._aka)
    ['k', 'key']
    >>> Val = MyType('Val', Union[int, float, List[Union[int, float]]], doc="A number or list of numbers.")
    >>> Val.__doc__
    'A number or list of numbers.'
    """

    new_tp = NewType(name, tp)

    if doc is not None:
        try:
            setattr(new_tp, '__doc__', doc)
        except AttributeError:  # because TypeVar attributes are read only in 3.6, it seems...
            pass
    if aka is not None:
        if isinstance(aka, str):
            aka = [aka]
        try:
            setattr(new_tp, '_aka', set(aka))
        except AttributeError:  # because TypeVar attributes are read only in 3.6, it seems...
            pass
    if assign_to_globals:
        globals()[
            name
        ] = new_tp  # not sure how kosher this is... Should only use at top level of module, for sure!
    return new_tp


def MyVar(
    name: str,
    constraint,
    *more_constraints,
    doc: Optional[str] = None,
    aka: Optional[Union[str, Iterable[str]]] = None,
    covariant=False,
    contravariant=False,
    assign_to_globals=False
):
    """
    TODO: Add docstring and doctests
    """
    if len(more_constraints) == 0:
        new_tp = TypeVar(
            name, bound=constraint, covariant=covariant, contravariant=contravariant
        )
    else:
        new_tp = TypeVar(
            name,
            constraint,
            *more_constraints,
            covariant=covariant,
            contravariant=contravariant
        )
    if doc is not None:
        try:
            setattr(new_tp, '__doc__', doc)
        except AttributeError:  # because TypeVar attributes are read only in 3.6, it seems...
            pass
    if aka is not None:
        if isinstance(aka, str):
            aka = [aka]
        try:
            setattr(new_tp, '_aka', set(aka))
        except AttributeError:  # because TypeVar attributes are read only in 3.6, it seems...
            pass
    if assign_to_globals:
        globals()[
            name
        ] = new_tp  # not sure how kosher this is... Should only use at top level of module, for sure!
    return new_tp
