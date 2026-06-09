"""
fopt_model_scan.py -- Scan over independent parameters of the conformal U(1)_D
dark sector model to find viable FOPT points producing GW in the PTA band.

Strategy:
1. Start with a coarse grid around literature benchmarks (Balan et al. 2502.19478)
2. Refine around viable regions
3. If no viable points found, extend ranges by one order of magnitude
4. Repeat until backend fails or f_peak_est leaves PTA band
"""

import sys
import os
import numpy as np
import csv
import json
import time
import signal
import traceback

# Add backend directory to path
_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from fopt_model import compute_fopt, is_viable, compute_dependent_params


# PTA frequency band (Hz)
PTA_F_MIN = 1e-9
PTA_F_MAX = 1e-7


class TimeoutError(Exception):
    """Raised when a computation times out."""
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Computation timed out")


def compute_with_timeout(g_D, y_psi, v, timeout_seconds=120):
    """
    Compute FOPT with a timeout guard.

    Parameters
    ----------
    g_D : float
    y_psi : float
    v : float
    timeout_seconds : int

    Returns
    -------
    dict
    """
    # Set timeout signal
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)

    try:
        result = compute_fopt(g_D, y_psi, v)
        return result
    finally:
        signal.alarm(0)


def physical_guards(g_D, y_psi, v):
    """
    Check physical constraints before calling the backend.

    Returns
    -------
    tuple (bool, str)
        (passes, reason if failed)
    """
    if v <= 0:
        return False, "vev <= 0"
    if g_D <= 0:
        return False, "g_D <= 0"
    if y_psi < 0:
        return False, "y_psi < 0"
    if g_D > 4 * np.pi:
        return False, "g_D > 4*pi (non-perturbative)"
    if y_psi > 4 * np.pi:
        return False, "y_psi > 4*pi (non-perturbative)"

    # CW condition: beta_lambda > 0 => y_psi < (3/2)^{1/4} * g_D
    y_psi_max_cw = (3.0 / 2.0) ** 0.25 * g_D
    if y_psi >= y_psi_max_cw:
        return False, f"y_psi >= (3/2)^(1/4)*g_D = {y_psi_max_cw:.4f} (CW condition fails)"

    # Supercooling condition: g_D > y_psi / sqrt(2) (m_A' > m_psi)
    if g_D <= y_psi / np.sqrt(2.0):
        return False, f"g_D <= y_psi/sqrt(2) = {y_psi/np.sqrt(2.0):.4f} (supercooling fails)"

    return True, ""


def classify_point(result):
    """
    Classify a FOPT result point.

    Parameters
    ----------
    result : dict

    Returns
    -------
    str
        Status label: "viable", "physical_failure", "numerical_failure", "not_fopt"
    """
    if result is None:
        return "numerical_failure"

    # Check for NaN/Inf in key observables
    for key in ["alpha", "beta_H", "Tn", "Tp", "Treh"]:
        val = result.get(key, np.nan)
        if not np.isfinite(val):
            return "numerical_failure"

    # Check physical constraints
    if result.get("beta_lambda", 0) <= 0:
        return "physical_failure"
    if result.get("g_D", 0) <= result.get("y_psi", 0) / np.sqrt(2.0):
        return "physical_failure"

    # Check FOPT viability
    if result.get("alpha", 0) <= 0:
        return "not_fopt"
    if result.get("beta_H", 0) <= 0:
        return "not_fopt"
    if result.get("Tp", 0) <= 0:
        return "not_fopt"
    if result.get("Treh", 0) <= 0:
        return "not_fopt"

    # Eternal inflation check
    ei = result.get("eternal_inflation", np.nan)
    if ei is True or not np.isfinite(ei):
        return "physical_failure"

    return "viable"


def estimate_f_peak(result):
    """Get f_peak_est from result, return NaN if not available."""
    return result.get("f_peak_est", np.nan)


def run_scan(g_D_range, y_psi_range, v_range, n_g, n_y, n_v, scan_label=""):
    """
    Run a scan over the parameter grid.

    Parameters
    ----------
    g_D_range : tuple (min, max)
    y_psi_range : tuple (min, max)
    v_range : tuple (min, max)
    n_g : int
    n_y : int
    n_v : int
    scan_label : str

    Returns
    -------
    list of dict
        All scan results.
    """
    g_D_vals = np.linspace(g_D_range[0], g_D_range[1], n_g)
    y_psi_vals = np.linspace(y_psi_range[0], y_psi_range[1], n_y)
    v_vals = np.logspace(np.log10(v_range[0]), np.log10(v_range[1]), n_v)

    results = []
    total = len(g_D_vals) * len(y_psi_vals) * len(v_vals)
    count = 0

    print(f"\n{'='*60}")
    print(f"Scan {scan_label}: {n_g}x{n_y}x{n_v} = {total} points")
    print(f"  g_D: [{g_D_range[0]:.4f}, {g_D_range[1]:.4f}] ({n_g} steps)")
    print(f"  y_psi: [{y_psi_range[0]:.4f}, {y_psi_range[1]:.4f}] ({n_y} steps)")
    print(f"  v: [{v_range[0]:.6e}, {v_range[1]:.6e}] GeV ({n_v} log steps)")
    print(f"{'='*60}")

    for g_D in g_D_vals:
        for y_psi in y_psi_vals:
            for v in v_vals:
                count += 1

                # Physical guards before backend call
                passes, reason = physical_guards(g_D, y_psi, v)
                if not passes:
                    result = {
                        "g_D": g_D,
                        "y_psi": y_psi,
                        "v": v,
                        "alpha": np.nan,
                        "beta_H": np.nan,
                        "Tn": np.nan,
                        "Tp": np.nan,
                        "Treh": np.nan,
                        "f_peak_est": np.nan,
                        "eternal_inflation": np.nan,
                        "beta_lambda": np.nan,
                        "lambda_Phi": np.nan,
                        "m_Aprime": np.nan,
                        "m_psi": np.nan,
                        "m_chi": np.nan,
                        "gb_scalar": np.nan,
                        "status": "physical_failure",
                        "failure_reason": reason,
                    }
                    results.append(result)
                    continue

                # Compute with timeout
                try:
                    fopt_result = compute_with_timeout(g_D, y_psi, v, timeout_seconds=120)
                    status = classify_point(fopt_result)
                    fopt_result["status"] = status
                    fopt_result["failure_reason"] = "" if status == "viable" else status
                    results.append(fopt_result)
                except TimeoutError:
                    result = {
                        "g_D": g_D,
                        "y_psi": y_psi,
                        "v": v,
                        "alpha": np.nan,
                        "beta_H": np.nan,
                        "Tn": np.nan,
                        "Tp": np.nan,
                        "Treh": np.nan,
                        "f_peak_est": np.nan,
                        "eternal_inflation": np.nan,
                        "beta_lambda": np.nan,
                        "lambda_Phi": np.nan,
                        "m_Aprime": np.nan,
                        "m_psi": np.nan,
                        "m_chi": np.nan,
                        "gb_scalar": np.nan,
                        "status": "numerical_failure",
                        "failure_reason": "timeout",
                    }
                    results.append(result)
                except Exception as e:
                    result = {
                        "g_D": g_D,
                        "y_psi": y_psi,
                        "v": v,
                        "alpha": np.nan,
                        "beta_H": np.nan,
                        "Tn": np.nan,
                        "Tp": np.nan,
                        "Treh": np.nan,
                        "f_peak_est": np.nan,
                        "eternal_inflation": np.nan,
                        "beta_lambda": np.nan,
                        "lambda_Phi": np.nan,
                        "m_Aprime": np.nan,
                        "m_psi": np.nan,
                        "m_chi": np.nan,
                        "gb_scalar": np.nan,
                        "status": "numerical_failure",
                        "failure_reason": f"exception: {str(e)[:100]}",
                    }
                    results.append(result)

                if count % 20 == 0 or count == total:
                    viable_count = sum(1 for r in results if r.get("status") == "viable")
                    print(f"  Progress: {count}/{total} ({100*count/total:.1f}%), "
                          f"viable so far: {viable_count}")

    return results


def write_csv(results, filepath):
    """Write scan results to CSV."""
    fieldnames = [
        "g_D", "y_psi", "v",
        "alpha", "beta_H", "Tn", "Tp", "Treh",
        "f_peak_est", "eternal_inflation",
        "beta_lambda", "lambda_Phi", "m_Aprime", "m_psi", "m_chi", "gb_scalar",
        "status", "failure_reason",
    ]

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            row = {}
            for key in fieldnames:
                val = r.get(key, np.nan)
                if isinstance(val, (float, np.floating)):
                    if np.isfinite(val):
                        row[key] = f"{val:.8e}"
                    else:
                        row[key] = ""
                elif isinstance(val, (bool, np.bool_)):
                    row[key] = str(val)
                else:
                    row[key] = str(val) if val is not None else ""
            writer.writerow(row)

    print(f"Wrote {len(results)} rows to {filepath}")


def write_results_json(results, filepath):
    """Write scan results to JSON (only viable points with full data)."""
    viable = [r for r in results if r.get("status") == "viable"]

    output = {
        "model": "u1conformal_fermion",
        "agent": "fopt-agent",
        "total_points": len(results),
        "viable_points": len(viable),
        "failed_points": sum(1 for r in results if r.get("status") == "numerical_failure"),
        "excluded_points": sum(1 for r in results if r.get("status") in ("physical_failure", "not_fopt")),
        "viable": [],
    }

    for r in viable:
        entry = {}
        for key in ["g_D", "y_psi", "v", "alpha", "beta_H", "Tn", "Tp", "Treh",
                     "f_peak_est", "beta_lambda", "lambda_Phi", "m_Aprime", "m_psi", "m_chi"]:
            val = r.get(key, np.nan)
            if isinstance(val, (float, np.floating)):
                entry[key] = float(val) if np.isfinite(val) else None
            else:
                entry[key] = val
        output["viable"].append(entry)

    with open(filepath, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Wrote {len(viable)} viable points to {filepath}")


def summarize_results(results):
    """Print summary of scan results."""
    total = len(results)
    viable = [r for r in results if r.get("status") == "viable"]
    numerical_fail = [r for r in results if r.get("status") == "numerical_failure"]
    physical_fail = [r for r in results if r.get("status") == "physical_failure"]
    not_fopt = [r for r in results if r.get("status") == "not_fopt"]

    print(f"\n{'='*60}")
    print(f"SCAN SUMMARY")
    print(f"{'='*60}")
    print(f"  Total points:        {total}")
    print(f"  Viable:              {len(viable)}")
    print(f"  Numerical failures:  {len(numerical_fail)}")
    print(f"  Physical failures:   {len(physical_fail)}")
    print(f"  Not FOPT:            {len(not_fopt)}")

    if viable:
        # Find best points (in PTA band, sorted by proximity to PTA center)
        pta_center = np.sqrt(PTA_F_MIN * PTA_F_MAX)
        in_pta = [r for r in viable if PTA_F_MIN <= r.get("f_peak_est", 0) <= PTA_F_MAX]

        print(f"\n  Points in PTA band ({PTA_F_MIN:.0e}-{PTA_F_MAX:.0e} Hz): {len(in_pta)}")

        if in_pta:
            # Sort by proximity to PTA center
            in_pta_sorted = sorted(in_pta,
                                    key=lambda r: abs(np.log10(r.get("f_peak_est", 1)) - np.log10(pta_center)))
            print(f"\n  Top 5 PTA-band points (sorted by proximity to PTA center):")
            for i, r in enumerate(in_pta_sorted[:5]):
                print(f"    {i+1}. g_D={r['g_D']:.4f}, y_psi={r['y_psi']:.4f}, v={r['v']:.6e} GeV")
                print(f"       alpha={r['alpha']:.4e}, beta/H={r['beta_H']:.4f}")
                print(f"       Tp={r['Tp']:.6e} GeV, Treh={r['Treh']:.6e} GeV")
                print(f"       f_peak_est={r['f_peak_est']:.4e} Hz")

        # Also show best by alpha (strongest transition)
        viable_sorted = sorted(viable, key=lambda r: r.get("alpha", 0), reverse=True)
        print(f"\n  Top 3 by alpha (strongest transition):")
        for i, r in enumerate(viable_sorted[:3]):
            print(f"    {i+1}. g_D={r['g_D']:.4f}, y_psi={r['y_psi']:.4f}, v={r['v']:.6e} GeV")
            print(f"       alpha={r['alpha']:.4e}, beta/H={r['beta_H']:.4f}")
            print(f"       f_peak_est={r['f_peak_est']:.4e} Hz")

    print(f"{'='*60}\n")


def main():
    """Main scan routine with coarse-to-fine strategy."""
    output_dir = os.path.dirname(os.path.abspath(__file__))

    all_results = []
    scan_iteration = 0
    max_iterations = 5

    # Initial scan ranges based on literature benchmarks (Balan et al. 2502.19478)
    # g_D ~ 0.6-0.7, y_psi ~ 0.2-0.4, v ~ 100-700 MeV = 0.1-0.7 GeV
    # Start broader to explore the full viable region
    scan_configs = [
        # Scan 1: Broad initial scan around literature benchmarks
        {
            "g_D_range": (0.3, 1.5),
            "y_psi_range": (0.05, 0.5),
            "v_range": (0.01, 10.0),  # 10 MeV to 10 GeV
            "n_g": 8,
            "n_y": 6,
            "n_v": 10,
            "label": "Initial broad scan",
        },
        # Scan 2: Refined scan around viable region (if found)
        {
            "g_D_range": (0.4, 1.2),
            "y_psi_range": (0.05, 0.4),
            "v_range": (0.01, 1.0),  # 10 MeV to 1 GeV
            "n_g": 10,
            "n_y": 8,
            "n_v": 12,
            "label": "Refined scan - lower vev",
        },
        # Scan 3: Extended to higher couplings
        {
            "g_D_range": (0.3, 2.0),
            "y_psi_range": (0.01, 0.6),
            "v_range": (0.001, 1.0),  # 1 MeV to 1 GeV
            "n_g": 12,
            "n_y": 10,
            "n_v": 12,
            "label": "Extended scan - higher g_D, lower v",
        },
        # Scan 4: Very low vev for PTA band
        {
            "g_D_range": (0.3, 2.0),
            "y_psi_range": (0.01, 0.6),
            "v_range": (0.0001, 0.1),  # 0.1 MeV to 100 MeV
            "n_g": 12,
            "n_y": 10,
            "n_v": 10,
            "label": "Low vev scan for PTA",
        },
        # Scan 5: High vev scan
        {
            "g_D_range": (0.3, 2.0),
            "y_psi_range": (0.01, 0.6),
            "v_range": (1.0, 100.0),  # 1 GeV to 100 GeV
            "n_g": 8,
            "n_y": 6,
            "n_v": 8,
            "label": "High vev scan",
        },
    ]

    for config in scan_configs:
        scan_iteration += 1
        print(f"\n{'#'*60}")
        print(f"# SCAN ITERATION {scan_iteration}")
        print(f"{'#'*60}")

        results = run_scan(
            config["g_D_range"],
            config["y_psi_range"],
            config["v_range"],
            config["n_g"],
            config["n_y"],
            config["n_v"],
            scan_label=config["label"],
        )

        all_results.extend(results)
        summarize_results(results)

        # Check if we have viable points
        viable = [r for r in results if r.get("status") == "viable"]
        in_pta = [r for r in viable if PTA_F_MIN <= r.get("f_peak_est", 0) <= PTA_F_MAX]

        if in_pta:
            print(f"Found {len(in_pta)} points in PTA band. Continuing with refinement.")
        elif viable:
            print(f"Found {len(viable)} viable points but none in PTA band. "
                  f"Checking f_peak_est range...")
            f_peaks = [r.get("f_peak_est", np.nan) for r in viable if np.isfinite(r.get("f_peak_est", np.nan))]
            if f_peaks:
                print(f"  f_peak_est range: [{min(f_peaks):.4e}, {max(f_peaks):.4e}] Hz")
                if max(f_peaks) < PTA_F_MIN:
                    print("  All peaks below PTA band. Need higher vev/Treh.")
                elif min(f_peaks) > PTA_F_MAX:
                    print("  All peaks above PTA band. Need lower vev/Treh.")

    # Write final results
    csv_path = os.path.join(output_dir, "fopt_benchmarks.csv")
    write_csv(all_results, csv_path)

    json_path = os.path.join(output_dir, "fopt_results.json")
    write_results_json(all_results, json_path)

    # Final summary
    print(f"\n{'='*60}")
    print(f"FINAL SUMMARY")
    print(f"{'='*60}")
    summarize_results(all_results)

    return all_results


if __name__ == "__main__":
    all_results = main()
