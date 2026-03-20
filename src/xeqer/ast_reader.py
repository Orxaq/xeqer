"""Load a Speqr JSON AST into Xeqer's internal SpecModel."""
from __future__ import annotations
import json
from dataclasses import dataclass


@dataclass
class VarDecl:
    name: str
    vtype: str   # e.g. "Real"
    sumo: str    # e.g. "RealNumber"


@dataclass
class SpecModel:
    """Xeqer's internal representation of a Speqr spec."""
    name: str
    inputs: list[VarDecl]
    outputs: list[VarDecl]
    preconditions: list[str]   # raw expression strings
    postconditions: list[str]
    causal_assertions: list[dict]


def load_spec(json_text: str) -> SpecModel:
    """Parse a Speqr JSON AST string into a SpecModel."""
    d = json.loads(json_text)
    return SpecModel(
        name=d["name"],
        inputs=[VarDecl(**v) for v in d["inputs"]],
        outputs=[VarDecl(**v) for v in d["outputs"]],
        preconditions=[p["expression"] for p in d["preconditions"]],
        postconditions=[p["expression"] for p in d["postconditions"]],
        causal_assertions=d["causal_assertions"],
    )
