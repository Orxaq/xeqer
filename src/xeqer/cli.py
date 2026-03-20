"""Xeqer CLI — `xeqer verify`."""
from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Optional
import typer
from xeqer.ast_reader import load_spec
from xeqer.decomposer import decompose
from xeqer.proof_rules import apply_rule
from xeqer.solver import discharge
from xeqer.certificate import build_certificate

app = typer.Typer(help="Xeqer — Jacobinian logic verification engine")


@app.command("verify")
def verify(
    spec_file: Path = typer.Argument(..., help="Path to Speqr JSON AST"),
    impl_file: Path = typer.Argument(..., help="Path to Python implementation"),
    output: Optional[Path] = typer.Option(None, help="Write proof certificate to file"),
    function_name: Optional[str] = typer.Option(None, "--function-name", help="Python function name to verify (default: lowercase spec name)"),
) -> None:
    """Verify a Python implementation against a Speqr specification."""
    for f in (spec_file, impl_file):
        if not f.exists():
            typer.echo(f"File not found: {f}", err=True)
            raise typer.Exit(1)

    spec_text = spec_file.read_text()
    impl_text = impl_file.read_text()

    spec = load_spec(spec_text)
    prog = decompose(impl_text, function_name=function_name or spec.name.lower())

    if not prog.is_structured:
        typer.echo(f"UNVERIFIABLE: {'; '.join(prog.unstructured_reasons)}")
        raise typer.Exit(2)

    # Build precondition/postcondition from spec
    precondition = " and ".join(spec.preconditions) or "True"
    postcondition = " and ".join(spec.postconditions) or "True"

    obligations = apply_rule(prog.body, precondition, postcondition)
    results = [(ob, discharge(ob)) for ob in obligations]

    cert = build_certificate(
        spec_name=spec.name,
        spec_hash=hashlib.sha256(spec_text.encode()).hexdigest()[:16],
        impl_hash=hashlib.sha256(impl_text.encode()).hexdigest()[:16],
        results=results,
    )

    cert_json = cert.to_json()

    if output:
        output.write_text(cert_json)
        typer.echo(f"Certificate written to {output}")

    status_symbol = "✓" if cert.status == "PROVEN" else "✗"
    typer.echo(f"{status_symbol} {cert.status}: {spec.name}")

    if cert.status == "FAILED":
        for ob, r in results:
            if not r.proved:
                typer.echo(f"  ✗ {ob.description}")
                if r.counterexample:
                    typer.echo(f"    Counterexample: {r.counterexample}")
        raise typer.Exit(1)
