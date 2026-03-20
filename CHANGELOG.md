# Changelog

All notable changes to Xeqer are documented here.
Format: [version] YYYY-MM-DD — description. Refs: SR11-7(2011)-§ or N/A.

## [0.1.0] 2026-03-19
Req: SR11-7(2011)-§model-development

Initial release. Xeqer Jacobinian logic verification engine v0.1.0.

### Added
- AST reader: load Speqr JSON AST into internal SpecModel
- Decomposer: Python source → Böhm-Jacopini structures (sequence/selection/iteration)
- Structures: Atom, Sequence, Selection, Iteration, StructuredProgram dataclasses
- Proof rules: Hoare-style rules for sequence, selection, iteration
- Proof obligations: ProofObligation dataclass with Z3 formula representation
- Z3 solver integration: discharge obligations with counterexample on failure
- Proof certificate: SHA-256 content-hashed JSON certificate (PROVEN/FAILED/UNVERIFIABLE)
- CLI: `xeqer verify <spec.json> <impl.py>` with optional `--output` certificate

### Excludes (future releases)
- Incremental verification
- Parallel verification
- Caching
- Recursion with termination metrics
