"""
fopt_model_refine_scan.py -- Refined scan focusing on the PTA-band region.

Based on initial scan results, the PTA-band region is:
  g in [0.9, 2.3]
  chi0 in [2e-5, 0.3] GeV

This script runs a denser grid in this region.
"""

import sys
import os
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import numpy as np

backend_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "backend")
sys.path.insert(0, os.path.abspath(backend_dir))

from fopt_model import compute_fopt

PTA_F_MIN = 1e-9
PTA_F_MAX = 1e-7


def estimate_f_peak(alpha, beta_H, Treh, gstar_eff):
    return 1.6e-5 * beta_H * (Treh / 100.0) * (gstar_eff / 100.0) ** (1.0 / 6.0)


def is_in_pta(result):
    f = result.get('f_peak_est')
    if f is not None and np.isfinite(f):
        return PTA_F_MIN <= f <= PTA_F_MAX
    return False


# Dense grid in PTA-relevant region
g_min, g_max, g_n = 0.7, 2.3, 20
chi0_min, chi0_max, chi0_n = 3e-5, 0.5, 25

print(f"Refined scan: g=[{g_min}, {g_max}] ({g_n}), chi0=[{chi0_min:.1e}, {chi0_max}] ({chi0_n})")

g_vals = np.linspace(g_min, g_max, g_n)
chi0_vals = np.geomspace(chi0_min, chi0_max, chi0_n)

results = []
n_total = len(g_vals) * len(chi0_vals)
n_viable = 0
n_pta = 0

for i, g in enumerate(g_vals):
    for j, chi0 in enumerate(chi0_vals):
        idx = i * len(chi0_vals) + j + 1
        if idx % 50 == 0 or idx == 1:
            print(f"  [{idx}/{n_total}] g={g:.3f}, chi0={chi0:.6e} ({n_viable} viable, {n_pta} PTA)")

        try:
            result = compute_fopt(float(g), float(chi0), verbose=False)
        except Exception as e:
            result = {
                'g': float(g), 'chi0': float(chi0),
                'alpha': None, 'beta_H': None,
                'Tn': None, 'Tp': None, 'Treh': None,
                'f_peak_est': None,
                'beta_lambda': None, 'm_chi': None, 'delta_V': None,
                'gstar_eff': None, 'eternal_inflation': None,
                'status': 'numerical_failure',
                'failure_reason': f'exception: {str(e)}'
            }

        if result['status'] == 'viable':
            n_viable += 1
            if is_in_pta(result):
                n_pta += 1

        results.append(result)

import csv
output_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(output_dir, "fopt_refine_benchmarks.csv")

fieldnames = [
    'g', 'chi0', 'alpha', 'beta_H', 'Tn', 'Tp', 'Treh', 'f_peak_est',
    'beta_lambda', 'm_chi', 'gstar_eff', 'eternal_inflation',
    'status', 'failure_reason'
]
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for r in results:
        row = {k: r.get(k, '') for k in fieldnames}
        writer.writerow(row)

print(f"\nDONE: {n_total} points, {n_viable} viable, {n_pta} in PTA band")
print(f"Saved to {csv_path}")

# Print PTA-band points sorted by f_peak
pta_results = [r for r in results if is_in_pta(r)]
pta_results.sort(key=lambda r: r['f_peak_est'])

print("\n=== PTA-band points (sorted by f_peak) ===")
print(f"{'g':>8s}  {'chi0(GeV)':>12s}  {'alpha':>10s}  {'beta/H':>10s}  "
      f"{'Tp(GeV)':>12s}  {'Treh(GeV)':>12s}  {'f_peak(Hz)':>12s}")
print("-" * 90)
for r in pta_results:
    print(f"{r['g']:>8.4f}  {r['chi0']:>12.6e}  {r['alpha']:>10.4e}  {r['beta_H']:>10.4e}  "
          f"{r['Tp']:>12.6e}  {r['Treh']:>12.6e}  {r['f_peak_est']:>12.6e}")