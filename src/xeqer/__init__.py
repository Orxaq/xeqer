"""Xeqer — Jacobinian logic verification engine."""

__version__ = "0.1.0"

from xeqer.ast_reader import load_spec
from xeqer.decomposer import decompose
from xeqer.proof_rules import apply_rule
from xeqer.solver import discharge
from xeqer.certificate import build_certificate

__all__ = ["load_spec", "decompose", "apply_rule", "discharge", "build_certificate", "__version__"]
