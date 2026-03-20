"""Z3 SMT solver integration — discharge ProofObligations."""
from __future__ import annotations
from dataclasses import dataclass
from xeqer.obligations import ProofObligation

try:
    import z3
    _Z3_AVAILABLE = True
except ImportError:
    _Z3_AVAILABLE = False


@dataclass
class SolverResult:
    proved: bool
    counterexample: str | None = None
    error: str | None = None


def discharge(obligation: ProofObligation) -> SolverResult:
    """Attempt to prove an obligation using Z3.

    The obligation.formula must be a valid Python expression using Z3 APIs.
    Variables named in obligation.variables are pre-declared as z3.Real().
    """
    if not _Z3_AVAILABLE:
        return SolverResult(proved=False, error="z3-solver not installed")

    try:
        context: dict = {}
        exec("from z3 import *", context)
        # Pre-declare all required variables as z3.Real
        for var in obligation.variables:
            context[var] = z3.Real(var)

        formula = eval(obligation.formula, context)
        solver = z3.Solver()
        # To prove F, check if NOT F is unsatisfiable
        solver.add(z3.Not(formula))
        result = solver.check()

        if result == z3.unsat:
            return SolverResult(proved=True)
        elif result == z3.sat:
            model = solver.model()
            return SolverResult(proved=False, counterexample=str(model))
        else:
            return SolverResult(proved=False, error="Z3 returned unknown")
    except Exception as e:
        return SolverResult(proved=False, error=str(e))
