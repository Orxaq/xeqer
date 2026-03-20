"""Hoare-style proof rules for Böhm-Jacopini structures.

Each rule generates ProofObligations to be discharged by the Z3 solver.

Rules (Hoare logic):
  Sequence:  {P} S1 {Q}, {Q} S2 {R} ⊢ {P} S1;S2 {R}
  Selection: {P∧B} S1 {Q}, {P∧¬B} S2 {Q} ⊢ {P} if B then S1 else S2 {Q}
  Iteration: {I∧B} S {I} ⊢ {I} while B {I∧¬B}  (I = loop invariant)
  Atom:      {P} stmt {Q} — discharged directly by Z3
"""
from __future__ import annotations
from xeqer.structures import Sequence, Selection, Iteration, Atom, Structure
from xeqer.obligations import ProofObligation


def rule_sequence(
    seq: Sequence, precondition: str, postcondition: str
) -> list[ProofObligation]:
    """Sequence rule: generate an intermediate condition between each pair."""
    obligations = []
    current_pre = precondition
    for i, item in enumerate(seq.items):
        is_last = i == len(seq.items) - 1
        current_post = postcondition if is_last else f"_intermediate_{i}"
        obligations.extend(
            apply_rule(item, current_pre, current_post)
        )
        current_pre = current_post
    return obligations


def rule_selection(
    sel: Selection, precondition: str, postcondition: str
) -> list[ProofObligation]:
    """Selection rule: prove each branch under its respective condition."""
    obligations = []
    # Then branch: precondition AND condition
    then_pre = f"({precondition}) and ({sel.condition})"
    obligations.extend(apply_rule(sel.then_branch, then_pre, postcondition))
    # Else branch: precondition AND NOT condition
    if sel.else_branch is not None:
        else_pre = f"({precondition}) and not ({sel.condition})"
        obligations.extend(apply_rule(sel.else_branch, else_pre, postcondition))
    else:
        # No else: when condition is false, postcondition must still hold
        obligations.append(ProofObligation(
            formula=f"Implies(And({precondition}, Not({sel.condition})), {postcondition})",
            description="No-else branch: postcondition holds when condition is false",
            structure_type="selection",
        ))
    return obligations


def rule_iteration(
    it: Iteration, precondition: str, postcondition: str
) -> list[ProofObligation]:
    """Iteration rule: requires a loop invariant."""
    invariant = it.invariant or "_invariant_placeholder"
    obligations = [
        ProofObligation(
            formula=f"Implies({precondition}, {invariant})",
            description=f"Loop invariant holds initially: {invariant}",
            structure_type="iteration",
        ),
        ProofObligation(
            formula=f"Implies(And({invariant}, {it.condition}), {invariant})",
            description="Loop invariant preserved by body",
            structure_type="iteration",
        ),
        ProofObligation(
            formula=f"Implies(And({invariant}, Not({it.condition})), {postcondition})",
            description="Postcondition follows when loop exits",
            structure_type="iteration",
        ),
    ]
    return obligations


def apply_rule(
    structure: Structure, precondition: str, postcondition: str
) -> list[ProofObligation]:
    """Dispatch to the correct rule for a structure."""
    if isinstance(structure, Atom):
        return [ProofObligation(
            formula=f"Implies({precondition}, {postcondition})",
            description=f"Atom: {structure.source}",
            structure_type="atom",
            line_hint=structure.lineno,
        )]
    elif isinstance(structure, Sequence):
        return rule_sequence(structure, precondition, postcondition)
    elif isinstance(structure, Selection):
        return rule_selection(structure, precondition, postcondition)
    elif isinstance(structure, Iteration):
        return rule_iteration(structure, precondition, postcondition)
    else:
        raise TypeError(f"Unknown structure type: {type(structure)}")
