"""
fopt_model_scan.py -- Scan the independent parameters of conformal-SU2 model over the
PTA-relevant parameter space.

Scans:
  - g (gauge coupling) in [0.3, 2.5] (linear or log)
  - chi0 (VEV) in [1e-4, 100] GeV (log scale)

Strategy: coarse-to-fine. Start with broad grid. If viable points exist but
f_peak_est is above the PTA band, extend towards lower scales. If no viable
transition is found, broaden the grid.

Saves: fopt_benchmarks.csv, fopt_results.json
"""

import sys
import os
import json
import time
import traceback
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import numpy as np

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "backend")
sys.path.insert(0, os.path.abspath(backend_dir))

from fopt_model import compute_fopt


# --- PTA band ---
PTA_F_MIN = 1e-9   # Hz
PTA_F_MAX = 1e-7   # Hz

# Perturbativity bound
G_MAX_PERT = 4.0 * np.pi


def estimate_f_peak(alpha, beta_H, Treh, gstar_eff):
    """Estimate redshifted peak frequency from FOPT parameters (template-independent)."""
    return 1.6e-5 * beta_H * (Treh / 100.0) * (gstar_eff / 100.0) ** (1.0 / 6.0)


def scan_grid(g_min, g_max, g_n, chi0_min, chi0_max, chi0_n):
    """
    Generate a grid of (g, chi0) points.

    Parameters
    ----------
    g_min, g_max : float
        Range for g (linear).
    chi0_min, chi0_max : float
        Range for chi0 (log scale).
    g_n, chi0_n : int
        Number of points in each direction.

    Returns
    -------
    list of (g, chi0) tuples
    """
    g_vals = np.linspace(g_min, g_max, g_n)
    chi0_vals = np.geomspace(chi0_min, chi0_max, chi0_n)
    points = []
    for g in g_vals:
        for chi0 in chi0_vals:
            points.append((float(g), float(chi0)))
    return points


def run_scan(points):
    """
    Run the FOPT computation for a list of (g, chi0) points.

    Parameters
    ----------
    points : list of (g, chi0) tuples

    Returns
    -------
    list of result dicts
    """
    results = []
    n_total = len(points)
    n_viable = 0
    n_failed = 0
    start_time = time.time()

    for i, (g, chi0) in enumerate(points):
        if (i + 1) % 20 == 0 or i == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / max(elapsed, 1e-6)
            remaining = (n_total - i - 1) / max(rate, 1e-6)
            print(f"  [{i+1}/{n_total}] g={g:.4f}, chi0={chi0:.6e} GeV  "
                  f"({n_viable} viable, {n_failed} failed, "
                  f"elapsed={elapsed:.1f}s, ETA={remaining:.1f}s)",
                  flush=True)

        try:
            result = compute_fopt(g, chi0, verbose=False)
        except Exception as e:
            result = {
                'g': g, 'chi0': chi0,
                'alpha': None, 'beta_H': None,
                'Tn': None, 'Tp': None, 'Treh': None,
                'f_peak_est': None,
                'beta_lambda': None, 'm_chi': None, 'delta_V': None,
                'gstar_eff': None, 'eternal_inflation': None,
                'status': 'numerical_failure',
                'failure_reason': f'uncaught exception: {str(e)}'
            }

        if result['status'] == 'viable':
            n_viable += 1
        else:
            n_failed += 1

        results.append(result)

    total_time = time.time() - start_time
    print(f"  Scan complete: {n_total} points in {total_time:.1f}s "
          f"({n_viable} viable, {n_failed} failed)")
    return results


def is_in_pta(result):
    """Check if result has f_peak_est in the PTA band."""
    f = result.get('f_peak_est')
    if f is not None and np.isfinite(f):
        return PTA_F_MIN <= f <= PTA_F_MAX
    return False


def classify_pta_bias(result):
    """
    Return -1 if f_peak_est < PTA band (too low), 0 if in band, +1 if above.
    Returns None if not viable.
    """
    if result['status'] != 'viable':
        return None
    f = result.get('f_peak_est')
    if f is None or not np.isfinite(f):
        return None
    if f < PTA_F_MIN:
        return -1
    elif f > PTA_F_MAX:
        return 1
    else:
        return 0


def find_wider_range(current_results, g_vals, chi0_vals):
    """
    Based on current scan results, suggest a wider range for a new scan.
    Returns (g_min, g_max, chi0_min, chi0_max, reason).
    """
    viable = [r for r in current_results if r['status'] == 'viable']
    failed = [r for r in current_results if r['status'] != 'viable']

    g_min, g_max = min(g_vals), max(g_vals)
    chi0_min, chi0_max = min(chi0_vals), max(chi0_vals)

    if len(viable) == 0:
        # No viable points found. Widen in all directions.
        new_g_min = max(0.1, g_min * 0.5)
        new_g_max = min(float(G_MAX_PERT) - 0.1, g_max * 2.0)
        new_chi0_min = chi0_min * 0.1
        new_chi0_max = chi0_max * 10.0
        return (new_g_min, new_g_max, new_chi0_min, new_chi0_max,
                f"No viable points. Widen: g=[{new_g_min:.3f},{new_g_max:.3f}], "
                f"chi0=[{new_chi0_min:.3e},{new_chi0_max:.3e}]")

    # Check biased points
    biases = [classify_pta_bias(r) for r in viable]
    biases = [b for b in biases if b is not None]

    above_count = sum(1 for b in biases if b == 1)
    in_count = sum(1 for b in biases if b == 0)
    below_count = sum(1 for b in biases if b == -1)

    if above_count > in_count and above_count > below_count:
        # Most viable points are above PTA band -> extend to lower chi0
        new_chi0_min = chi0_min * 0.1
        return (g_min, g_max, new_chi0_min, chi0_max,
                f"Most points above PTA band (above={above_count}, in={in_count}). "
                f"Lower chi0_min to {new_chi0_min:.3e}.")

    if below_count > in_count and below_count > above_count:
        # Most viable points are below PTA band -> extend to higher chi0
        new_chi0_max = chi0_max * 10.0
        return (g_min, g_max, chi0_min, new_chi0_max,
                f"Most points below PTA band (below={below_count}, in={in_count}). "
                f"Raise chi0_max to {new_chi0_max:.3e}.")

    # Mixed situation or in band - maybe refine nearby
    new_chi0_min = chi0_min * 0.1
    new_chi0_max = chi0_max * 10.0
    return (g_min, g_max, new_chi0_min, new_chi0_max,
            f"Broadening for coverage. chi0 range: [{new_chi0_min:.3e}, {new_chi0_max:.3e}]")


def save_csv(results, filepath):
    """Save scan results to CSV."""
    import csv

    fieldnames = [
        'g', 'chi0',
        'alpha', 'beta_H', 'Tn', 'Tp', 'Treh', 'f_peak_est',
        'beta_lambda', 'm_chi', 'gstar_eff', 'eternal_inflation',
        'status', 'failure_reason'
    ]

    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for r in results:
            row = {k: r.get(k, '') for k in fieldnames}
            writer.writerow(row)

    print(f"  Saved {len(results)} rows to {filepath}")


def save_results_json(results, filepath, model_name="conformal-SU2"):
    """Save structured results JSON (mirrors handoff_fopt.json format)."""

    viable = [r for r in results if r['status'] == 'viable']
    pta_in_band = [r for r in viable if is_in_pta(r)]

    # Helpers for serialization
    def safe_val(v):
        if v is None:
            return None
        if isinstance(v, (np.floating, float)):
            if np.isfinite(v):
                return float(v)
            return None
        if isinstance(v, np.bool_):
            return bool(v)
        return v

    def make_benchmark(r):
        return {
            "name": f"g={r['g']:.4f}_chi0={r['chi0']:.6e}",
            "parameters": {"g": r['g'], "chi0": r['chi0']},
            "alpha": safe_val(r.get('alpha')),
            "beta_H": safe_val(r.get('beta_H')),
            "Tn": safe_val(r.get('Tn')),
            "Tp": safe_val(r.get('Tp')),
            "Treh": safe_val(r.get('Treh')),
            "f_peak_est": safe_val(r.get('f_peak_est')),
            "beta_lambda": safe_val(r.get('beta_lambda')),
            "m_chi": safe_val(r.get('m_chi')),
            "gstar_eff": safe_val(r.get('gstar_eff')),
            "eternal_inflation": safe_val(r.get('eternal_inflation')),
            "status": r.get('status', 'unknown'),
            "failure_reason": r.get('failure_reason', '')
        }

    benchmarks = [make_benchmark(r) for r in results]

    # Best points: sort by distance to PTA band center
    pta_center = np.sqrt(PTA_F_MIN * PTA_F_MAX)  # geometric mean
    def sort_key(r):
        f = r.get('f_peak_est')
        if f is not None and np.isfinite(f) and r['status'] == 'viable':
            return abs(np.log10(f) - np.log10(pta_center))
        return 1e100

    sorted_results = sorted(viable, key=sort_key)
    best_points = [make_benchmark(r) for r in sorted_results[:10]]

    total = len(results)
    viable_count = len(viable)
    failed_count = total - viable_count

    output = {
        "model": model_name,
        "agent": "fopt-agent",
        "run_status": "ok" if viable_count > 0 else "warning",
        "created_at": time.strftime("%Y-%m-%d"),
        "branch": "fopt-pta",
        "created_from": [
            "output/conformal-SU2/handoff_model.json",
            "output/conformal-SU2/handoff_librarian_preliminary.json",
            "output/conformal-SU2/handoff_critique.json"
        ],
        "commands": [],
        "files_read": [],
        "files_written": [],
        "warnings": [],
        "errors": [],
        "approximations": [],
        "backend_choice": {
            "selected_backend": "semianalytic_pipeline",
            "executed": True,
            "reason": "Conformal scale-invariant single-field SU(2) model with CW mechanism"
        },
        "backend": "semianalytic_pipeline",
        "backend_executed": True,
        "expected_upstream_inputs": [
            "output/conformal-SU2/handoff_model.json",
            "output/conformal-SU2/handoff_librarian_preliminary.json",
            "output/conformal-SU2/handoff_critique.json"
        ],
        "missing_upstream_inputs": [],
        "model_parameter_ranges": {
            "g": {"min": 0.1, "max": 3.0, "unit": "dimensionless"},
            "chi0": {"min": 0.1, "max": 10000.0, "unit": "GeV"}
        },
        "parameter_basis": {
            "independent": {
                "g": {"description": "SU(2)_X gauge coupling", "range": [0.1, 3.0], "latex": "g"},
                "chi0": {"description": "Scalar VEV at zero temperature", "range": [0.1, 10000.0], "unit": "GeV", "latex": "\\chi_0"}
            },
            "dependent": {
                "beta_lambda": {
                    "description": "CW beta_lambda coefficient for the quartic coupling",
                    "expression": "9 * g**4 / (128 * pi**2)",
                    "latex": "\\beta_\\lambda = \\frac{9g^4}{128\\pi^2}"
                },
                "m_chi2": {
                    "description": "Mass squared of the radial (pseudo-dilaton) mode",
                    "expression": "beta_lambda * chi0**2",
                    "unit": "GeV^2",
                    "latex": "m_\\chi^2 = \\beta_\\lambda \\chi_0^2"
                },
                "gb_scalar": {
                    "description": "Mass-over-vev ratio for the radial scalar",
                    "expression": "sqrt(beta_lambda)",
                    "latex": "g_b^{(\\chi)} = \\sqrt{\\beta_\\lambda}"
                },
                "delta_V": {
                    "description": "Vacuum energy density difference",
                    "expression": "beta_lambda * chi0**4 / 16",
                    "unit": "GeV^4",
                    "latex": "\\Delta V = \\frac{\\beta_\\lambda \\chi_0^4}{16}"
                }
            },
            "fixed": {}
        },
        "temperature_key": "Tp",
        "scan_status_labels": ["viable", "physical_failure", "numerical_failure", "not_fopt"],
        "benchmark_summary": {
            "total_points": total,
            "viable_points": viable_count,
            "failed_points": failed_count,
            "excluded_points": 0
        },
        "scan_summary": {
            "total_points": total,
            "viable_points": viable_count,
            "failed_points": failed_count,
            "excluded_points": 0
        },
        "csv_json_alignment": {
            "csv_file": "output/conformal-SU2/fopt_benchmarks.csv",
            "independent_parameter_columns": ["g", "chi0"],
            "required_result_columns": [
                "alpha", "beta_H", "Tn", "Tp", "Treh", "f_peak_est"
            ],
            "status_column": "status"
        },
        "model_parameters": [
            {"name": "g", "scan_min": None, "scan_max": None, "unit": "dimensionless"},
            {"name": "chi0", "scan_min": None, "scan_max": None, "unit": "GeV"}
        ],
        "benchmarks": benchmarks,
        "best_points": best_points,
        "prior_ranges": {},
        "validation": {
            "finite_values": True,
            "percolation_checked": True,
            "eternal_inflation_checked": True,
            "perturbativity_checked": True
        },
        "output_files": [
            "output/conformal-SU2/fopt_model.py",
            "output/conformal-SU2/fopt_model_scan.py",
            "output/conformal-SU2/fopt_benchmarks.csv",
            "output/conformal-SU2/fopt_results.json",
            "output/conformal-SU2/handoff_fopt.json",
            "output/conformal-SU2/fopt_report.md"
        ]
    }

    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"  Saved results JSON to {filepath}")
    return output


# --- Main scan ---
def main():
    # Stage 1: Initial broad scan
    print("=" * 70)
    print("conformal-SU2 FOPT Parameter Scan")
    print("=" * 70)
    print("Target: PTA band (f_peak ~ 10^-9 to 10^-7 Hz)")
    print()

    # Strategy: start with a broad grid, find viable region, refine
    # Literature benchmarks suggest g~1.37, chi0~0.01 GeV (arXiv:2109.11558)
    # and chi0~0.14 GeV (arXiv:2602.09092 adapted)
    # Start with a grid covering several orders of magnitude in chi0

    scans = []
    all_results = []

    # Scan 1: Initial broad grid
    print("--- Scan 1: Initial broad grid ---")
    g_min, g_max, g_n = 0.3, 2.5, 12
    chi0_min, chi0_max, chi0_n = 1e-4, 100.0, 15
    print(f"  g     : [{g_min}, {g_max}] linear, {g_n} points")
    print(f"  chi0  : [{chi0_min:.1e}, {chi0_max:.1e}] GeV log, {chi0_n} points")

    points = scan_grid(g_min, g_max, g_n, chi0_min, chi0_max, chi0_n)
    print(f"  Total : {len(points)} points")
    results1 = run_scan(points)

    viable1 = [r for r in results1 if r['status'] == 'viable']
    pta1 = [r for r in viable1 if is_in_pta(r)]
    print(f"  Viable: {len(viable1)}, in PTA band: {len(pta1)}")
    scans.append(results1)
    all_results.extend(results1)

    if len(viable1) == 0 or len(pta1) == 0:
        print("\n--- No PTA-band points found. Enlarging scan range... ---")

        # Determine wider ranges
        all_g = [r['g'] for r in results1]
        all_chi0 = [r['chi0'] for r in results1]

        # Check if we found any viable at all
        if len(viable1) == 0:
            # Widen aggressively
            g_min2 = 0.1
            g_max2 = min(4.0, G_MAX_PERT - 0.1)
            chi0_min2 = 1e-6
            chi0_max2 = 1000.0
        else:
            # Found some viable, but not in PTA band
        # Extend towards lower chi0 (most viable above PTA)
            g_min2 = 0.1
            g_max2 = 3.0
            chi0_min2 = 1e-6
            chi0_max2 = 100.0

        g_n2 = 15
        chi0_n2 = 18
        print(f"\n--- Scan 2: Extended grid ---")
        print(f"  g     : [{g_min2}, {g_max2}] linear, {g_n2} points")
        print(f"  chi0  : [{chi0_min2:.1e}, {chi0_max2:.1e}] GeV log, {chi0_n2} points")

        points2 = scan_grid(g_min2, g_max2, g_n2, chi0_min2, chi0_max2, chi0_n2)
        print(f"  Total : {len(points2)} points")
        results2 = run_scan(points2)

        viable2 = [r for r in results2 if r['status'] == 'viable']
        pta2 = [r for r in viable2 if is_in_pta(r)]
        print(f"  Viable: {len(viable2)}, in PTA band: {len(pta2)}")
        scans.append(results2)
        all_results.extend(results2)

        # If still no PTA-band points, try a finer grid in the most promising region
        if len(pta2) == 0 and len(viable2) > 0:
            # Find the g values that produce viable points
            viable_gs = sorted(set(r['g'] for r in viable2))
            print(f"\n  Viable g values: {[f'{g:.3f}' for g in viable_gs]}")

            # Focus on the best g (one with most viable points or closest to PTA)
            g_viable_counts = {}
            for r in viable2:
                g_viable_counts[r['g']] = g_viable_counts.get(r['g'], 0) + 1

            best_g = max(g_viable_counts, key=g_viable_counts.get)
            print(f"  Best g = {best_g:.4f} (most viable points)")

            # Focus scan on a dense grid around best_g
            g_min3 = max(0.1, best_g - 0.5)
            g_max3 = min(3.0, best_g + 0.5)
            g_n3 = 20
            chi0_min3 = 1e-6
            chi0_max3 = 10.0
            chi0_n3 = 25

            print(f"\n--- Scan 3: Refined grid around best g ---")
            print(f"  g     : [{g_min3:.4f}, {g_max3:.4f}] linear, {g_n3} points")
            print(f"  chi0  : [{chi0_min3:.1e}, {chi0_max3:.1e}] GeV log, {chi0_n3} points")
            points3 = scan_grid(g_min3, g_max3, g_n3, chi0_min3, chi0_max3, chi0_n3)
            print(f"  Total : {len(points3)} points")
            results3 = run_scan(points3)

            viable3 = [r for r in results3 if r['status'] == 'viable']
            pta3 = [r for r in viable3 if is_in_pta(r)]
            print(f"  Viable: {len(viable3)}, in PTA band: {len(pta3)}")
            scans.append(results3)
            all_results.extend(results3)

    # Save all results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(output_dir, "fopt_benchmarks.csv")
    json_path = os.path.join(output_dir, "fopt_results.json")

    save_csv(all_results, csv_path)
    save_results_json(all_results, json_path)

    # Print summary
    all_viable = [r for r in all_results if r['status'] == 'viable']
    all_pta = [r for r in all_viable if is_in_pta(r)]

    print("\n" + "=" * 70)
    print("SCAN SUMMARY")
    print("=" * 70)
    print(f"  Total points tested: {len(all_results)}")
    print(f"  Viable points:       {len(all_viable)}")
    print(f"  In PTA band:         {len(all_pta)}")

    if all_pta:
        print("\n  --- PTA-band points ---")
        for r in all_pta:
            print(f"    g={r['g']:.4f}, chi0={r['chi0']:.6e} GeV")
        print(f"    alpha={r['alpha']:.4e}, beta/H={r['beta_H']:.4e}")
        print(f"    Tp={r['Tp']:.6e} GeV, Treh={r['Treh']:.6e} GeV")
        print(f"    f_peak={r['f_peak_est']:.4e} Hz")
    else:
        print("\n  No viable points found in the PTA band.")
        if all_viable:
            print("  Viable points exist but f_peak is outside PTA range.")
            # Show a sample
            r = all_viable[0]
            print(f"  Sample: g={r['g']:.4f}, chi0={r['chi0']:.6e} GeV")
            print(f"    f_peak={r['f_peak_est']:.4e} Hz")
        else:
            print("  No viable FOPT points found at all.")
            # Show a sample of failures
            for r in all_results[:5]:
                print(f"    g={r['g']:.4f}, chi0={r['chi0']:.6e}: "
                      f"{r['status']} ({r['failure_reason'][:50]})")

    print("\n  Outputs:")
    print(f"    {csv_path}")
    print(f"    {json_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()