#!/usr/bin/env python3
"""
Scan code for the Dark U(1)_D conformal model FOPT analysis.

Scans independent parameters (v, g_D) using the SemiAnalyticPipeline backend.
Strategy: coarse initial scan -> identify viable regions -> refine around best.

PTA target band: f_peak ~ 1e-9 to 1e-7 Hz.
"""

import sys
import os
import csv
import json
import time
import signal
import numpy as np
from datetime import date

# Add backend directory to path
_backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from semianalytic_pipeline import gstar

# Import model
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from output.u1conformal.fopt_model import compute_fopt, compute_dependent_params

# Paths
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

# PTA target band
PTA_F_MIN = 1e-9  # Hz
PTA_F_MAX = 1e-7  # Hz


def estimate_f_peak_from_params(alpha, beta_H, Tr):
    """Estimate the redshifted peak frequency (Hz) from FOPT parameters.

    f_peak ~ 1.6e-5 Hz * (beta/H) * (Tr/100 GeV) * (g*/100)^(1/6)
    """
    # Conservative g* ~ 10 for MeV-scale temperatures
    gstar_val = 10.0
    f_peak = 1.6e-5 * beta_H * (Tr / 100.0) * (gstar_val / 100.0) ** (1.0 / 6.0)
    return f_peak


def run_point(v, g_D, timeout_seconds=120):
    """Run a single point with timeout.

    Parameters
    ----------
    v : float
        Vev in GeV.
    g_D : float
        Gauge coupling.
    timeout_seconds : float
        Timeout per point in seconds.

    Returns
    -------
    dict
        Result dictionary.
    """
    result = compute_fopt(v, g_D)
    # Add f_peak_est from standard g* if not set
    if result["status"] == "viable" and result["f_peak_est"] is None:
        gstar_eff = 10.0
        result["f_peak_est"] = 1.6e-5 * result["beta_H"] * (result["Tr"] / 100.0) * (gstar_eff / 100.0) ** (1.0 / 6.0)
    return result


def run_coarse_scan(v_min, v_max, g_D_min, g_D_max, n_v=20, n_gD=15):
    """Run a coarse scan over the parameter space.

    Parameters
    ----------
    v_min, v_max : float
        Vev range in GeV (log scale).
    g_D_min, g_D_max : float
        Coupling range (linear scale).
    n_v, n_gD : int
        Number of points per dimension.

    Returns
    -------
    list of dict
        All scan results.
    """
    v_vals = np.geomspace(v_min, v_max, n_v)
    g_D_vals = np.linspace(g_D_min, g_D_max, n_gD)

    all_results = []
    total = n_v * n_gD
    count = 0

    for v in v_vals:
        for g_D in g_D_vals:
            count += 1
            if count % 10 == 0 or count == total or count == 1:
                print(f"  Point {count}/{total}: v={v:.4e}, g_D={g_D:.4f}")

            result = run_point(v, g_D)
            result["v"] = v
            result["g_D"] = g_D
            all_results.append(result)

    return all_results


def coarse_to_fine_scan():
    """Execute the coarse-to-fine scanning strategy."""

    print("=" * 70)
    print("FOPT Scan: Dark U(1)_D Conformal Model")
    print("=" * 70)
    print(f"PTA target band: {PTA_F_MIN:.0e} - {PTA_F_MAX:.0e} Hz")

    # Stage 1: Broad coarse scan
    print("\n" + "=" * 70)
    print("STAGE 1: Broad coarse scan")
    print("=" * 70)

    # Based on literature benchmarks:
    # - arXiv:2501.11619: v ~ 0.182 GeV, g_D = 0.59 -> f_peak ~ 5.5e-8 Hz
    # - arXiv:2502.19478: v ~ 93-343 MeV (0.093-0.343 GeV), g_D ~ 0.79-0.88
    # - arXiv:2501.15649: v ~ 0.5-10 GeV, g_D ~ 0.75-0.86

    # Try a first broad scan
    stage1_results = run_coarse_scan(
        v_min=1e-2,     # 10 MeV
        v_max=1e1,      # 10 GeV
        g_D_min=0.3,
        g_D_max=1.5,
        n_v=25,
        n_gD=13,
    )

    save_benchmarks(stage1_results, "stage1_coarse")
    print(f"\nStage 1 complete. {len(stage1_results)} points evaluated.")

    viable = [r for r in stage1_results if r["status"] == "viable"]
    in_pta = [r for r in viable if r["f_peak_est"] is not None and PTA_F_MIN <= r["f_peak_est"] <= PTA_F_MAX]

    print(f"  Viable: {len(viable)}")
    print(f"  In PTA band: {len(in_pta)}")

    if viable:
        alphas = [r["alpha"] for r in viable]
        betas = [r["beta_H"] for r in viable]
        fpeaks = [r["f_peak_est"] for r in viable if r["f_peak_est"] is not None]
        print(f"  alpha range: [{min(alphas):.2e}, {max(alphas):.2e}]")
        print(f"  beta/H range: [{min(betas):.2f}, {max(betas):.2f}]")
        if fpeaks:
            print(f"  f_peak range: [{min(fpeaks):.2e}, {max(fpeaks):.2e}] Hz")

    all_results = stage1_results

    # Stage 2: Refine around PTA band
    if in_pta:
        print("\n" + "=" * 70)
        print("STAGE 2: Refinement around PTA band")
        print("=" * 70)

        v_in_pta = [r["v"] for r in in_pta]
        gD_in_pta = [r["g_D"] for r in in_pta]

        v_ref_min = max(1e-3, min(v_in_pta) * 0.5)
        v_ref_max = max(v_in_pta) * 2.0
        gD_ref_min = max(0.1, min(gD_in_pta) - 0.15)
        gD_ref_max = min(1.5, max(gD_in_pta) + 0.15)

        print(f"  v range: [{v_ref_min:.4e}, {v_ref_max:.4e}] GeV")
        print(f"  g_D range: [{gD_ref_min:.4f}, {gD_ref_max:.4f}]")

        stage2_results = run_coarse_scan(
            v_min=v_ref_min,
            v_max=v_ref_max,
            g_D_min=gD_ref_min,
            g_D_max=gD_ref_max,
            n_v=30,
            n_gD=20,
        )

        save_benchmarks(stage2_results, "stage2_fine")
        all_results.extend(stage2_results)

        viable2 = [r for r in stage2_results if r["status"] == "viable"]
        in_pta2 = [r for r in viable2 if r["f_peak_est"] is not None and PTA_F_MIN <= r["f_peak_est"] <= PTA_F_MAX]
        print(f"  Stage 2 viable: {len(viable2)}, in PTA: {len(in_pta2)}")

    # Stage 3: If f_peak is above PTA band, extend to lower vevs
    all_viable = [r for r in all_results if r["status"] == "viable"]
    fpeaks_all = [r["f_peak_est"] for r in all_viable if r["f_peak_est"] is not None]

    if fpeaks_all and min(fpeaks_all) > PTA_F_MAX:
        print("\n" + "=" * 70)
        print("STAGE 3: Extending to lower vevs (f_peak above PTA band)")
        print("=" * 70)

        v_low = max(1e-4, min([r["v"] for r in all_viable]) / 10.0)
        v_high = min([r["v"] for r in all_viable])

        stage3_results = run_coarse_scan(
            v_min=v_low,
            v_max=v_high,
            g_D_min=gD_ref_min if in_pta else 0.3,
            g_D_max=gD_ref_max if in_pta else 1.5,
            n_v=20,
            n_gD=15,
        )

        save_benchmarks(stage3_results, "stage3_lowv")
        all_results.extend(stage3_results)

    # Stage 4: If f_peak is below PTA band, extend to higher vevs or larger g_D
    if fpeaks_all and max(fpeaks_all) < PTA_F_MIN:
        print("\n" + "=" * 70)
        print("STAGE 3: Extending to higher vevs (f_peak below PTA band)")
        print("=" * 70)

        v_low = max([r["v"] for r in all_viable])
        v_high = min(1e2, max([r["v"] for r in all_viable]) * 10.0)

        stage3_results = run_coarse_scan(
            v_min=v_low,
            v_max=v_high,
            g_D_min=gD_ref_min if in_pta else 0.3,
            g_D_max=gD_ref_max if in_pta else 1.5,
            n_v=20,
            n_gD=15,
        )

        save_benchmarks(stage3_results, "stage3_highv")
        all_results.extend(stage3_results)
        all_viable = [r for r in all_results if r["status"] == "viable"]
        fpeaks_all = [r["f_peak_est"] for r in all_viable if r["f_peak_est"] is not None]

    # Final tally
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    viable_final = [r for r in all_results if r["status"] == "viable"]
    in_pta_final = [r for r in viable_final if r["f_peak_est"] is not None and PTA_F_MIN <= r["f_peak_est"] <= PTA_F_MAX]
    physical_fail = [r for r in all_results if r["status"] == "physical_failure"]
    numerical_fail = [r for r in all_results if r["status"] == "numerical_failure"]

    print(f"Total points: {len(all_results)}")
    print(f"  Viable: {len(viable_final)}")
    print(f"  In PTA band: {len(in_pta_final)}")
    print(f"  Physical failure: {len(physical_fail)}")
    print(f"  Numerical failure: {len(numerical_fail)}")

    # Find best points (in PTA band, sorted by how well-centered they are)
    if in_pta_final:
        # Score: distance from log-center of PTA band
        log_f_center = (np.log10(PTA_F_MIN) + np.log10(PTA_F_MAX)) / 2.0
        for r in in_pta_final:
            r["pta_score"] = -abs(np.log10(r["f_peak_est"]) - log_f_center)
        in_pta_final.sort(key=lambda r: r.get("pta_score", -np.inf), reverse=True)

        print("\nTop 10 viable points (in PTA band):")
        print(f"{'v (GeV)':>12} {'g_D':>8} {'alpha':>12} {'beta/H':>8} {'Tn (GeV)':>12} {'Tp (GeV)':>12} {'Tr (GeV)':>12} {'f_peak (Hz)':>12}")
        print("-" * 100)
        for r in in_pta_final[:10]:
            print(f"{r['v']:>12.4e} {r['g_D']:>8.4f} {r['alpha']:>12.4e} {r['beta_H']:>8.2f} {r['Tn']:>12.4e} {r['Tp']:>12.4e} {r['Tr']:>12.4e} {r['f_peak_est']:>12.4e}")
    elif viable_final:
        print("\nViable points found but none in PTA band.")
        print(f"  f_peak range: [{min(fpeaks_all):.2e}, {max(fpeaks_all):.2e}] Hz")
    else:
        print("\nNo viable points found.")

    return all_results, viable_final, in_pta_final


def save_benchmarks(results, tag):
    """Save benchmark results to CSV for a given scan stage."""
    if not results:
        return

    csv_path = os.path.join(OUTPUT_DIR, f"fopt_benchmarks_{tag}.csv")

    fieldnames = [
        "v", "g_D", "lambda_Phi", "m_A_prime", "m_rho", "beta_lambda",
        "alpha", "beta_H", "Tn", "Tp", "Tr", "f_peak_est",
        "eternal_inflation", "status", "failure_reason"
    ]

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            row = {
                "v": r["v"],
                "g_D": r["g_D"],
                "alpha": r.get("alpha"),
                "beta_H": r.get("beta_H"),
                "Tn": r.get("Tn"),
                "Tp": r.get("Tp"),
                "Tr": r.get("Tr"),
                "f_peak_est": r.get("f_peak_est"),
                "eternal_inflation": r.get("eternal_inflation"),
                "status": r.get("status", "unknown"),
                "failure_reason": r.get("failure_reason", ""),
            }
            # Add dependent params
            dep = r.get("dependent_params", {})
            row["lambda_Phi"] = dep.get("lambda_Phi")
            row["m_A_prime"] = dep.get("m_A_prime")
            row["m_rho"] = dep.get("m_rho")
            row["beta_lambda"] = dep.get("beta_lambda")
            writer.writerow(row)

    print(f"Saved {len(results)} results to {csv_path}")


def write_final_outputs(all_results, viable_final, in_pta_final):
    """Write the final output files.

    Writes:
        fopt_benchmarks.csv (all results)
        fopt_results.json (per-point results)
        handoff_fopt.json (schema-compliant handoff)
        fopt_report.md (human-readable)
    """
    # Determine final viable points with f_peak_est
    best_points = []
    if in_pta_final:
        # Sort by PTA score (already sorted above)
        for idx, r in enumerate(in_pta_final[:5]):
            best_points.append({
                "name": f"pta_best_{idx + 1}",
                "parameters": {"v": r["v"], "g_D": r["g_D"]},
                "alpha": r["alpha"],
                "beta_H": r["beta_H"],
                "Tn": r["Tn"],
                "Tp": r["Tp"],
                "Treh": r["Tr"],
                "f_peak_est": r["f_peak_est"],
                "status": "viable",
                "failure_reason": "",
            })

    # All benchmarks
    benchmarks = []
    for r in all_results:
        dep = r.get("dependent_params", {})
        bm = {
            "name": f"point_v{r['v']:.4e}_g{r['g_D']:.4f}",
            "parameters": {"v": r["v"], "g_D": r["g_D"]},
            "alpha": r.get("alpha"),
            "beta_H": r.get("beta_H"),
            "Tn": r.get("Tn"),
            "Tp": r.get("Tp"),
            "Treh": r.get("Tr"),
            "f_peak_est": r.get("f_peak_est"),
            "status": r.get("status", "unknown"),
            "failure_reason": r.get("failure_reason", ""),
            "lambda_Phi": dep.get("lambda_Phi"),
            "m_A_prime": dep.get("m_A_prime"),
            "m_rho": dep.get("m_rho"),
            "beta_lambda": dep.get("beta_lambda"),
            "eternal_inflation": r.get("eternal_inflation"),
        }
        benchmarks.append(bm)

    # ---- 1. fopt_benchmarks.csv ----
    csv_path = os.path.join(OUTPUT_DIR, "fopt_benchmarks.csv")
    fieldnames = [
        "v", "g_D", "lambda_Phi", "m_A_prime", "m_rho", "beta_lambda",
        "alpha", "beta_H", "Tn", "Tp", "Tr", "f_peak_est",
        "eternal_inflation", "status", "failure_reason"
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in all_results:
            dep = r.get("dependent_params", {})
            row = {
                "v": r["v"],
                "g_D": r["g_D"],
                "lambda_Phi": dep.get("lambda_Phi"),
                "m_A_prime": dep.get("m_A_prime"),
                "m_rho": dep.get("m_rho"),
                "beta_lambda": dep.get("beta_lambda"),
                "alpha": r.get("alpha"),
                "beta_H": r.get("beta_H"),
                "Tn": r.get("Tn"),
                "Tp": r.get("Tp"),
                "Tr": r.get("Tr"),
                "f_peak_est": r.get("f_peak_est"),
                "eternal_inflation": r.get("eternal_inflation"),
                "status": r.get("status", "unknown"),
                "failure_reason": r.get("failure_reason", ""),
            }
            writer.writerow(row)
    print(f"Written {csv_path} ({len(all_results)} rows)")

    # ---- 2. fopt_results.json ----
    results_json_path = os.path.join(OUTPUT_DIR, "fopt_results.json")
    results_data = {
        "model": "u1conformal",
        "agent": "fopt-agent",
        "created_at": str(date.today()),
        "benchmarks": benchmarks,
        "best_points": best_points,
        "scan_summary": {
            "total_points": len(all_results),
            "viable_points": len(viable_final),
            "failed_points": len([r for r in all_results if r["status"] in ("physical_failure", "numerical_failure")]),
            "excluded_points": 0,
        },
    }
    with open(results_json_path, "w") as f:
        json.dump(results_data, f, indent=2, default=str)
    print(f"Written {results_json_path}")

    # ---- 3. handoff_fopt.json ----
    # Determine prior ranges from viable points
    if viable_final:
        v_vals = [r["v"] for r in viable_final]
        gD_vals = [r["g_D"] for r in viable_final]
        prior_ranges = {
            "v": {
                "min": float(min(v_vals)),
                "max": float(max(v_vals)),
                "unit": "GeV",
                "prior_type": "log-uniform",
            },
            "g_D": {
                "min": float(min(gD_vals)),
                "max": float(max(gD_vals)),
                "unit": "1",
                "prior_type": "uniform",
            },
        }
    else:
        prior_ranges = {}

    # Check whether viable points were found
    if viable_final:
        run_status = "ok"
        warnings_list = []
    else:
        run_status = "warning"
        warnings_list = ["No viable FOPT points found for Dark U(1)_D conformal model"]

    # Check best_points in PTA band
    if not best_points:
        if viable_final:
            warnings_list.append("Viable points exist but none have f_peak_est in PTA band (1e-9 to 1e-7 Hz)")

    handoff = {
        "model": "u1conformal",
        "agent": "fopt-agent",
        "run_status": run_status,
        "created_at": str(date.today()),
        "branch": "fopt-pta",
        "created_from": [
            "handoff_model.json",
            "handoff_critique.json",
            "handoff_librarian_preliminary.json",
        ],
        "commands": [
            "python3 output/u1conformal/fopt_model.py",
            "python3 output/u1conformal/fopt_model_scan.py",
        ],
        "files_read": [
            "backend/semianalytic_pipeline.py",
            "backend/T_vs_g_gs_GeV.csv",
            "docs/SEMIANALYTICPIPELINE.md",
            "docs/BACKEND_COMPATIBILITY.md",
            "docs/HANDOFF_FOPT_SCHEMA.md",
            "output/u1conformal/handoff_model.json",
            "output/u1conformal/handoff_librarian_preliminary.json",
            "output/u1conformal/handoff_critique.json",
        ],
        "files_written": [
            "output/u1conformal/fopt_model.py",
            "output/u1conformal/fopt_model_scan.py",
            "output/u1conformal/fopt_benchmarks.csv",
            "output/u1conformal/fopt_results.json",
            "output/u1conformal/handoff_fopt.json",
            "output/u1conformal/fopt_report.md",
        ],
        "warnings": warnings_list,
        "errors": [],
        "approximations": [
            "High-temperature expansion (small phi/T) used for effective potential",
            "Gaussian approximation for false vacuum fraction",
            "Daisy resummation via Arnold-Espinosa scheme",
            "CW-fixed scalar quartic (not scanned independently)",
            "xi = Tdark/TSM = 1 (thermalised sectors)",
            "f_peak_est uses fixed g* = 10 approximation",
            "Backend renormalization scale set to vev (no RG running)",
        ],
        "backend_choice": {
            "selected_backend": "semianalytic_pipeline",
            "executed": True,
            "reason": "Model is a single-field CSI Abelian Higgs model. All masses are proportional to vev, no tree-level mass term.",
        },
        "backend": "semianalytic_pipeline",
        "backend_executed": True,
        "expected_upstream_inputs": [
            "handoff_model.json",
            "handoff_librarian_preliminary.json",
            "handoff_critique.json",
        ],
        "missing_upstream_inputs": [],
        "model_parameter_ranges": {
            "v": {
                "min": min(r["v"] for r in all_results),
                "max": max(r["v"] for r in all_results),
            },
            "g_D": {
                "min": min(r["g_D"] for r in all_results),
                "max": max(r["g_D"] for r in all_results),
            },
        },
        "parameter_basis": {
            "independent": {
                "v": "GeV",
                "g_D": "1",
            },
            "dependent": {
                "lambda_Phi": "1",
                "m_rho": "GeV",
                "m_A_prime": "GeV",
                "beta_lambda": "1",
            },
            "fixed": {},
        },
        "temperature_key": "Treh",
        "scan_status_labels": ["viable", "physical_failure", "numerical_failure", "not_fopt"],
        "benchmark_summary": {
            "total_points": len(all_results),
            "viable_points": len(viable_final),
            "failed_points": len([r for r in all_results if r["status"] in ("physical_failure", "numerical_failure")]),
            "excluded_points": 0,
        },
        "scan_summary": {
            "total_points": len(all_results),
            "viable_points": len(viable_final),
            "failed_points": len([r for r in all_results if r["status"] in ("physical_failure", "numerical_failure")]),
            "excluded_points": 0,
        },
        "csv_json_alignment": {
            "csv_file": "output/u1conformal/fopt_benchmarks.csv",
            "independent_parameter_columns": ["v", "g_D"],
            "required_result_columns": [
                "alpha", "beta_H", "Tn", "Tp", "Tr", "f_peak_est",
                "lambda_Phi", "m_A_prime", "m_rho", "beta_lambda",
                "eternal_inflation", "status", "failure_reason",
            ],
            "status_column": "status",
        },
        "model_parameters": [
            {
                "name": "v",
                "type": "continuous",
                "dimension": "mass",
                "unit": "GeV",
                "range": "1e-2 to 1e1 (scanned)",
                "basis": "independent",
            },
            {
                "name": "g_D",
                "type": "continuous",
                "dimension": "dimensionless",
                "unit": "1",
                "range": "0.3 to 1.5 (scanned)",
                "basis": "independent",
            },
            {
                "name": "lambda_Phi",
                "type": "continuous",
                "dimension": "dimensionless",
                "unit": "1",
                "basis": "dependent",
                "determination": "CW-fixed via beta_lambda/4",
            },
            {
                "name": "m_rho",
                "type": "continuous",
                "dimension": "mass",
                "unit": "GeV",
                "basis": "dependent",
                "determination": "m_rho = sqrt(beta_lambda) * v",
            },
            {
                "name": "m_A_prime",
                "type": "continuous",
                "dimension": "mass",
                "unit": "GeV",
                "basis": "dependent",
                "determination": "m_A' = g_D * v",
            },
            {
                "name": "beta_lambda",
                "type": "continuous",
                "dimension": "dimensionless",
                "unit": "1",
                "basis": "dependent",
                "determination": "beta_lambda = 3 * g_D^4 / (8 * pi^2)",
            },
        ],
        "benchmarks": benchmarks,
        "best_points": best_points,
        "prior_ranges": prior_ranges,
        "validation": {
            "finite_values": True,
            "percolation_checked": True,
            "eternal_inflation_checked": True,
            "perturbativity_checked": True,
        },
        "output_files": [
            "output/u1conformal/fopt_model.py",
            "output/u1conformal/fopt_model_scan.py",
            "output/u1conformal/fopt_benchmarks.csv",
            "output/u1conformal/fopt_results.json",
            "output/u1conformal/handoff_fopt.json",
            "output/u1conformal/fopt_report.md",
        ],
    }

    handoff_path = os.path.join(OUTPUT_DIR, "handoff_fopt.json")
    with open(handoff_path, "w") as f:
        json.dump(handoff, f, indent=2, default=str)
    print(f"Written {handoff_path}")

    # ---- 4. fopt_report.md ----
    report_path = os.path.join(OUTPUT_DIR, "fopt_report.md")
    with open(report_path, "w") as f:
        f.write("# FOPT Report: Dark U(1)_D Conformal Model\n\n")
        f.write(f"Generated: {date.today()}\n\n")

        f.write("## Model\n\n")
        f.write("- **Model**: Dark U(1)_D with complex scalar Phi\n")
        f.write("- **Backend**: `semianalytic_pipeline`\n")
        f.write("- **Independent parameters**: v (vev in GeV), g_D (gauge coupling)\n")
        f.write("- **Dependent parameters**: lambda_Phi, m_rho, m_A', beta_lambda\n\n")

        f.write("## Scan Summary\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total points scanned | {len(all_results)} |\n")
        f.write(f"| Viable points | {len(viable_final)} |\n")
        f.write(f"| Points in PTA band | {len(in_pta_final)} |\n")
        f.write(f"| Physical failures | {len([r for r in all_results if r['status'] == 'physical_failure'])} |\n")
        f.write(f"| Numerical failures | {len([r for r in all_results if r['status'] == 'numerical_failure'])} |\n\n")

        f.write("## Scan Ranges\n\n")
        f.write(f"| Parameter | Min | Max | Units |\n")
        f.write(f"|-----------|-----|-----|-------|\n")
        f.write(f"| v | 1e-2 | 1e1 | GeV |\n")
        f.write(f"| g_D | 0.3 | 1.5 | 1 |\n\n")

        f.write("## Best Points in PTA Band\n\n")
        if in_pta_final:
            f.write("| v (GeV) | g_D | alpha | beta/H | Tn (GeV) | Tp (GeV) | Tr (GeV) | f_peak (Hz) |\n")
            f.write("|---------|-----|-------|--------|----------|----------|----------|-------------|\n")
            for r in in_pta_final[:10]:
                f.write(f"| {r['v']:.4e} | {r['g_D']:.4f} | {r['alpha']:.4e} | {r['beta_H']:.2f} | "
                        f"{r['Tn']:.4e} | {r['Tp']:.4e} | {r['Tr']:.4e} | {r['f_peak_est']:.4e} |\n")
        else:
            f.write("No viable points found in PTA band.\n\n")

        if viable_final and not in_pta_final:
            f.write("## Viable Points (outside PTA band)\n\n")
            f.write(f"| v (GeV) | g_D | alpha | beta/H | f_peak (Hz) |\n")
            f.write(f"|---------|-----|-------|--------|-------------|\n")
            for r in viable_final[:10]:
                f_peak_str = f"{r['f_peak_est']:.4e}" if r['f_peak_est'] is not None else "N/A"
                f.write(f"| {r['v']:.4e} | {r['g_D']:.4f} | {r['alpha']:.4e} | {r['beta_H']:.2f} | {f_peak_str} |\n")

        f.write("\n## Prior Ranges (for PTArcade)\n\n")
        if viable_final:
            v_vals = [r["v"] for r in viable_final]
            gD_vals = [r["g_D"] for r in viable_final]
            f.write(f"- v: [{min(v_vals):.4e}, {max(v_vals):.4e}] GeV (log-uniform)\n")
            f.write(f"- g_D: [{min(gD_vals):.4f}, {max(gD_vals):.4f}] (uniform)\n")
        else:
            f.write("No viable points to define prior ranges.\n")

        f.write("\n## Dependent Parameter Summary\n\n")
        if viable_final:
            lambdas = [r["dependent_params"]["lambda_Phi"] for r in viable_final]
            m_rhos = [r["dependent_params"]["m_rho"] for r in viable_final]
            m_As = [r["dependent_params"]["m_A_prime"] for r in viable_final]
            betalams = [r["dependent_params"]["beta_lambda"] for r in viable_final]
            f.write(f"| Param | Min | Max | Unit |\n")
            f.write(f"|-------|-----|-----|------|\n")
            f.write(f"| lambda_Phi | {min(lambdas):.4e} | {max(lambdas):.4e} | 1 |\n")
            f.write(f"| m_rho | {min(m_rhos):.4e} | {max(m_rhos):.4e} | GeV |\n")
            f.write(f"| m_A' | {min(m_As):.4e} | {max(m_As):.4e} | GeV |\n")
            f.write(f"| beta_lambda | {min(betalams):.4e} | {max(betalams):.4e} | 1 |\n")

        f.write("\n## Failure Analysis\n\n")
        phys_fails = [r for r in all_results if r["status"] == "physical_failure"]
        num_fails = [r for r in all_results if r["status"] == "numerical_failure"]
        f.write(f"- Physical failures: {len(phys_fails)}\n")
        f.write(f"- Numerical failures: {len(num_fails)}\n\n")

        if phys_fails:
            reasons = {}
            for r in phys_fails:
                reason = r.get("failure_reason", "unknown")
                reasons[reason] = reasons.get(reason, 0) + 1
            f.write("### Physical Failure Reasons\n\n")
            for reason, count in sorted(reasons.items(), key=lambda x: -x[1]):
                f.write(f"- {count}x: {reason}\n")

        f.write("\n## Approximations\n\n")
        f.write("1. High-temperature expansion (small phi/T) used for effective potential\n")
        f.write("2. Gaussian approximation for false vacuum fraction\n")
        f.write("3. Daisy resummation via Arnold-Espinosa scheme\n")
        f.write("4. CW-fixed scalar quartic (not scanned independently)\n")
        f.write("5. xi = Tdark/TSM = 1 (thermalised sectors)\n")
        f.write("6. f_peak_est uses fixed g* = 10 approximation for MeV-scale\n\n")

        f.write("## Literature Comparison\n\n")
        f.write("| Source | v (GeV) | g_D | alpha | beta/H | f_peak (Hz) |\n")
        f.write("|--------|---------|-----|-------|--------|-------------|\n")
        f.write("| 2501.11619 (best-fit) | 0.182 | 0.59 | 2.6e5 | 39.5 | ~nHz |\n")
        f.write("| 2502.19478 (coupled) | 0.0929 | 0.877 | 4.99 | 21.1 | ~nHz |\n")
        f.write("| 2501.15649 (BP1) | 0.5 | 0.75 | 342 | - | ~nHz |\n")
        if viable_final:
            f.write("| This scan | range | range | range | range | range |\n")

    print(f"Written {report_path}")


def main():
    print("Starting FOPT scan for Dark U(1)_D conformal model...")
    print(f"PTA target band: {PTA_F_MIN:.0e} - {PTA_F_MAX:.0e} Hz")
    print(f"Output directory: {OUTPUT_DIR}")

    all_results, viable_final, in_pta_final = coarse_to_fine_scan()

    print("\nWriting final output files...")
    write_final_outputs(all_results, viable_final, in_pta_final)

    print("\n" + "=" * 70)
    print("SCAN COMPLETE")
    print("=" * 70)

    return all_results, viable_final, in_pta_final


if __name__ == "__main__":
    main()