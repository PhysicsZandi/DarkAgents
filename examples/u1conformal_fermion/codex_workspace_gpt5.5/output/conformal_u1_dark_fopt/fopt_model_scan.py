"""Bounded FOPT scan for conformal_u1_dark_fopt."""

from __future__ import annotations

import csv
import json
import math
import signal
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from fopt_model import PTA_F_MAX_HZ, PTA_F_MIN_HZ, evaluate_point

MODEL = "conformal_u1_dark_fopt"
BRANCH = "fopt-pta"
OUTDIR = Path(__file__).resolve().parent
CSV_PATH = OUTDIR / "fopt_benchmarks.csv"
RESULTS_PATH = OUTDIR / "fopt_results.json"
HANDOFF_PATH = OUTDIR / "handoff_fopt.json"
REPORT_PATH = OUTDIR / "fopt_report.md"

FIELDNAMES = [
    "name",
    "v_D",
    "g_D",
    "y_D",
    "gb_X",
    "gf_psi",
    "beta_lambda",
    "m_X_GeV",
    "m_psi_GeV",
    "m_chi_GeV",
    "Tn",
    "Tp",
    "Treh",
    "alpha",
    "beta_H",
    "f_peak_est",
    "gstar_Treh",
    "eternal_inflation",
    "status",
    "failure_reason",
    "scan_stage",
]


class TimeoutError(Exception):
    pass


def _timeout_handler(signum: int, frame: Any) -> None:
    raise TimeoutError("point_timeout")


def safe_evaluate(v_D: float, g_D: float, y_D: float, timeout_s: int = 12) -> dict[str, Any]:
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_s)
    try:
        row = evaluate_point(v_D, g_D, y_D)
    except TimeoutError:
        row = {"v_D": v_D, "g_D": g_D, "y_D": y_D, "status": "numerical_failure", "failure_reason": "point_timeout"}
    except Exception as exc:
        row = {"v_D": v_D, "g_D": g_D, "y_D": y_D, "status": "numerical_failure", "failure_reason": type(exc).__name__}
    finally:
        signal.alarm(0)
    return row


def point_grid(stage: str) -> Iterable[tuple[str, float, float, float]]:
    if stage == "seeded":
        seeds = [
            ("borah_low_scale", 0.0196875, 0.32, 0.02),
            ("balan_point_A_mapped", 0.173, 0.34, 0.224),
            ("balan_point_B_mapped", 0.692, 0.30, 0.234),
            ("goncalves_scale_hint", 0.18, 0.59, 0.25),
        ]
        for item in seeds:
            yield item
        return

    if stage == "coarse":
        v_vals = [0.02, 0.05, 0.10, 0.173, 0.30, 0.50, 0.70]
        g_vals = [0.30, 0.36, 0.44, 0.55, 0.70]
        y_vals = [0.00, 0.10, 0.20, 0.30, 0.40]
    elif stage == "extended_low":
        v_vals = np.geomspace(0.002, 0.80, 8)
        g_vals = [0.22, 0.30, 0.38, 0.50, 0.65, 0.80]
        y_vals = [0.00, 0.05, 0.15, 0.25, 0.35, 0.50]
    elif stage == "extended_broad":
        v_vals = np.geomspace(0.001, 7.0, 9)
        g_vals = [0.15, 0.25, 0.35, 0.50, 0.75, 1.00]
        y_vals = [0.00, 0.10, 0.25, 0.40, 0.65, 0.90]
    else:
        raise ValueError(stage)

    for v_D in v_vals:
        for g_D in g_vals:
            for y_D in y_vals:
                yield (f"{stage}_v{v_D:.4g}_g{g_D:.3g}_y{y_D:.3g}", float(v_D), float(g_D), float(y_D))


def dedupe(points: Iterable[tuple[str, float, float, float]]) -> list[tuple[str, float, float, float]]:
    seen = set()
    unique = []
    for name, v_D, g_D, y_D in points:
        key = (round(v_D, 12), round(g_D, 12), round(y_D, 12))
        if key not in seen:
            seen.add(key)
            unique.append((name, v_D, g_D, y_D))
    return unique


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def benchmark_item(row: dict[str, Any]) -> dict[str, Any]:
    status = "viable" if row.get("status") == "viable" else "failed"
    return {
        "name": row["name"],
        "parameters": {
            "v_D": row.get("v_D"),
            "g_D": row.get("g_D"),
            "y_D": row.get("y_D"),
            "gb_X": row.get("gb_X"),
            "gf_psi": row.get("gf_psi"),
            "beta_lambda": row.get("beta_lambda"),
        },
        "alpha": finite_float(row.get("alpha")),
        "beta_H": finite_float(row.get("beta_H")),
        "Tn": finite_float(row.get("Tn")),
        "Tp": finite_float(row.get("Tp")),
        "Treh": finite_float(row.get("Treh")),
        "f_peak_est": finite_float(row.get("f_peak_est")),
        "_comment_f_peak_est": "template-independent, order-of-magnitude redshifted peak frequency in Hz; anchors the vev/temperature scale for the PTA agent and must not be treated as the true spectral peak",
        "status": status,
        "failure_reason": row.get("failure_reason", ""),
    }


def write_outputs(rows: list[dict[str, Any]]) -> None:
    with CSV_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDNAMES})

    viable = [row for row in rows if row.get("status") == "viable"]
    pta_viable = [
        row
        for row in viable
        if (finite_float(row.get("f_peak_est")) is not None and PTA_F_MIN_HZ <= float(row["f_peak_est"]) <= PTA_F_MAX_HZ)
    ]
    best_source = pta_viable if pta_viable else viable
    best_rows = sorted(best_source, key=lambda r: abs(math.log10(float(r["f_peak_est"]) / 1.0e-8)) if finite_float(r.get("f_peak_est")) else 99.0)[:12]

    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row.get("status", "unknown")] = status_counts.get(row.get("status", "unknown"), 0) + 1

    warnings = []
    if not viable:
        warnings.append("No viable finite non-eternal FOPT point was found after seeded, coarse, and one-order extended scans.")
    elif not pta_viable:
        warnings.append("Viable FOPT points were found, but none had f_peak_est inside 1e-9--1e-7 Hz.")

    handoff = {
        "model": MODEL,
        "agent": "fopt-agent",
        "run_status": "ok" if viable else "warning",
        "created_at": str(date.today()),
        "branch": BRANCH,
        "created_from": [
            "output/conformal_u1_dark_fopt/handoff_model.json",
            "output/conformal_u1_dark_fopt/handoff_librarian_preliminary.json",
            "output/conformal_u1_dark_fopt/handoff_critique.json",
            "output/conformal_u1_dark_fopt/field_dependent_mass_recheck.md",
        ],
        "commands": [
            "conda run -n ptarcade python output/conformal_u1_dark_fopt/fopt_model.py",
            "conda run -n ptarcade python output/conformal_u1_dark_fopt/fopt_model_scan.py",
        ],
        "files_read": [
            ".codex/agents/fopt-agent.md",
            ".codex/skills/fopt-implementation/SKILL.md",
            "docs/HANDOFF_FOPT_SCHEMA.md",
            "docs/BACKEND_COMPATIBILITY.md",
            "docs/SEMIANALYTICPIPELINE.md",
            "backend/semianalytic_pipeline.py",
            "backend/T_vs_g_gs_GeV.csv",
            "output/conformal_u1_dark_fopt/handoff_model.json",
            "output/conformal_u1_dark_fopt/handoff_librarian_preliminary.json",
            "output/conformal_u1_dark_fopt/handoff_critique.json",
            "output/conformal_u1_dark_fopt/field_dependent_mass_recheck.md",
        ],
        "files_written": [
            "output/conformal_u1_dark_fopt/fopt_model.py",
            "output/conformal_u1_dark_fopt/fopt_model_scan.py",
            "output/conformal_u1_dark_fopt/fopt_benchmarks.csv",
            "output/conformal_u1_dark_fopt/fopt_report.md",
            "output/conformal_u1_dark_fopt/handoff_fopt.json",
            "output/conformal_u1_dark_fopt/fopt_results.json",
        ],
        "warnings": warnings,
        "errors": [],
        "approximations": [
            "Semianalytic conformal single-field backend with small-field/high-temperature polynomial potential.",
            "Gaussian false-vacuum-fraction/percolation approximation from backend.",
            "No RG running, portal coupling, kinetic mixing, or Daisy-resummed explicit thermal masses are included.",
            "f_peak_est is a template-independent order-of-magnitude scale guide only.",
        ],
        "backend_choice": {
            "selected_backend": "semianalytic_pipeline",
            "executed": True,
            "reason": "Validated conformal single-field model with all backend masses proportional to v_D.",
        },
        "backend": "semianalytic_pipeline",
        "backend_executed": True,
        "expected_upstream_inputs": [
            "output/conformal_u1_dark_fopt/handoff_model.json",
            "output/conformal_u1_dark_fopt/handoff_librarian_preliminary.json",
            "output/conformal_u1_dark_fopt/handoff_critique.json",
            "output/conformal_u1_dark_fopt/field_dependent_mass_recheck.md",
        ],
        "missing_upstream_inputs": [],
        "model_parameter_ranges": {
            "v_D": {"unit": "GeV", "scanned_min": min(r["v_D"] for r in rows), "scanned_max": max(r["v_D"] for r in rows)},
            "g_D": {"unit": "dimensionless", "scanned_min": min(r["g_D"] for r in rows), "scanned_max": max(r["g_D"] for r in rows)},
            "y_D": {"unit": "dimensionless", "scanned_min": min(r["y_D"] for r in rows), "scanned_max": max(r["y_D"] for r in rows)},
        },
        "parameter_basis": {
            "independent": {
                "v_D": {"unit": "GeV", "description": "Dark radial vev"},
                "g_D": {"unit": "dimensionless", "description": "Dark U(1)_D gauge coupling"},
                "y_D": {"unit": "dimensionless", "description": "Dark Yukawa coupling"},
            },
            "dependent": {
                "gb_X": "2*g_D",
                "gf_psi": "y_D/sqrt(2)",
                "beta_lambda": "(1/(8*pi**2))*(3*gb_X**4 - 4*gf_psi**4)",
                "lambda_D": "Coleman-Weinberg dependent; not scanned",
            },
            "fixed": {"lambda_HP": 0, "epsilon": 0, "boson_dof_X_mu": 3, "fermion_dof_psi_degenerate_majorana_pair": 4},
        },
        "temperature_key": "Treh",
        "scan_status_labels": ["viable", "physical_failure", "numerical_failure", "not_fopt"],
        "benchmark_summary": {
            "total_points": len(rows),
            "viable_points": len(viable),
            "failed_points": len([r for r in rows if r.get("status") == "numerical_failure"]),
            "excluded_points": len([r for r in rows if r.get("status") in ("physical_failure", "not_fopt")]),
        },
        "scan_summary": {
            "total_points": len(rows),
            "viable_points": len(viable),
            "failed_points": len([r for r in rows if r.get("status") == "numerical_failure"]),
            "excluded_points": len([r for r in rows if r.get("status") in ("physical_failure", "not_fopt")]),
            "pta_band_viable_points": len(pta_viable),
            "status_counts": status_counts,
        },
        "csv_json_alignment": {
            "csv_file": "output/conformal_u1_dark_fopt/fopt_benchmarks.csv",
            "independent_parameter_columns": ["v_D", "g_D", "y_D"],
            "required_result_columns": ["alpha", "beta_H", "Tn", "Tp", "Treh", "f_peak_est", "status"],
            "status_column": "status",
        },
        "model_parameters": ["v_D", "g_D", "y_D"],
        "benchmarks": [benchmark_item(row) for row in best_rows],
        "best_points": [benchmark_item(row) for row in best_rows if row.get("status") == "viable"],
        "prior_ranges": {
            "v_D": {"unit": "GeV", "min": min(r["v_D"] for r in rows), "max": max(r["v_D"] for r in rows)},
            "g_D": {"unit": "dimensionless", "min": min(r["g_D"] for r in rows), "max": max(r["g_D"] for r in rows)},
            "y_D": {"unit": "dimensionless", "min": min(r["y_D"] for r in rows), "max": max(r["y_D"] for r in rows)},
        },
        "validation": {
            "finite_values": bool(viable),
            "percolation_checked": True,
            "eternal_inflation_checked": True,
            "perturbativity_checked": True,
        },
        "output_files": [
            "output/conformal_u1_dark_fopt/fopt_model.py",
            "output/conformal_u1_dark_fopt/fopt_model_scan.py",
            "output/conformal_u1_dark_fopt/fopt_benchmarks.csv",
            "output/conformal_u1_dark_fopt/fopt_report.md",
            "output/conformal_u1_dark_fopt/handoff_fopt.json",
            "output/conformal_u1_dark_fopt/fopt_results.json",
        ],
    }

    RESULTS_PATH.write_text(json.dumps(handoff, indent=2) + "\n")
    HANDOFF_PATH.write_text(json.dumps(handoff, indent=2) + "\n")

    best_lines = []
    for row in best_rows[:8]:
        best_lines.append(
            f"| {row['name']} | {row['v_D']:.6g} | {row['g_D']:.4g} | {row['y_D']:.4g} | "
            f"{row.get('Treh', math.nan):.6g} | {row.get('alpha', math.nan):.6g} | "
            f"{row.get('beta_H', math.nan):.6g} | {row.get('f_peak_est', math.nan):.6g} | {row['status']} |"
        )
    report = [
        "# FOPT Report: conformal_u1_dark_fopt",
        "",
        "Backend: `semianalytic_pipeline`.",
        "",
        f"Total scan points: {len(rows)}.",
        f"Viable FOPT points: {len(viable)}.",
        f"Viable points with `f_peak_est` in 1e-9--1e-7 Hz: {len(pta_viable)}.",
        f"Status counts: {status_counts}.",
        "",
        "Independent scan axes are `v_D` [GeV], `g_D`, and `y_D`. Dependent quantities use `gb_X=2*g_D`, `gf_psi=y_D/sqrt(2)`, and `beta_lambda=(3*gb_X**4 - 4*gf_psi**4)/(8*pi**2)`. `lambda_D` was not scanned.",
        "",
        "## Best Points",
        "",
        "| name | v_D [GeV] | g_D | y_D | Treh [GeV] | alpha | beta/H | f_peak_est [Hz] | status |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        *best_lines,
        "",
        "## Diagnostics",
        "",
        "The scan used seeded literature-mapped points, a MeV/sub-GeV coarse grid, and one-order extended low/broad ranges. Points with nonpositive beta_lambda, nonpositive temperatures/alpha/beta_H, nonfinite backend outputs, timeouts, or eternal inflation were not marked viable.",
    ]
    if warnings:
        report.extend(["", "## Warnings", "", *[f"- {warning}" for warning in warnings]])
    REPORT_PATH.write_text("\n".join(report) + "\n")


def main() -> None:
    stages = ["seeded", "coarse", "extended_low", "extended_broad"]
    points = dedupe(item for stage in stages for item in point_grid(stage))
    rows = []
    for idx, (name, v_D, g_D, y_D) in enumerate(points, start=1):
        row = safe_evaluate(v_D, g_D, y_D)
        row["name"] = name
        row["scan_stage"] = name.split("_", 1)[0]
        rows.append(row)
        if idx % 50 == 0:
            print(f"evaluated {idx}/{len(points)} points")
    write_outputs(rows)
    print(f"wrote {CSV_PATH}")
    print(f"wrote {HANDOFF_PATH}")


if __name__ == "__main__":
    main()
