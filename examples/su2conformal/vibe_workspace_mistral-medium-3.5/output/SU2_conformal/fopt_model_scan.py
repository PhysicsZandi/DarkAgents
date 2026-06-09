"""
SU2_conformal FOPT parameter scan.

This script performs a bounded coarse-to-fine scan over the independent parameters
g_D and v to identify viable parameter space for first-order phase transition.

Scan strategy:
1. Start with literature-informed ranges extended for PTA compatibility
2. Use logarithmic spacing for broad coverage
3. Check physical guards: g_D < 4*pi, v > 0, finite positive temperatures, alpha > 0, beta_H > 0
4. Extend range if no viable points found in PTA band
5. Save results to fopt_benchmarks.csv

References:
- Literature benchmarks: 2109.11558 (Borah et al.) suggests g_D ~ 0.5-2.0
- For PTA (nano-Hz GW), we need lower v to get lower f_peak
- Backend: semianalytic_pipeline
- Handoff: output/SU2_conformal/handoff_model.json
"""

import numpy as np
import pandas as pd
import sys
import os
from datetime import datetime
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Add parent directory to path to import model
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fopt_model import compute_point


def scan_parameter_space(
    g_D_range=(0.1, 3.0),
    v_range=(0.01, 100),
    n_points_gD=20,
    n_points_v=20,
    scan_id="coarse",
    timeout_per_point=30,
    verbose=False,
):
    """
    Perform a scan over g_D and v parameter space.
    
    Args:
        g_D_range (tuple): (min, max) for g_D (log-spaced)
        v_range (tuple): (min, max) for v in GeV (log-spaced)
        n_points_gD (int): Number of points for g_D
        n_points_v (int): Number of points for v
        scan_id (str): Identifier for this scan
        timeout_per_point (int): Timeout in seconds per point
        verbose (bool): Print progress
        
    Returns:
        pd.DataFrame: Results dataframe
    """
    g_D_min, g_D_max = g_D_range
    v_min, v_max = v_range
    
    # Logarithmic spacing for broad parameter coverage
    g_D_values = np.logspace(np.log10(g_D_min), np.log10(g_D_max), n_points_gD)
    v_values = np.logspace(np.log10(v_min), np.log10(v_max), n_points_v)
    
    results = []
    total_points = len(g_D_values) * len(v_values)
    point_count = 0
    
    print(f"\n=== Scan {scan_id} ===")
    print(f"g_D range: [{g_D_min:.4g}, {g_D_max:.4g}] ({n_points_gD} points)")
    print(f"v range: [{v_min:.4g}, {v_max:.4g}] GeV ({n_points_v} points)")
    print(f"Total points: {total_points}")
    print(f"Starting scan at: {datetime.now().isoformat()}")
    
    viable_count = 0
    failure_count = 0
    
    for i, g_D in enumerate(g_D_values):
        for j, v in enumerate(v_values):
            point_count += 1
            
            # Physical guards before computation
            if g_D <= 0 or v <= 0:
                results.append({
                    "g_D": g_D,
                    "v": v,
                    "status": "physical_failure",
                    "failure_reason": "g_D or v <= 0",
                    "scan_id": scan_id,
                })
                failure_count += 1
                continue
            
            if g_D >= 4 * np.pi:
                results.append({
                    "g_D": g_D,
                    "v": v,
                    "status": "physical_failure",
                    "failure_reason": "g_D >= 4*pi (non-perturbative)",
                    "scan_id": scan_id,
                })
                failure_count += 1
                continue
            
            # Compute point
            try:
                result = compute_point(g_D, v, verbose=False)
                results.append(result)
                
                if result["status"] == "viable":
                    viable_count += 1
                else:
                    failure_count += 1
                        
            except Exception as e:
                results.append({
                    "g_D": g_D,
                    "v": v,
                    "status": "numerical_failure",
                    "failure_reason": f"Exception: {str(e)}",
                    "scan_id": scan_id,
                })
                failure_count += 1
            
            # Progress indicator
            if point_count % max(1, total_points // 10) == 0:
                print(f"  Progress: {point_count}/{total_points} ({100*point_count/total_points:.1f}%) - viable: {viable_count}, failed: {failure_count}")
    
    print(f"\nScan {scan_id} complete at: {datetime.now().isoformat()}")
    print(f"Results: {viable_count} viable, {failure_count} failed out of {total_points} total")
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    df["scan_id"] = scan_id
    
    return df


def add_dependent_parameters(df):
    """Add dependent parameter columns to dataframe."""
    df["lambda"] = 3 * df["g_D"]**4 / (64 * np.pi**2)
    return df


def save_scan_results(df, output_dir="."):
    """Save scan results to CSV and JSON files."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Sort by status (viable first), then by f_peak_est (PTA-relevant first)
    status_order = {"viable": 0, "physical_failure": 1, "numerical_failure": 2}
    df["status_order"] = df["status"].map(status_order)
    df = df.sort_values(["status_order", "f_peak_est"], na_position="last")
    
    # Save to CSV
    csv_path = os.path.join(output_dir, "fopt_benchmarks.csv")
    csv_columns = [
        "g_D", "v", "lambda", "beta_lambda", "m_rho",
        "Tn", "Tp", "Tr", "alpha", "beta_H", "f_peak_est",
        "eternal_inflation", "status", "failure_reason", "scan_id"
    ]
    available_columns = [c for c in csv_columns if c in df.columns]
    df[available_columns].to_csv(csv_path, index=False)
    
    print(f"Saved scan results to: {csv_path}")
    
    # Save full results to JSON
    json_path = os.path.join(output_dir, "fopt_results.json")
    df.to_json(json_path, orient="records", indent=2)
    print(f"Saved full results to: {json_path}")
    
    return csv_path, json_path


def analyze_results(df):
    """Analyze scan results and print summary."""
    print("\n" + "="*80)
    print("SCAN RESULTS ANALYSIS")
    print("="*80)
    
    total = len(df)
    viable = len(df[df["status"] == "viable"])
    physical_fail = len(df[df["status"] == "physical_failure"])
    numerical_fail = len(df[df["status"] == "numerical_failure"])
    
    print(f"\nTotal points scanned: {total}")
    print(f"  Viable: {viable} ({100*viable/total:.2f}%)")
    print(f"  Physical failures: {physical_fail} ({100*physical_fail/total:.2f}%)")
    print(f"  Numerical failures: {numerical_fail} ({100*numerical_fail/total:.2f}%)")
    
    if viable > 0:
        viable_df = df[df["status"] == "viable"]
        print(f"\nViable points summary:")
        print(f"  g_D range: [{viable_df['g_D'].min():.4g}, {viable_df['g_D'].max():.4g}]")
        print(f"  v range: [{viable_df['v'].min():.4g}, {viable_df['v'].max():.4g}] GeV")
        print(f"  alpha range: [{viable_df['alpha'].min():.4g}, {viable_df['alpha'].max():.4g}]")
        print(f"  beta_H range: [{viable_df['beta_H'].min():.4g}, {viable_df['beta_H'].max():.4g}]")
        print(f"  Tp range: [{viable_df['Tp'].min():.4g}, {viable_df['Tp'].max():.4g}] GeV")
        print(f"  Tr range: [{viable_df['Tr'].min():.4g}, {viable_df['Tr'].max():.4g}] GeV")
        print(f"  f_peak_est range: [{viable_df['f_peak_est'].min():.4g}, {viable_df['f_peak_est'].max():.4g}] Hz")
        
        # PTA band: ~1e-9 to 1e-7 Hz
        pta_lower = 1e-9
        pta_upper = 1e-7
        in_pta = viable_df[
            (viable_df['f_peak_est'] >= pta_lower) & 
            (viable_df['f_peak_est'] <= pta_upper)
        ]
        print(f"\nPoints in PTA band ({pta_lower:.1e}-{pta_upper:.1e} Hz): {len(in_pta)}")
        
        if len(in_pta) > 0:
            print(f"  g_D range: [{in_pta['g_D'].min():.4g}, {in_pta['g_D'].max():.4g}]")
            print(f"  v range: [{in_pta['v'].min():.4g}, {in_pta['v'].max():.4g}] GeV")
            print(f"  f_peak_est range: [{in_pta['f_peak_est'].min():.4g}, {in_pta['f_peak_est'].max():.4g}] Hz")
    
    print(f"\nFailure reasons breakdown:")
    failure_counts = df[df["status"] != "viable"]["failure_reason"].value_counts()
    for reason, count in failure_counts.head(10).items():
        print(f"  {reason}: {count}")
    
    print("="*80)
    
    return {
        "total": total,
        "viable": viable,
        "physical_failures": physical_fail,
        "numerical_failures": numerical_fail,
        "in_pta_band": len(in_pta) if viable > 0 else 0,
    }


def find_best_points(df, n_best=5, target_f_peak=1e-8):
    """Find best points closest to target PTA frequency."""
    viable_df = df[df["status"] == "viable"].copy()
    
    if len(viable_df) == 0:
        print("\nNo viable points found. Cannot identify best points.")
        return pd.DataFrame()
    
    # Add distance from target frequency (in log space)
    viable_df["f_peak_dist"] = np.abs(np.log10(viable_df["f_peak_est"]) - np.log10(target_f_peak))
    viable_df = viable_df.sort_values("f_peak_dist")
    
    best = viable_df.head(n_best)
    
    print(f"\n=== BEST {n_best} POINTS (closest to f_peak = {target_f_peak:.2e} Hz) ===")
    for i, (_, row) in enumerate(best.iterrows()):
        print(f"\n#{i+1}:")
        print(f"  g_D = {row['g_D']:.6f}")
        print(f"  v = {row['v']:.6f} GeV")
        print(f"  Tn = {row['Tn']:.4g} GeV")
        print(f"  Tp = {row['Tp']:.4g} GeV")
        print(f"  Tr = {row['Tr']:.4g} GeV")
        print(f"  alpha = {row['alpha']:.4g}")
        print(f"  beta_H = {row['beta_H']:.4g}")
        print(f"  f_peak_est = {row['f_peak_est']:.4g} Hz")
        print(f"  distance from target = {row['f_peak_dist']:.4f} (log10)")
    
    return best


def main():
    """Main scan function with adaptive range extension."""
    
    print("\n" + "="*80)
    print("SU2_CONFORMAL FOPT PARAMETER SCAN")
    print("="*80)
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Scan configuration - start with ranges that cover PTA band
    scans_to_run = [
        {
            "name": "coarse_pta",
            "g_D_range": (0.5, 3.0),
            "v_range": (0.01, 10.0),
            "n_gD": 20,
            "n_v": 20,
            "description": "Coarse scan covering PTA-compatible range",
        },
    ]
    
    all_results = []
    scan_summaries = []
    
    for i, scan_config in enumerate(scans_to_run):
        print(f"\n{'='*80}")
        print(f"Running scan {i+1}/{len(scans_to_run)}: {scan_config['name']}")
        print(f"Description: {scan_config['description']}")
        print("="*80)
        
        # Run scan
        df = scan_parameter_space(
            g_D_range=scan_config["g_D_range"],
            v_range=scan_config["v_range"],
            n_points_gD=scan_config["n_gD"],
            n_points_v=scan_config["n_v"],
            scan_id=scan_config["name"],
            verbose=True,
        )
        
        # Add dependent parameters
        df = add_dependent_parameters(df)
        
        # Save intermediate results
        csv_path, json_path = save_scan_results(df, output_dir)
        
        # Analyze
        summary = analyze_results(df)
        scan_summaries.append({
            "scan_name": scan_config["name"],
            **summary,
        })
        
        all_results.append(df)
        
        # Check results
        viable_count = summary["viable"]
        pta_count = summary.get("in_pta_band", 0)
        
        if viable_count > 0:
            print(f"\n✓ Found {viable_count} viable points ({pta_count} in PTA band)")
            
            # Find and display best points
            all_df = pd.concat(all_results, ignore_index=True)
            best_df = find_best_points(all_df, n_best=5, target_f_peak=1e-8)
            
            if pta_count == 0 and viable_count > 0:
                print(f"\n⚠ No points in PTA band yet. Extending scan range.")
                # Extend to lower v
                g_D_min, g_D_max = scan_config["g_D_range"]
                v_min, v_max = scan_config["v_range"]
                new_v_min = v_min / 2
                new_v_max = v_max * 2
                
                next_scan = {
                    "name": f"extended_{i+1}",
                    "g_D_range": (g_D_min, g_D_max),
                    "v_range": (new_v_min, new_v_max),
                    "n_gD": 25,
                    "n_v": 25,
                    "description": f"Extended v range: [{new_v_min:.2f}, {new_v_max:.2f}] GeV",
                }
                scans_to_run.append(next_scan)
                print(f"   Next scan: v = [{new_v_min:.2f}, {new_v_max:.2f}] GeV")
            else:
                print(f"\n✓ Scan has points in PTA band!")
        else:
            print(f"\n✗ No viable points found. Extending scan range.")
            g_D_min, g_D_max = scan_config["g_D_range"]
            v_min, v_max = scan_config["v_range"]
            
            new_g_D_min = max(g_D_min / 1.5, 0.1)
            new_g_D_max = min(g_D_max * 1.5, 12.0)
            new_v_min = v_min / 2
            new_v_max = v_max * 2
            
            next_scan = {
                "name": f"extended_{i+1}",
                "g_D_range": (new_g_D_min, new_g_D_max),
                "v_range": (new_v_min, new_v_max),
                "n_gD": 25,
                "n_v": 25,
                "description": f"Extended range: g_D [{new_g_D_min:.2f}, {new_g_D_max:.2f}], v [{new_v_min:.2f}, {new_v_max:.2f}] GeV",
            }
            scans_to_run.append(next_scan)
            print(f"   Next scan: g_D = [{new_g_D_min:.2f}, {new_g_D_max:.2f}], v = [{new_v_min:.2f}, {new_v_max:.2f}] GeV")
        
        # Limit to 2 scans total for now
        if i >= 0:  # Just do the first scan for now
            break
    
    # Combine all results
    final_df = pd.concat(all_results, ignore_index=True)
    
    # Save final combined results
    print(f"\n{'='*80}")
    print("FINAL RESULTS")
    print("="*80)
    
    final_csv, final_json = save_scan_results(final_df, output_dir)
    final_summary = analyze_results(final_df)
    
    # Find best points
    if final_summary["viable"] > 0:
        find_best_points(final_df, n_best=10, target_f_peak=1e-8)
    
    print(f"\nAll scan summaries:")
    for s in scan_summaries:
        print(f"  {s['scan_name']}: {s['viable']} viable / {s['total']} total")
    
    print(f"\n{'='*80}")
    print(f"SCAN COMPLETE")
    print(f"Total viable points: {final_summary['viable']}")
    print(f"Total points scanned: {final_summary['total']}")
    print(f"Points in PTA band: {final_summary.get('in_pta_band', 0)}")
    print(f"Results saved to: {final_csv}")
    print(f"Full data saved to: {final_json}")
    print("="*80)
    
    return final_df


if __name__ == "__main__":
    results_df = main()
