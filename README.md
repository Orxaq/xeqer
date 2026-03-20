# Xeqer  /ˈzeː.kər/

> How you prove your code actually does it.

Xeqer is a verification engine that proves Python implementations satisfy
[Speqr](https://github.com/Orxaq/speqr) specifications using Jacobinian logic —
structured program decomposition (Böhm-Jacopini) combined with Hoare-style proof
rules and Z3-discharged proof obligations.

## Install

```bash
pip install xeqer
```

## Quick Start

```bash
# Given a Speqr JSON AST and a Python implementation:
xeqer verify divide.speqr.json divide.py

# Output a signed proof certificate:
xeqer verify divide.speqr.json divide.py --output cert.json
```

## How It Works

1. **Decompose** — Parse the Python function into sequence/selection/iteration
   structures (Böhm-Jacopini theorem)
2. **Generate** — Apply Hoare-style proof rules to generate proof obligations
3. **Discharge** — Use Z3 (SMT solver) to prove or refute each obligation
4. **Certify** — Produce a SHA-256 content-hashed proof certificate
