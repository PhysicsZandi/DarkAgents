"""Bounded coarse-to-fine FOPT scan for the minimal conformal U(1)_D model."""

from __future__ import annotations

import csv
import json
import math
import signal
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from fopt_model import (  # noqa: E402
    BRANCH,
    MODEL,
    PTA_FREQUENCY_BAND_HZ,
    evaluate_point,
    point_to_dict,
)


CSV_FILE = HERE / "fopt_benchmarks.csv"
REPORT_FILE = HERE / "fopt_report.md"
HANDOFF_FILE = HERE / "handoff_fopt.json"
RESULTS_FILE = HERE / "fopt_results.json"
PER_POINT_TIMEOUT_SECONDS = 20

CSV_COLUMNS = [
    "v",
    "g_D",
    "lambda_Phi",
    "beta_lambda",
    "m_Aprime",
    "m_rho",
    "Tn",
    "Tp",
    "Treh",
    "alpha",
    "beta_H",
    "g_star",
    "f_peak_est",
    "eternal_inflation",
    "status",
    "failure_reason",
]


class PointTimeout(RuntimeError):
    pass


def _timeout_handler(_signum: int, _frame: Any) -> None:
    raise PointTimeout(f"backend call exceeded {PER_POINT_TIMEOUT_SECONDS} s")


def unique_sorted(values: Iterable[float]) -> list[float]:
    return sorted({round(float(v), 12) for v in values if math.isfinite(float(v)) and float(v) > 0.0})


def grid(v_values: Iterable[float], g_values: Iterable[float]) -> list[tuple[float, float]]:
    return [(v, g) for v in unique_sorted(v_values) for g in unique_sorted(g_values)]


def first_pass_grid() -> list[tuple[float, float]]:
    v_values = np.geomspace(0.01, 1.0, 10)
    g_values = [0.10, 0.20, 0.30, 0.40, 0.50, 0.57, 0.60, 0.65, 0.677, 0.70, 0.75, 0.90]
    return grid(v_values, g_values)


def expanded_grid() -> list[tuple[float, float]]:
    v_values = np.geomspace(0.001, 10.0, 14)
    g_values = np.linspace(0.05, 1.50, 16)
    return grid(v_values, g_values)


def refinement_grid(points: list[dict[str, Any]]) -> list[tuple[float, float]]:
    viable = [p for p in points if p["status"] == "viable"]
    if not viable:
        return expanded_grid()
    low, high = PTA_FREQUENCY_BAND_HZ
    f_values = [p["f_peak_est"] for p in viable if p.get("f_peak_est")]
    g_values = [p["g_D"] for p in viable]
    g_min = max(0.03, min(g_values) * 0.80)
    g_max = min(1.80, max(g_values) * 1.20)
    if f_values and min(f_values) > high:
        v_values = np.geomspace(1.0e-4, max(0.2, max(p["v"] for p in viable)), 16)
    elif f_values and max(f_values) < low:
        v_values = np.geomspace(min(p["v"] for p in viable), 20.0, 16)
    else:
        in_band = [p for p in viable if p.get("f_peak_est") and low <= p["f_peak_est"] <= high]
        seed = in_band or viable
        v_min = max(1.0e-4, min(p["v"] for p in seed) / 2.0)
        v_max = min(20.0, max(p["v"] for p in seed) * 2.0)
        v_values = np.geomspace(v_min, v_max, 16)
    return grid(v_values, np.linspace(g_min, g_max, 16))


def evaluate_with_timeout(v: float, g_D: float) -> dict[str, Any]:
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(PER_POINT_TIMEOUT_SECONDS)
    try:
        return point_to_dict(evaluate_point(v, g_D))
    except PointTimeout as exc:
        return {
            "v": v,
            "g_D": g_D,
            "lambda_Phi": None,
            "beta_lambda": None,
            "m_Aprime": None,
            "m_rho": None,
            "Tn": None,
            "Tp": None,
            "Treh": None,
            "alpha": None,
            "beta_H": None,
            "g_star": None,
            "f_peak_est": None,
            "eternal_inflation": None,
            "status": "numerical_failure",
            "failure_reason": f"timeout: {exc}",
        }
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


def in_pta_band(point: dict[str, Any]) -> bool:
    f_peak = point.get("f_peak_est")
    return point.get("status") == "viable" and f_peak is not None and PTA_FREQUENCY_BAND_HZ[0] <= f_peak <= PTA_FREQUENCY_BAND_HZ[1]


def distance_to_pta_center(point: dict[str, Any]) -> float:
    f_peak = point.get("f_peak_est")
    if f_peak is None or f_peak <= 0.0:
        return float("inf")
    center = math.sqrt(PTA_FREQUENCY_BAND_HZ[0] * PTA_FREQUENCY_BAND_HZ[1])
    return abs(math.log10(f_peak / center))


def run_scan() -> tuple[list[dict[str, Any]], list[str]]:
    attempted: set[tuple[float, float]] = set()
    points: list[dict[str, Any]] = []
    scan_notes: list[str] = []

    passes = [("literature_seeded_coarse", first_pass_grid())]
    pass_index = 0
    while pass_index < len(passes):
        name, candidates = passes[pass_index]
        new_candidates = [(v, g) for v, g in candidates if (v, g) not in attempted]
        scan_notes.append(f"{name}: evaluating {len(new_candidates)} new points")
        for v, g in new_candidates:
            attempted.add((v, g))
            point = evaluate_with_timeout(v, g)
            point["scan_pass"] = name
            points.append(point)

        viable_count = sum(1 for p in points if p["status"] == "viable")
        pta_count = sum(1 for p in points if in_pta_band(p))
        if pass_index == 0 and viable_count == 0:
            passes.append(("expanded_no_viable_fopt", expanded_grid()))
        elif pass_index == 0 and pta_count == 0:
            passes.append(("pta_frequency_refinement", refinement_grid(points)))
        elif pass_index == 1 and viable_count > 0 and pta_count == 0:
            passes.append(("second_pta_frequency_refinement", refinement_grid(points)))
        pass_index += 1

    return points, scan_notes


def clean_for_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: clean_for_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean_for_json(v) for v in value]
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        value = float(value)
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def write_csv(points: list[dict[str, Any]]) -> None:
    with CSV_FILE.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS + ["scan_pass"])
        writer.writeheader()
        for point in points:
            row = {key: point.get(key) for key in CSV_COLUMNS + ["scan_pass"]}
            writer.writerow(row)


def benchmark_item(index: int, point: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": f"scan_point_{index:04d}",
        "parameters": {"v": point["v"], "g_D": point["g_D"]},
        "alpha": point.get("alpha"),
        "beta_H": point.get("beta_H"),
        "Tn": point.get("Tn"),
        "Tp": point.get("Tp"),
        "Treh": point.get("Treh"),
        "f_peak_est": point.get("f_peak_est"),
        "_comment_f_peak_est": "template-independent, order-of-magnitude redshifted peak frequency in Hz; anchors the vev/temperature scale for the PTA agent and must not be treated as the true spectral peak",
        "status": point.get("status"),
        "failure_reason": point.get("failure_reason", ""),
    }


def build_payload(points: list[dict[str, Any]], scan_notes: list[str]) -> dict[str, Any]:
    counts = Counter(p["status"] for p in points)
    viable = [p for p in points if p["status"] == "viable"]
    in_band = [p for p in viable if in_pta_band(p)]
    best_source = in_band if in_band else viable
    best_points = sorted(best_source, key=distance_to_pta_center)[:10]
    warnings = [
        "lambda_Phi is CW/backend-fixed and not exported as a standalone numeric input by backend/semianalytic_pipeline.py; it is therefore not scanned and is recorded as an internal dependent parameter.",
        "f_peak_est is an order-of-magnitude scale setter only; PTA spectral templates are owned by the PTA stage.",
        "Portal and kinetic-mixing effects are neglected in the FOPT calculation, following the upstream critic assumptions.",
    ]
    if viable and not in_band:
        warnings.append("Viable FOPT points were found, but none landed inside the nominal 1e-9-1e-7 Hz PTA estimate band after adaptive refinement.")
    if not viable:
        warnings.append("No viable FOPT point was found after the coarse and expanded scans.")

    total = len(points)
    failed = counts["numerical_failure"] + counts["not_fopt"]
    excluded = counts["physical_failure"]
    summary = {
        "total_points": total,
        "viable_points": counts["viable"],
        "failed_points": failed,
        "excluded_points": excluded,
    }

    payload = {
        "model": MODEL,
        "agent": "fopt-agent",
        "run_status": "ok" if viable else "warning",
        "created_at": date.today().isoformat(),
        "branch": BRANCH,
        "created_from": [
            ".codex/agents/fopt-agent.md",
            ".codex/skills/fopt-implementation/SKILL.md",
            "docs/HANDOFF_SCHEMAS.md",
            "docs/HANDOFF_FOPT_SCHEMA.md",
            "docs/BACKEND_COMPATIBILITY.md",
            "docs/SEMIANALYTICPIPELINE.md",
            "backend/semianalytic_pipeline.py",
            "backend/T_vs_g_gs_GeV.csv",
            "output/u1conformal/handoff_model.json",
            "output/u1conformal/handoff_critique.json",
            "output/u1conformal/handoff_librarian_preliminary.json",
        ],
        "commands": [
            "MPLCONFIGDIR=output/u1conformal/.mplconfig conda run -n ptarcade python output/u1conformal/fopt_model.py",
            "MPLCONFIGDIR=output/u1conformal/.mplconfig conda run -n ptarcade python output/u1conformal/fopt_model_scan.py",
        ],
        "files_read": [
            ".codex/agents/fopt-agent.md",
            ".codex/skills/fopt-implementation/SKILL.md",
            "docs/HANDOFF_SCHEMAS.md",
            "docs/HANDOFF_FOPT_SCHEMA.md",
            "docs/BACKEND_COMPATIBILITY.md",
            "docs/SEMIANALYTICPIPELINE.md",
            "backend/semianalytic_pipeline.py",
            "backend/T_vs_g_gs_GeV.csv",
            "output/u1conformal/handoff_model.json",
            "output/u1conformal/handoff_critique.json",
            "output/u1conformal/handoff_librarian_preliminary.json",
        ],
        "files_written": [
            "output/u1conformal/fopt_model.py",
            "output/u1conformal/fopt_model_scan.py",
            "output/u1conformal/fopt_benchmarks.csv",
            "output/u1conformal/fopt_report.md",
            "output/u1conformal/handoff_fopt.json",
            "output/u1conformal/fopt_results.json",
        ],
        "warnings": warnings,
        "errors": [],
        "approximations": [
            "Semi-analytic conformal single-field backend with scalar/Goldstone contributions treated as subleading.",
            "High-temperature polynomial form is used as in docs/SEMIANALYTICPIPELINE.md.",
            "Gaussian false-vacuum-fraction/percolation approximation from the backend.",
            "g_* for f_peak_est is interpolated from backend/T_vs_g_gs_GeV.csv and clamped at table boundaries.",
        ],
        "backend_choice": {
            "selected_backend": "semianalytic_pipeline",
            "executed": True,
            "reason": "The model is a classically scale-invariant single-field U(1)_D Coleman-Weinberg model with masses proportional to v.",
        },
        "backend": "semianalytic_pipeline",
        "backend_executed": True,
        "expected_upstream_inputs": [
            "output/u1conformal/handoff_model.json",
            "output/u1conformal/handoff_critique.json",
            "output/u1conformal/handoff_librarian_preliminary.json",
        ],
        "missing_upstream_inputs": [],
        "model_parameter_ranges": {
            "v": {"units": "GeV", "scanned_min": min(p["v"] for p in points), "scanned_max": max(p["v"] for p in points)},
            "g_D": {"scanned_min": min(p["g_D"] for p in points), "scanned_max": max(p["g_D"] for p in points)},
        },
        "parameter_basis": {
            "independent": {
                "v": {"units": "GeV", "description": "Dark Higgs background vev <chi>; CSV column v."},
                "g_D": {"description": "U(1)_D gauge coupling in charge-one convention; CSV column g_D."},
            },
            "dependent": {
                "lambda_Phi": {"description": "CW-fixed scalar quartic eliminated by the backend; not scanned independently."},
                "beta_lambda": "3 * g_D**4 / (8 * pi**2)",
                "m_Aprime": "g_D * v",
                "m_rho": "sqrt(beta_lambda) * v",
            },
            "fixed": {
                "q_Phi": 1,
                "xi": 1,
                "boson_gbs": {"Aprime": "g_D"},
                "boson_dofs": {"Aprime": 3},
                "fermion_gfs": {},
                "fermion_dofs": {},
            },
        },
        "temperature_key": "Treh",
        "scan_status_labels": ["viable", "physical_failure", "numerical_failure", "not_fopt"],
        "benchmark_summary": summary,
        "scan_summary": summary,
        "csv_json_alignment": {
            "csv_file": "output/u1conformal/fopt_benchmarks.csv",
            "independent_parameter_columns": ["v", "g_D"],
            "required_result_columns": ["alpha", "beta_H", "Tn", "Tp", "Treh", "f_peak_est", "status"],
            "status_column": "status",
        },
        "model_parameters": ["v", "g_D"],
        "benchmarks": [benchmark_item(i + 1, p) for i, p in enumerate(points)],
        "best_points": [benchmark_item(i + 1, p) for i, p in enumerate(best_points)],
        "prior_ranges": {
            "v": {"units": "GeV", "min": min(p["v"] for p in points), "max": max(p["v"] for p in points), "scale": "log"},
            "g_D": {"min": min(p["g_D"] for p in points), "max": max(p["g_D"] for p in points), "scale": "mixed linear/seeded"},
        },
        "validation": {
            "finite_values": all(
                p["status"] != "viable"
                or all(p.get(k) is not None and p[k] > 0.0 for k in ("alpha", "beta_H", "Tp", "Treh"))
                for p in points
            ),
            "percolation_checked": True,
            "eternal_inflation_checked": True,
            "perturbativity_checked": True,
        },
        "output_files": [
            "output/u1conformal/fopt_model.py",
            "output/u1conformal/fopt_model_scan.py",
            "output/u1conformal/fopt_benchmarks.csv",
            "output/u1conformal/fopt_report.md",
            "output/u1conformal/handoff_fopt.json",
            "output/u1conformal/fopt_results.json",
        ],
        "scan_notes": scan_notes,
        "status_counts": dict(counts),
    }
    return clean_for_json(payload)


def write_report(payload: dict[str, Any]) -> None:
    summary = payload["scan_summary"]
    best = payload["best_points"][:5]
    lines = [
        "# FOPT Report: u1conformal",
        "",
        "## Backend",
        "",
        "Selected backend: `backend/semianalytic_pipeline.py`.",
        "Mapping: `chi0=v`, `boson_gbs={\"Aprime\": g_D}`, `boson_dofs={\"Aprime\": 3}`, no fermions, `xi=1`.",
        "",
        "## Scan",
        "",
        f"Total evaluated points: {summary['total_points']}",
        f"Viable FOPT points: {summary['viable_points']}",
        f"Failed/not-FOPT points: {summary['failed_points']}",
        f"Perturbativity/physical exclusions: {summary['excluded_points']}",
        "",
        "Scan notes:",
    ]
    lines.extend(f"- {note}" for note in payload.get("scan_notes", []))
    lines.extend([
        "",
        "The independent scan columns are exactly `v` [GeV] and `g_D`. `lambda_Phi`, `beta_lambda`, `m_Aprime`, and `m_rho` are dependent diagnostics and were not scanned.",
        "",
        "## Best Points",
        "",
    ])
    if best:
        lines.append("| v [GeV] | g_D | alpha | beta/H | Tn [GeV] | Tp [GeV] | Treh [GeV] | f_peak_est [Hz] |")
        lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for item in best:
            p = item["parameters"]
            lines.append(
                f"| {p['v']:.6g} | {p['g_D']:.6g} | {item['alpha']:.6g} | {item['beta_H']:.6g} | "
                f"{item['Tn']:.6g} | {item['Tp']:.6g} | {item['Treh']:.6g} | {item['f_peak_est']:.6g} |"
            )
    else:
        lines.append("No viable point was found.")
    lines.extend([
        "",
        "## Caveats",
        "",
        "- `f_peak_est` uses the template-independent estimate `1.6e-5 Hz * (beta/H) * (Treh/100 GeV) * (g_*/100)^(1/6)` and is only an order-of-magnitude PTA scale anchor.",
        "- The semi-analytic backend omits portal and kinetic-mixing effects in the thermal potential, as requested by the upstream critic handoff.",
        "- `lambda_Phi` is Coleman-Weinberg/backend-fixed but not exported numerically by the backend; it is recorded as dependent and never scanned.",
    ])
    REPORT_FILE.write_text("\n".join(lines) + "\n")


def main() -> None:
    points, scan_notes = run_scan()
    write_csv(points)
    payload = build_payload(points, scan_notes)
    write_report(payload)
    HANDOFF_FILE.write_text(json.dumps(payload, indent=2) + "\n")
    RESULTS_FILE.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "total_points": payload["scan_summary"]["total_points"],
        "viable_points": payload["scan_summary"]["viable_points"],
        "best_points": payload["best_points"][:3],
        "status_counts": payload["status_counts"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
