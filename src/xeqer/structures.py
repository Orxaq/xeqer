"""Böhm-Jacopini program structures: the three universal control forms."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union


@dataclass
class Atom:
    """A single statement with no branches or loops."""
    source: str          # the Python statement as text
    lineno: int


@dataclass
class Sequence:
    """One or more structures executed in order."""
    items: list[Structure]


@dataclass
class Selection:
    """An if/elif/else branching structure."""
    condition: str
    then_branch: Structure
    else_branch: Structure | None


@dataclass
class Iteration:
    """A while or for loop."""
    condition: str       # loop condition or 'for <target> in <iter>'
    body: Structure
    invariant: str | None = None   # loop invariant annotation (if provided)


Structure = Union[Atom, Sequence, Selection, Iteration]


@dataclass
class StructuredProgram:
    """The Böhm-Jacopini decomposition of a Python function."""
    function_name: str
    params: list[str]
    body: Structure
    is_structured: bool = True      # False if unstructured constructs found
    unstructured_reasons: list[str] = field(default_factory=list)
