"""Scan gD and vD for minimal_conformal_su2_doublet FOPT benchmarks."""

from __future__ import annotations

import csv
import json
import math
import signal
from datetime import date
from pathlib import Path

import numpy as np

from fopt_model import MAX_PERTURBATIVE_GD, PTA_F_MAX_HZ, PTA_F_MIN_HZ, evaluate_point


MODEL = "minimal_conformal_su2_doublet"
MODEL_DIR = Path(__file__).resolve().parent
PROJECT_DIR = MODEL_DIR.parents[1]
CSV_PATH = MODEL_DIR / "fopt_benchmarks.csv"
RESULTS_PATH = MODEL_DIR / "fopt_results.json"
HANDOFF_PATH = MODEL_DIR / "handoff_fopt.json"
REPORT_PATH = MODEL_DIR / "fopt_report.md"

SCAN_STATUS_LABELS = ["viable", "physical_failure", "numerical_failure", "not_fopt"]
REQUIRED_RESULT_COLUMNS = [
    "m_WD",
    "gb_WD",
    "beta_lambda",
    "m_chi",
    "Tn",
    "Tp",
    "Treh",
    "alpha",
    "beta_H",
    "gstar_eff",
    "f_peak_est",
    "eternal_inflation",
    "in_pta_band_est",
    "status",
    "failure_reason",
]
CSV_COLUMNS = ["name", "gD", "vD"] + REQUIRED_RESULT_COLUMNS


class PointTimeout(Exception):
    pass


def _timeout_handler(_signum, _frame):
    raise PointTimeout("per-point timeout")


def evaluate_with_timeout(gD: float, vD: float, timeout_s: int = 25) -> dict:
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_s)
    try:
        return evaluate_point(gD, vD)
    except PointTimeout as exc:
        return _failed_row(gD, vD, "numerical_failure", str(exc))
    except Exception as exc:
        return _failed_row(gD, vD, "numerical_failure", f"{type(exc).__name__}: {exc}")
    finally:
        signal.alarm(0)


def _failed_row(gD: float, vD: float, status: str, reason: str) -> dict:
    row = {column: None for column in CSV_COLUMNS}
    row.update(
        {
            "gD": float(gD),
            "vD": float(vD),
            "status": status,
            "failure_reason": reason,
            "eternal_inflation": None,
            "in_pta_band_est": False,
        }
    )
    return row


def unique_points(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    seen = set()
    unique = []
    for gD, vD in points:
        if not (0.0 < gD < MAX_PERTURBATIVE_GD and vD > 0.0):
            continue
        key = (round(float(gD), 12), round(float(vD), 12))
        if key not in seen:
            seen.add(key)
            unique.append((float(gD), float(vD)))
    return unique


def build_scan_points() -> list[tuple[float, float]]:
    g_anchor = 1.37
    m_zd_anchor_gev = 8.23e-3
    v_anchor = 2.0 * m_zd_anchor_gev / g_anchor

    points: list[tuple[float, float]] = []

    # Coarse anchor-centered grid.
    for gD in np.linspace(0.45, 2.45, 17):
        for vD in np.geomspace(v_anchor / 30.0, v_anchor * 30.0, 17):
            points.append((gD, vD))

    # Wider lower/higher scale expansion for PTA steering.
    for gD in np.linspace(0.25, 3.2, 16):
        for vD in np.geomspace(1.0e-5, 0.8, 18):
            points.append((gD, vD))

    # Fine pass around the same-model literature anchor.
    for gD in np.linspace(0.9, 1.8, 19):
        for vD in np.geomspace(v_anchor / 5.0, v_anchor * 5.0, 19):
            points.append((gD, vD))

    return unique_points(points)


def finite_float(value) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def point_score(row: dict) -> float:
    f_peak = row.get("f_peak_est")
    alpha = row.get("alpha")
    beta_H = row.get("beta_H")
    if not (finite_float(f_peak) and finite_float(alpha) and finite_float(beta_H)):
        return float("inf")
    target = math.sqrt(PTA_F_MIN_HZ * PTA_F_MAX_HZ)
    frequency_penalty = abs(math.log10(float(f_peak) / target))
    beta_penalty = max(0.0, math.log10(float(beta_H) / 1000.0)) if float(beta_H) > 0 else 99.0
    strength_penalty = max(0.0, -math.log10(float(alpha))) if float(alpha) > 0 else 99.0
    return frequency_penalty + 0.2 * beta_penalty + 0.1 * strength_penalty


def benchmark_item(row: dict, index: int) -> dict:
    json_status = "viable" if row["status"] == "viable" else "failed"
    return {
        "name": row.get("name") or f"point_{index:04d}",
        "parameters": {"gD": row["gD"], "vD": row["vD"]},
        "alpha": row.get("alpha"),
        "beta_H": row.get("beta_H"),
        "Tn": row.get("Tn"),
        "Tp": row.get("Tp"),
        "Treh": row.get("Treh"),
        "f_peak_est": row.get("f_peak_est"),
        "_comment_f_peak_est": "template-independent, order-of-magnitude redshifted peak frequency in Hz; anchors the vev/temperature scale for the PTA agent and must not be treated as the true spectral peak",
        "status": json_status,
        "failure_reason": row.get("failure_reason") or "",
    }


def write_csv(rows: list[dict]) -> None:
    with CSV_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column) for column in CSV_COLUMNS})


def write_outputs(rows: list[dict]) -> None:
    viable = [row for row in rows if row["status"] == "viable"]
    viable_sorted = sorted(viable, key=point_score)
    best_rows = viable_sorted[:10]
    failed_points = len([row for row in rows if row["status"] == "numerical_failure"])
    excluded_points = len(rows) - len(viable) - failed_points
    warnings = [
        "f_peak_est is a template-independent order-of-magnitude estimate for PTA-band steering only.",
        "The semianalytic backend uses its high-temperature polynomial approximation and Gaussian percolation approximation.",
        "The exact core model has same-model literature precedent; this scan recomputes observables locally with the critic-authoritative vector mass convention.",
    ]
    if not any(row.get("in_pta_band_est") for row in viable):
        warnings.append("No viable evaluated point had f_peak_est inside 1e-9-1e-7 Hz.")

    commands = [
        "MPLCONFIGDIR=output/minimal_conformal_su2_doublet/.mplconfig conda run -n ptarcade python output/minimal_conformal_su2_doublet/fopt_model.py",
        "MPLCONFIGDIR=output/minimal_conformal_su2_doublet/.mplconfig conda run -n ptarcade python output/minimal_conformal_su2_doublet/fopt_model_scan.py",
    ]
    files_written = [
        "output/minimal_conformal_su2_doublet/fopt_model.py",
        "output/minimal_conformal_su2_doublet/fopt_model_scan.py",
        "output/minimal_conformal_su2_doublet/fopt_benchmarks.csv",
        "output/minimal_conformal_su2_doublet/fopt_results.json",
        "output/minimal_conformal_su2_doublet/handoff_fopt.json",
        "output/minimal_conformal_su2_doublet/fopt_report.md",
    ]
    handoff = {
        "model": MODEL,
        "agent": "fopt-agent",
        "run_status": "ok" if viable else "warning",
        "created_at": date.today().isoformat(),
        "branch": "fopt-pta",
        "created_from": [
            "output/minimal_conformal_su2_doublet/handoff_model.json",
            "output/minimal_conformal_su2_doublet/handoff_critique.json",
            "output/minimal_conformal_su2_doublet/handoff_librarian_preliminary.json",
            "docs/BACKEND_COMPATIBILITY.md",
            "docs/SEMIANALYTICPIPELINE.md",
            "docs/HANDOFF_FOPT_SCHEMA.md",
            "docs/HANDOFF_SCHEMAS.md",
            "backend/semianalytic_pipeline.py",
            "backend/T_vs_g_gs_GeV.csv",
        ],
        "commands": commands,
        "files_read": [
            ".codex/agents/fopt-agent.md",
            ".codex/skills/fopt-implementation/SKILL.md",
            "docs/BACKEND_COMPATIBILITY.md",
            "docs/SEMIANALYTICPIPELINE.md",
            "docs/HANDOFF_FOPT_SCHEMA.md",
            "docs/HANDOFF_SCHEMAS.md",
            "output/minimal_conformal_su2_doublet/handoff_model.json",
            "output/minimal_conformal_su2_doublet/handoff_critique.json",
            "output/minimal_conformal_su2_doublet/handoff_librarian_preliminary.json",
            "backend/semianalytic_pipeline.py",
            "backend/T_vs_g_gs_GeV.csv",
        ],
        "files_written": files_written,
        "warnings": warnings,
        "errors": [],
        "approximations": [
            "Classically scale-invariant single-field Coleman-Weinberg backend.",
            "No Higgs portal, dark fermions, scalar mass-ratio scan, daisy thermal-mass scan, or RG-running scan.",
            "f_peak_est uses 1.6e-5 Hz * (beta/H) * (Treh/100 GeV) * (g*/100)^(1/6).",
        ],
        "backend_choice": {
            "selected_backend": "semianalytic_pipeline",
            "executed": True,
            "reason": "Compatible single-field conformal model with masses proportional to vD.",
        },
        "backend": "semianalytic_pipeline",
        "backend_executed": True,
        "expected_upstream_inputs": [
            "output/minimal_conformal_su2_doublet/handoff_model.json",
            "output/minimal_conformal_su2_doublet/handoff_critique.json",
            "output/minimal_conformal_su2_doublet/handoff_librarian_preliminary.json",
        ],
        "missing_upstream_inputs": [],
        "model_parameter_ranges": {
            "gD": {"min": min(row["gD"] for row in rows), "max": max(row["gD"] for row in rows)},
            "vD": {"min_GeV": min(row["vD"] for row in rows), "max_GeV": max(row["vD"] for row in rows)},
        },
        "parameter_basis": {
            "independent": {
                "gD": {"description": "Dark SU(2)_D gauge coupling.", "domain": "0 < gD < sqrt(4*pi)"},
                "vD": {"description": "Coleman-Weinberg vev in GeV.", "domain": "vD > 0"},
            },
            "dependent": {
                "m_WD": "gD * vD / 2",
                "gb_WD": "gD / 2",
                "beta_lambda": "computed by semianalytic_pipeline from boson_gbs and dof",
                "m_chi": "computed by semianalytic_pipeline from beta_lambda and vD",
                "lambda_phi": "Coleman-Weinberg fixed by backend minimization convention",
            },
            "fixed": {"portal_coupling": 0, "dark_fermions": 0, "boson_dofs_W_D": 9},
        },
        "temperature_key": "Treh",
        "scan_status_labels": SCAN_STATUS_LABELS,
        "benchmark_summary": {
            "total_points": len(rows),
            "viable_points": len(viable),
            "failed_points": failed_points,
            "excluded_points": excluded_points,
        },
        "scan_summary": {
            "total_points": len(rows),
            "viable_points": len(viable),
            "failed_points": failed_points,
            "excluded_points": excluded_points,
        },
        "csv_json_alignment": {
            "csv_file": "output/minimal_conformal_su2_doublet/fopt_benchmarks.csv",
            "independent_parameter_columns": ["gD", "vD"],
            "required_result_columns": REQUIRED_RESULT_COLUMNS,
            "status_column": "status",
        },
        "model_parameters": ["gD", "vD"],
        "benchmarks": [benchmark_item(row, i) for i, row in enumerate(rows, 1)],
        "best_points": [benchmark_item(row, i) for i, row in enumerate(best_rows, 1)],
        "prior_ranges": {
            "gD": [min(row["gD"] for row in rows), max(row["gD"] for row in rows)],
            "vD_GeV": [min(row["vD"] for row in rows), max(row["vD"] for row in rows)],
        },
        "validation": {
            "finite_values": bool(all(finite_float(row.get("alpha")) and finite_float(row.get("beta_H")) and finite_float(row.get("Treh")) for row in viable)),
            "percolation_checked": bool(all(row.get("percolation_checked") for row in viable)),
            "eternal_inflation_checked": bool(all(row.get("eternal_inflation") is False for row in viable)),
            "perturbativity_checked": True,
        },
        "output_files": files_written,
    }

    RESULTS_PATH.write_text(json.dumps(handoff, indent=2) + "\n")
    HANDOFF_PATH.write_text(json.dumps(handoff, indent=2) + "\n")

    best_lines = []
    for row in best_rows[:5]:
        best_lines.append(
            f"- {row['name']}: gD={row['gD']:.6g}, vD={row['vD']:.6g} GeV, "
            f"Treh={row['Treh']:.6g} GeV, alpha={row['alpha']:.6g}, "
            f"beta/H={row['beta_H']:.6g}, f_peak_est={row['f_peak_est']:.6g} Hz, "
            f"in_PTA_band={row['in_pta_band_est']}"
        )
    if not best_lines:
        best_lines.append("- No viable points found.")

    REPORT_PATH.write_text(
        "\n".join(
            [
                "# FOPT report: minimal_conformal_su2_doublet",
                "",
                "Backend: `backend/semianalytic_pipeline.py`.",
                "Independent scan axes: `gD`, `vD` only.",
                "Mapping: `chi0 = vD`, `boson_gbs = {'W_D': gD / 2}`, `boson_dofs = {'W_D': 9}`.",
                "",
                f"Total evaluated points: {len(rows)}.",
                f"Viable points: {len(viable)}.",
                f"Numerical failures: {failed_points}.",
                f"Physical/non-FOPT exclusions: {excluded_points}.",
                "",
                "Best viable points by closeness to the PTA steering estimate:",
                *best_lines,
                "",
                "Warnings:",
                *[f"- {warning}" for warning in warnings],
                "",
            ]
        )
    )


def main() -> None:
    points = build_scan_points()
    rows = []
    for index, (gD, vD) in enumerate(points, 1):
        row = evaluate_with_timeout(gD, vD)
        row["name"] = f"point_{index:04d}"
        rows.append(row)
        if index % 25 == 0:
            print(f"evaluated {index}/{len(points)}")
    write_csv(rows)
    write_outputs(rows)
    viable = len([row for row in rows if row["status"] == "viable"])
    pta = len([row for row in rows if row.get("in_pta_band_est")])
    print(f"evaluated_points={len(rows)} viable_points={viable} pta_band_est_points={pta}")


if __name__ == "__main__":
    main()
