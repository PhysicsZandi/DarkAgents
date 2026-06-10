"""
PTA benchmark scan for the Dark U(1)_D conformal model.

Scans the independent model parameters (v, g_D) in the PTA-relevant region,
computes the GW spectrum using the FOPT model and the selected spectrum template,
and scores each point against the PTA violin windows from backend/pta_violin_windows.csv.

Usage:
    conda run -n ptarcade python3 output/u1conformal/pta_scan.py
"""
import sys
import os
import numpy as np
import csv
from pathlib import Path

# Add paths
_backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Import the FOPT model and spectrum
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fopt_model import compute_fopt
from pta_spectrum import get_spectrum

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load PTA violin windows
violin_file = os.path.join(_backend_dir, "pta_violin_windows.csv")
with open(violin_file, "r") as f:
    raw = f.read().strip().split("\n")
header = raw[0].split(",")
# Parse each row, ignoring trailing empty fields
violin_rows = []
for line in raw[1:]:
    parts = line.strip().split(",")
    # Take only first 5 fields (index from 0)
    vals = [float(p) if p.strip() else float("nan") for p in parts[:5]]
    violin_rows.append(vals)
violin_data = np.array(violin_rows)
violin_bins = int(violin_data.shape[0])  # 14 bins
violin_freq = violin_data[:, 2]  # log10(f/Hz)
violin_ymin = violin_data[:, 3]  # log10(h^2 Omega_GW) min
violin_ymax = violin_data[:, 4]  # log10(h^2 Omega_GW) max
violin_freq_Hz = 10.0 ** violin_freq  # Convert to Hz

print(f"Loaded {violin_bins} PTA violin bins")
print(f"Frequency range: log10(f/Hz) in [{violin_freq[0]:.3f}, {violin_freq[-1]:.3f}]")


def score_point(h2OmegaGW):
    """
    Score a point by counting how many frequency bins fall inside the PTA violin windows.

    Parameters
    ----------
    h2OmegaGW : ndarray
        Spectrum values at the 14 PTA frequency bins.

    Returns
    -------
    int
        Number of bins where the spectrum is inside the violin window.
    """
    log_spectrum = np.log10(h2OmegaGW)
    score = 0
    inside = []
    for i in range(violin_bins):
        if violin_ymin[i] <= log_spectrum[i] <= violin_ymax[i]:
            score += 1
            inside.append(True)
        else:
            inside.append(False)
    return score, inside


def run_scan(v_values, gD_values, scan_stage=""):
    """
    Run a full scan over v and g_D values.

    Parameters
    ----------
    v_values : array-like
        v values in GeV
    gD_values : array-like
        g_D values (dimensionless)
    scan_stage : str
        Label for the scan stage

    Returns
    -------
    list
        List of result dicts
    """
    results = []
    total = len(v_values) * len(gD_values)
    count = 0

    for v in v_values:
        for gD in gD_values:
            count += 1
            if count % 20 == 0:
                print(f"  [{scan_stage}] Point {count}/{total}...", flush=True)

            # Compute FOPT parameters
            fopt_result = compute_fopt(v, gD)

            if fopt_result["status"] != "viable":
                results.append({
                    "v": v,
                    "g_D": gD,
                    "status": fopt_result["status"],
                    "failure_reason": fopt_result.get("failure_reason", ""),
                    "alpha": np.nan,
                    "beta_H": np.nan,
                    "Tr": np.nan,
                    "score": 0,
                    "inside_bins": 0,
                    "f_peak_est": np.nan,
                })
                continue

            alpha = fopt_result["alpha"]
            beta_H = fopt_result["beta_H"]
            Tr = fopt_result["Tr"]
            f_peak_est = fopt_result["f_peak_est"]

            # Check if FOPT results are valid
            if not (np.isfinite(alpha) and np.isfinite(beta_H) and np.isfinite(Tr)
                    and alpha > 0 and beta_H > 0 and Tr > 0):
                results.append({
                    "v": v,
                    "g_D": gD,
                    "status": "numerical_failure",
                    "failure_reason": "non-finite FOPT params",
                    "alpha": alpha,
                    "beta_H": beta_H,
                    "Tr": Tr,
                    "score": 0,
                    "inside_bins": 0,
                    "f_peak_est": f_peak_est,
                })
                continue

            # Compute spectrum at PTA frequencies
            try:
                h2OmegaGW = get_spectrum(violin_freq_Hz, Tr, alpha, beta_H)
            except Exception as e:
                results.append({
                    "v": v,
                    "g_D": gD,
                    "status": "numerical_failure",
                    "failure_reason": f"spectrum failed: {e}",
                    "alpha": alpha,
                    "beta_H": beta_H,
                    "Tr": Tr,
                    "score": 0,
                    "inside_bins": 0,
                    "f_peak_est": f_peak_est,
                })
                continue

            if not np.all(np.isfinite(h2OmegaGW)):
                results.append({
                    "v": v,
                    "g_D": gD,
                    "status": "numerical_failure",
                    "failure_reason": "non-finite spectrum",
                    "alpha": alpha,
                    "beta_H": beta_H,
                    "Tr": Tr,
                    "score": 0,
                    "inside_bins": 0,
                    "f_peak_est": f_peak_est,
                })
                continue

            score, inside = score_point(h2OmegaGW)

            results.append({
                "v": v,
                "g_D": gD,
                "status": "viable",
                "failure_reason": "",
                "alpha": alpha,
                "beta_H": beta_H,
                "Tr": Tr,
                "score": score,
                "inside_bins": sum(inside),
                "f_peak_est": f_peak_est,
                "log10_h2Omega_bins": [float(np.log10(h)) for h in h2OmegaGW],
            })

    return results


def save_results(results, filename):
    """Save scan results to CSV."""
    csv_path = os.path.join(OUTPUT_DIR, filename)
    fieldnames = [
        "v", "g_D", "status", "failure_reason",
        "alpha", "beta_H", "Tr",
        "score", "inside_bins", "f_peak_est",
    ]
    # Add per-bin columns
    for i in range(violin_bins):
        fieldnames.append(f"log10_h2Omega_bin{i+1}")

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = {
                "v": f"{r['v']:.6e}",
                "g_D": f"{r['g_D']:.6e}",
                "status": r["status"],
                "failure_reason": r["failure_reason"],
                "alpha": f"{r['alpha']:.6e}" if np.isfinite(r.get("alpha", np.nan)) else "",
                "beta_H": f"{r['beta_H']:.6e}" if np.isfinite(r.get("beta_H", np.nan)) else "",
                "Tr": f"{r['Tr']:.6e}" if np.isfinite(r.get("Tr", np.nan)) else "",
                "score": r["score"],
                "inside_bins": r["inside_bins"],
                "f_peak_est": f"{r['f_peak_est']:.6e}" if np.isfinite(r.get("f_peak_est", np.nan)) else "",
            }
            # Add per-bin spectrum values
            log10_bins = r.get("log10_h2Omega_bins", [""] * violin_bins)
            for i in range(violin_bins):
                val = log10_bins[i] if i < len(log10_bins) else ""
                row[f"log10_h2Omega_bin{i+1}"] = f"{val:.6e}" if val != "" else ""

            writer.writerow(row)

    print(f"Saved {len(results)} results to {csv_path}")
    return csv_path


def print_summary(results, top_n=20):
    """Print summary of best-scoring points."""
    viable = [r for r in results if r["status"] == "viable" and r["score"] > 0]
    viable.sort(key=lambda r: (-r["score"], r.get("alpha", np.nan)))

    print(f"\nTotal points: {len(results)}")
    print(f"Viable with score>0: {len(viable)}")
    print(f"\nTop {min(top_n, len(viable))} points:")
    print(f"{'Rank':<5} {'v (GeV)':<12} {'g_D':<8} {'score':<7} {'alpha':<12} {'beta_H':<10} {'Tr (GeV)':<12} {'f_peak (Hz)':<14}")
    print("-" * 80)

    for i, r in enumerate(viable[:top_n]):
        print(f"{i+1:<5} {r['v']:<12.6e} {r['g_D']:<8.4f} {r['score']:<7} {r['alpha']:<12.3e} {r['beta_H']:<10.3f} {r['Tr']:<12.6e} {r.get('f_peak_est', np.nan):<14.3e}")


def find_diverse_points(results, n=4):
    """Find n maximally different points among those with maximum score."""
    max_score = max(r["score"] for r in results if r["status"] == "viable")
    best = [r for r in results if r["status"] == "viable" and r["score"] == max_score]

    if len(best) <= n:
        return best

    # Find maximally different points in (v, g_D) space
    selected = [best[0]]
    remaining = best[1:]

    while len(selected) < n and remaining:
        # Find point with max minimum distance to selected points
        max_min_dist = -1
        best_idx = 0
        for i, r in enumerate(remaining):
            log_v = np.log10(r["v"])
            log_v_sel = np.log10([s["v"] for s in selected])
            gD_sel = [s["g_D"] for s in selected]
            min_dist = min(np.sqrt((log_v - lv)**2 + (r["g_D"] - gd)**2)
                          for lv, gd in zip(log_v_sel, gD_sel))
            if min_dist > max_min_dist:
                max_min_dist = min_dist
                best_idx = i

        selected.append(remaining.pop(best_idx))

    return selected


if __name__ == "__main__":
    print("=" * 60)
    print("PTA Benchmark Scan for U(1)_D Conformal Model")
    print("=" * 60)

    # Stage 1: Coarse scan over the PTA-relevant region
    # Based on FOPT results, the PTA-relevant region covers:
    # v: ~0.005 to 10 GeV, g_D: ~0.49 to 1.3
    # But many points with small v and low g_D fail numerically.
    # Let's start with a wide range and refine.

    print("\n--- Stage 1: Coarse scan ---")
    v_coarse = np.logspace(np.log10(0.005), np.log10(10.0), 30)
    gD_coarse = np.linspace(0.49, 1.3, 20)

    results_1 = run_scan(v_coarse, gD_coarse, scan_stage="Stage1")
    save_results(results_1, "pta_benchmark_scan.csv")
    print_summary(results_1)

    # Stage 2: Refine around the best region
    print("\n--- Stage 2: Fine scan around best region ---")
    best_viable = [r for r in results_1 if r["status"] == "viable" and r["score"] > 0]
    if best_viable:
        best_viable.sort(key=lambda r: -r["score"])
        top_scores = [r["score"] for r in best_viable[:10]]
        print(f"Top scores: {top_scores}")

        # Check if best points are at boundaries
        best_v = best_viable[0]["v"]
        best_gD = best_viable[0]["g_D"]

        v_min_scan = min(v_coarse)
        v_max_scan = max(v_coarse)
        gD_min_scan = min(gD_coarse)
        gD_max_scan = max(gD_coarse)

        v_min_new = v_min_scan
        v_max_new = v_max_scan
        gD_min_new = gD_min_scan
        gD_max_new = gD_max_scan

        boundary_expanded = False

        if abs(best_v - v_min_scan) / v_min_scan < 0.1:
            v_min_new = v_min_scan / 5
            boundary_expanded = True
            print(f"  Best v near lower boundary, expanding to {v_min_new}")
        if abs(best_v - v_max_scan) / v_max_scan < 0.1:
            v_max_new = v_max_scan * 5
            boundary_expanded = True
            print(f"  Best v near upper boundary, expanding to {v_max_new}")
        if abs(best_gD - gD_min_scan) / gD_min_scan < 0.1:
            gD_min_new = max(0.3, gD_min_scan - 0.15)
            boundary_expanded = True
            print(f"  Best g_D near lower boundary, expanding to {gD_min_new}")
        if abs(best_gD - gD_max_scan) / gD_max_scan < 0.1:
            gD_max_new = min(1.5, gD_max_scan + 0.15)
            boundary_expanded = True
            print(f"  Best g_D near upper boundary, expanding to {gD_max_new}")

        # Narrow the scan range around the best region
        # Find the range of v and g_D that give high scores
        # Define threshold before using it
        max_score_threshold = max(r["score"] for r in best_viable)
        high_score = [r for r in best_viable if r["score"] >= max_score_threshold]

        # Use all viable points to determine scan range
        v_vals = np.array([r["v"] for r in best_viable])
        gD_vals = np.array([r["g_D"] for r in best_viable])
        scores = np.array([r["score"] for r in best_viable])

        # Get score-weighted center
        if len(best_viable) > 5:
            score_weighted_v_center = np.average(np.log10(v_vals), weights=scores)
            score_weighted_gD_center = np.average(gD_vals, weights=scores)
        else:
            score_weighted_v_center = np.log10(best_viable[0]["v"])
            score_weighted_gD_center = best_viable[0]["g_D"]

        v_center = 10**score_weighted_v_center
        gD_center = score_weighted_gD_center

        # Fine scan: 3 orders of magnitude in v around center, wider range in g_D
        v_fine = np.logspace(np.log10(v_center) - 1.5, np.log10(v_center) + 1.5, 40)
        gD_fine = np.linspace(max(0.4, gD_center - 0.3), min(1.3, gD_center + 0.3), 25)

        # Apply boundary expansion
        if boundary_expanded:
            v_min_fine = min(v_min_new, min(v_fine))
            v_max_fine = max(v_max_new, max(v_fine))
            gD_min_fine = max(0.3, min(gD_min_new, min(gD_fine)))
            gD_max_fine = min(1.5, max(gD_max_new, max(gD_fine)))
            v_fine = np.logspace(np.log10(v_min_fine), np.log10(v_max_fine), 40)
            gD_fine = np.linspace(gD_min_fine, gD_max_fine, 25)

        results_2 = run_scan(v_fine, gD_fine, scan_stage="Stage2")
        # Append to the same CSV
        all_results = results_1 + results_2
        save_results(all_results, "pta_benchmark_scan.csv")
        print_summary(all_results)

        # Check if any points achieved 14/14
        max_score_final = max(r["score"] for r in all_results if r["status"] == "viable")
        print(f"\nMaximum score achieved: {max_score_final}/{violin_bins}")

        if max_score_final < violin_bins:
            print(f"WARNING: No point achieved {violin_bins}/{violin_bins}. Best: {max_score_final}/{violin_bins}")

        # Select diverse best points
        diverse_points = find_diverse_points(all_results, n=4)
        print(f"\nSelected {len(diverse_points)} diverse best points for plotting:")
        for i, p in enumerate(diverse_points):
            print(f"  Point {i+1}: v={p['v']:.6e} GeV, g_D={p['g_D']:.4f}, score={p['score']}/{violin_bins}")
    else:
        print("No viable points found!")
        diverse_points = []

    print("\nPTA benchmark scan complete.")