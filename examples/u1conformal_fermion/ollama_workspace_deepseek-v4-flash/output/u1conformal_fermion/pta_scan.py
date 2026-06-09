"""
pta_scan.py -- Benchmark scan of the conformal U(1)_D model parameter space against PTA violins.

This script:
1. Scans the model parameter space (g_D, y_psi, v) on a coarse grid
2. For each point, computes FOPT parameters and the GW spectrum
3. Scores each point against the PTA violin windows
4. Refines around the best-scoring points
5. Saves results to pta_benchmark_scan.csv
"""

import sys
import os
import numpy as np
import csv
from pathlib import Path

# Add backend to path
_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Add output dir to path
_output_dir = os.path.dirname(os.path.abspath(__file__))
if _output_dir not in sys.path:
    sys.path.insert(0, _output_dir)

from fopt_model import compute_fopt, is_viable
from pta_spectrum import get_spectrum


def load_violin_windows(csv_path):
    """
    Load PTA violin windows from CSV.

    Returns
    -------
    dict
        Dictionary with keys: 'bin_i', 'f_nHz', 'log10_f_Hz', 'ymin', 'ymax'
    """
    windows = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            windows.append({
                'bin_i': int(row['bin_i']),
                'f_nHz': float(row['f_nHz']),
                'log10_f_Hz': float(row['log10_f_Hz']),
                'ymin': float(row['ymin_log10_h2OmegaGW']),
                'ymax': float(row['ymax_log10_h2OmegaGW']),
            })
    return windows


def score_spectrum(h2OmegaGW, log10_f, windows):
    """
    Score a spectrum against PTA violin windows.

    A point scores 1 for each frequency bin where the spectrum falls inside the violin.

    Parameters
    ----------
    h2OmegaGW : ndarray
        h^2 Omega_GW values at the evaluation frequencies.
    log10_f : ndarray
        log10(f/Hz) values.
    windows : list of dict
        Violin window definitions.

    Returns
    -------
    dict
        Score details: inside_bins, total_bins, score, bin_details
    """
    log10_h2OmegaGW = np.log10(np.maximum(h2OmegaGW, 1e-30))

    inside_bins = 0
    bin_details = []

    for w in windows:
        # Find the closest frequency in our spectrum array
        idx = np.argmin(np.abs(log10_f - w['log10_f_Hz']))
        spec_val = log10_h2OmegaGW[idx]

        is_inside = w['ymin'] <= spec_val <= w['ymax']
        if is_inside:
            inside_bins += 1

        bin_details.append({
            'bin_i': w['bin_i'],
            'log10_f_Hz': w['log10_f_Hz'],
            'ymin': w['ymin'],
            'ymax': w['ymax'],
            'spectrum_log10_h2OmegaGW': float(spec_val),
            'inside': is_inside,
        })

    return {
        'inside_bins': inside_bins,
        'total_bins': len(windows),
        'score': inside_bins / len(windows),
        'bin_details': bin_details,
    }


def scan_parameter_grid(g_D_vals, y_psi_vals, v_vals, template="dbf"):
    """
    Scan a grid of model parameters and score each point.

    Parameters
    ----------
    g_D_vals : array_like
        g_D values to scan.
    y_psi_vals : array_like
        y_psi values to scan.
    v_vals : array_like
        v values (GeV) to scan.
    template : str
        Spectrum template.

    Returns
    -------
    list of dict
        Scan results for each viable point.
    """
    # Load violin windows
    violin_csv = os.path.join(_backend_dir, "pta_violin_windows.csv")
    windows = load_violin_windows(violin_csv)

    # Frequency array for spectrum evaluation
    # Cover the PTA range with some margin
    f = np.logspace(-9.5, -6.5, 500)

    results = []

    total = len(g_D_vals) * len(y_psi_vals) * len(v_vals)
    count = 0

    for g_D in g_D_vals:
        for y_psi in y_psi_vals:
            for v in v_vals:
                count += 1
                if count % 50 == 0:
                    print(f"  Progress: {count}/{total}")

                # Check physical guards quickly
                beta_lambda = (3.0 * g_D**4 - 2.0 * y_psi**4) / (8.0 * np.pi**2)
                if beta_lambda <= 0:
                    continue
                if g_D <= y_psi / np.sqrt(2.0):
                    continue

                # Compute FOPT
                try:
                    fopt_result = compute_fopt(g_D, y_psi, v)
                except Exception:
                    continue

                if not is_viable(fopt_result):
                    continue

                # Compute spectrum
                try:
                    h2OmegaGW = get_spectrum(
                        f, fopt_result["Treh"], fopt_result["alpha"],
                        fopt_result["beta_H"], template=template
                    )
                except Exception:
                    continue

                # Score
                log10_f = np.log10(f)
                score_result = score_spectrum(h2OmegaGW, log10_f, windows)

                # Find peak
                peak_idx = np.argmax(h2OmegaGW)
                peak_f = f[peak_idx]
                peak_h2OmegaGW = h2OmegaGW[peak_idx]

                results.append({
                    'g_D': g_D,
                    'y_psi': y_psi,
                    'v': v,
                    'alpha': fopt_result["alpha"],
                    'beta_H': fopt_result["beta_H"],
                    'Tn': fopt_result["Tn"],
                    'Tp': fopt_result["Tp"],
                    'Treh': fopt_result["Treh"],
                    'f_peak_est': fopt_result["f_peak_est"],
                    'peak_f_Hz': peak_f,
                    'peak_h2OmegaGW': peak_h2OmegaGW,
                    'inside_bins': score_result['inside_bins'],
                    'total_bins': score_result['total_bins'],
                    'score': score_result['score'],
                    'template': template,
                })

    return results


def save_results(results, output_path):
    """Save scan results to CSV."""
    if not results:
        print("No results to save.")
        return

    fieldnames = [
        'g_D', 'y_psi', 'v', 'alpha', 'beta_H', 'Tn', 'Tp', 'Treh',
        'f_peak_est', 'peak_f_Hz', 'peak_h2OmegaGW',
        'inside_bins', 'total_bins', 'score', 'template'
    ]

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    print(f"Saved {len(results)} results to {output_path}")


def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv = os.path.join(output_dir, "pta_benchmark_scan.csv")

    print("=" * 60)
    print("PTA Benchmark Scan for Conformal U(1)_D Dark Sector")
    print("=" * 60)

    # ============================================================
    # Coarse scan 1: Wide range based on FOPT f_peak_est
    # ============================================================
    print("\n--- Coarse Scan 1: Wide parameter range ---")

    # From FOPT results: f_peak_est ~ 1e-8 Hz for v ~ 0.01-0.02 GeV
    # The PTA band is ~ 2-30 nHz = 2e-9 to 3e-8 Hz
    # So we need v around 0.001-0.1 GeV to get the peak in the PTA band
    # g_D ~ 0.3-2.0, y_psi ~ 0.05-0.6

    g_D_coarse = np.linspace(0.3, 2.0, 8)
    y_psi_coarse = np.linspace(0.05, 0.6, 8)
    v_coarse = np.logspace(-3.0, 0.0, 10)  # 0.001 to 1 GeV

    print(f"  g_D: {g_D_coarse}")
    print(f"  y_psi: {y_psi_coarse}")
    print(f"  v (GeV): {v_coarse}")
    print(f"  Total points: {len(g_D_coarse) * len(y_psi_coarse) * len(v_coarse)}")

    results1 = scan_parameter_grid(g_D_coarse, y_psi_coarse, v_coarse, template="dbf")

    # Sort by score descending
    results1.sort(key=lambda r: r['score'], reverse=True)

    print(f"\n  Viable points: {len(results1)}")
    if results1:
        print(f"  Best score: {results1[0]['score']} ({results1[0]['inside_bins']}/{results1[0]['total_bins']})")
        print(f"  Best point: g_D={results1[0]['g_D']:.4f}, y_psi={results1[0]['y_psi']:.4f}, v={results1[0]['v']:.6f} GeV")
        print(f"  Best alpha={results1[0]['alpha']:.2f}, beta_H={results1[0]['beta_H']:.2f}")

    # ============================================================
    # Refined scan around best points
    # ============================================================
    print("\n--- Refined Scan 2: Finer grid around best region ---")

    # Based on coarse scan results, refine around the best region
    # The best points from the FOPT handoff have g_D ~ 0.64-0.92, y_psi ~ 0.23-0.6, v ~ 0.003-0.02
    # Let's scan a finer grid

    g_D_fine = np.linspace(0.4, 1.5, 12)
    y_psi_fine = np.linspace(0.1, 0.6, 11)
    v_fine = np.logspace(-3.0, -1.0, 12)  # 0.001 to 0.1 GeV

    print(f"  g_D: {g_D_fine}")
    print(f"  y_psi: {y_psi_fine}")
    print(f"  v (GeV): {v_fine}")
    print(f"  Total points: {len(g_D_fine) * len(y_psi_fine) * len(v_fine)}")

    results2 = scan_parameter_grid(g_D_fine, y_psi_fine, v_fine, template="dbf")

    results2.sort(key=lambda r: r['score'], reverse=True)

    print(f"\n  Viable points: {len(results2)}")
    if results2:
        print(f"  Best score: {results2[0]['score']} ({results2[0]['inside_bins']}/{results2[0]['total_bins']})")
        print(f"  Best point: g_D={results2[0]['g_D']:.4f}, y_psi={results2[0]['y_psi']:.4f}, v={results2[0]['v']:.6f} GeV")
        print(f"  Best alpha={results2[0]['alpha']:.2f}, beta_H={results2[0]['beta_H']:.2f}")

    # ============================================================
    # Ultra-fine scan around the very best region
    # ============================================================
    print("\n--- Ultra-fine Scan 3: Tight grid around best points ---")

    # If we have good candidates, zoom in further
    if results2:
        best_g_D = results2[0]['g_D']
        best_y_psi = results2[0]['y_psi']
        best_v = results2[0]['v']

        g_D_ultra = np.linspace(max(0.3, best_g_D - 0.3), min(2.0, best_g_D + 0.3), 10)
        y_psi_ultra = np.linspace(max(0.05, best_y_psi - 0.15), min(0.6, best_y_psi + 0.15), 10)
        v_ultra = np.logspace(np.log10(best_v) - 0.5, np.log10(best_v) + 0.5, 10)

        print(f"  g_D: {g_D_ultra}")
        print(f"  y_psi: {y_psi_ultra}")
        print(f"  v (GeV): {v_ultra}")
        print(f"  Total points: {len(g_D_ultra) * len(y_psi_ultra) * len(v_ultra)}")

        results3 = scan_parameter_grid(g_D_ultra, y_psi_ultra, v_ultra, template="dbf")

        results3.sort(key=lambda r: r['score'], reverse=True)

        print(f"\n  Viable points: {len(results3)}")
        if results3:
            print(f"  Best score: {results3[0]['score']} ({results3[0]['inside_bins']}/{results3[0]['total_bins']})")
            print(f"  Best point: g_D={results3[0]['g_D']:.4f}, y_psi={results3[0]['y_psi']:.4f}, v={results3[0]['v']:.6f} GeV")
            print(f"  Best alpha={results3[0]['alpha']:.2f}, beta_H={results3[0]['beta_H']:.2f}")

    # ============================================================
    # Check boundary: if best point is at edge, expand
    # ============================================================
    all_results = results1 + results2 + results3
    all_results.sort(key=lambda r: r['score'], reverse=True)

    # Check if best point touches any boundary
    boundary_expansions = []
    if all_results:
        best = all_results[0]
        g_D_range = [min(r['g_D'] for r in all_results), max(r['g_D'] for r in all_results)]
        y_psi_range = [min(r['y_psi'] for r in all_results), max(r['y_psi'] for r in all_results)]
        v_range = [min(r['v'] for r in all_results), max(r['v'] for r in all_results)]

        print(f"\n--- Boundary Check ---")
        print(f"  g_D range: [{g_D_range[0]:.4f}, {g_D_range[1]:.4f}], best: {best['g_D']:.4f}")
        print(f"  y_psi range: [{y_psi_range[0]:.4f}, {y_psi_range[1]:.4f}], best: {best['y_psi']:.4f}")
        print(f"  v range: [{v_range[0]:.6f}, {v_range[1]:.6f}], best: {best['v']:.6f}")

        # Check if best point is near any scan boundary
        near_boundary = False
        if best['g_D'] <= g_D_range[0] * 1.05 or best['g_D'] >= g_D_range[1] * 0.95:
            print(f"  WARNING: g_D near boundary!")
            near_boundary = True
        if best['y_psi'] <= y_psi_range[0] * 1.05 or best['y_psi'] >= y_psi_range[1] * 0.95:
            print(f"  WARNING: y_psi near boundary!")
            near_boundary = True
        if best['v'] <= v_range[0] * 1.05 or best['v'] >= v_range[1] * 0.95:
            print(f"  WARNING: v near boundary!")
            near_boundary = True

        if near_boundary:
            print("  Expanding scan range...")
            # Expand and rescan
            g_D_exp = np.linspace(0.2, 2.5, 12)
            y_psi_exp = np.linspace(0.01, 0.7, 12)
            v_exp = np.logspace(-4.0, 0.0, 12)

            results_exp = scan_parameter_grid(g_D_exp, y_psi_exp, v_exp, template="dbf")
            all_results.extend(results_exp)
            all_results.sort(key=lambda r: r['score'], reverse=True)
            boundary_expansions.append("Expanded to g_D=[0.2,2.5], y_psi=[0.01,0.7], v=[1e-4,1]")

    # ============================================================
    # Save all results
    # ============================================================
    save_results(all_results, output_csv)

    # Print top 10 results
    print("\n--- Top 10 Results ---")
    print(f"{'Rank':<5} {'g_D':<8} {'y_psi':<8} {'v(GeV)':<12} {'alpha':<10} {'beta_H':<8} {'Score':<8} {'Bins':<8}")
    print("-" * 70)
    for i, r in enumerate(all_results[:10]):
        print(f"{i+1:<5} {r['g_D']:<8.4f} {r['y_psi']:<8.4f} {r['v']:<12.6f} {r['alpha']:<10.2f} {r['beta_H']:<8.2f} {r['score']:<8.3f} {r['inside_bins']}/{r['total_bins']}")

    print("\nDone!")


if __name__ == "__main__":
    main()
