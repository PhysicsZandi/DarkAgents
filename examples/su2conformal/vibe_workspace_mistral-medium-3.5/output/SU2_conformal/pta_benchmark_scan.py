"""
PTA benchmark scan for SU2_conformal model.
Scans (g_D, v) parameter space and evaluates GW spectrum against PTA violin windows.
"""
import numpy as np
import pandas as pd
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from spectrum import Spectrum
from semianalytic_pipeline import SemiAnalyticPipeline


def load_pta_violin_windows():
    violin_file = Path(__file__).resolve().parents[2] / "backend" / "pta_violin_windows.csv"
    # Read CSV - the file has columns: bin_i, f_nHz, log10_f_Hz, ymin, ymax
    # where f_nHz is in nHz, log10_f_Hz is log10(frequency in Hz)
    df = pd.read_csv(violin_file)
    # Compute f_Hz from f_nHz (convert nHz to Hz)
    df["f_Hz"] = df["f_nHz"] * 1e-9
    return df


def compute_spectrum_at_fopt_point(g_D, v, template="dbf"):
    chi0 = v
    boson_gbs = {"W": g_D / 2, "W3": 0.0}
    boson_dofs = {"W": 6, "W3": 2}
    try:
        model = SemiAnalyticPipeline(
            chi0=chi0, boson_gbs=boson_gbs, boson_dofs=boson_dofs,
            fermion_gfs={}, fermion_dofs={}, verbose=False,
        )
        alpha = model.get_alpha()
        beta_H = model.get_beta_H()
        Treh = model.get_Tr()
        if not all(np.isfinite([alpha, beta_H, Treh])) or any(x <= 0 for x in [alpha, beta_H, Treh]):
            return None, None, None, None
        return float(alpha), float(beta_H), float(Treh), model
    except:
        return None, None, None, None


def compute_spectrum_values(f, T, alpha, beta_H, template="dbf"):
    spectrum = Spectrum(template=template)
    try:
        h2OmegaGW = spectrum.h2OmegaGW(f, T, alpha, beta_H)
        return np.where(np.isfinite(h2OmegaGW), h2OmegaGW, 0.0)
    except:
        return np.zeros_like(f)


def main():
    benchmarks_csv = Path(__file__).parent / "fopt_benchmarks.csv"
    output_csv = Path(__file__).parent / "pta_benchmark_scan.csv"
    output_json = Path(__file__).parent / "pta_benchmark_scan.json"
    template = "dbf"
    
    print("Loading FOPT benchmarks...")
    df_benchmarks = pd.read_csv(benchmarks_csv)
    print(f"Loaded {len(df_benchmarks)} benchmark points")
    
    pta_df = load_pta_violin_windows()
    f_pta = pta_df["f_Hz"].values
    f_pta_list = [float(x) for x in f_pta.tolist()]
    print(f"PTA frequencies: {len(f_pta)} bins from {f_pta[0]:.2e} to {f_pta[-1]:.2e} Hz")
    
    print("Finding best-fit points...")
    n_scan = min(len(df_benchmarks[df_benchmarks["status"] == "viable"]), 50)
    
    best_points = []
    for idx, row in df_benchmarks[df_benchmarks["status"] == "viable"].head(n_scan).iterrows():
        g_D = row["g_D"]
        v = row["v"]
        print(f"  Point {idx}: g_D={g_D:.4f}, v={v:.4e}")
        
        try:
            alpha, beta_H, Treh, model = compute_spectrum_at_fopt_point(g_D, v, template)
            if any(x is None for x in [alpha, beta_H, Treh]):
                print(f"    -> Failed FOPT")
                continue
            
            h2OmegaGW = compute_spectrum_values(f_pta, Treh, alpha, beta_H, template)
            peak_idx = np.argmax(h2OmegaGW)
            peak_f = float(f_pta[peak_idx])
            peak_amp = float(h2OmegaGW[peak_idx])
            
            f_target = 3e-9
            f_width = 2e-9
            f_score = np.exp(-0.5 * ((np.log10(peak_f) - np.log10(f_target)) / np.log10(f_width))**2) if peak_f > 0 else 0
            
            log10_amp = np.log10(peak_amp) if peak_amp > 0 else -np.inf
            amp_target = -9.5
            amp_width = 2.0
            a_score = np.exp(-0.5 * ((log10_amp - amp_target) / amp_width)**2) if np.isfinite(log10_amp) else 0
            
            total_score = float(f_score + a_score)
            
            best_points.append({
                "g_D": float(g_D), "v": float(v), "alpha": alpha,
                "beta_H": beta_H, "T_star": Treh,
                "f_peak_Hz": peak_f, "h2OmegaGW_peak": peak_amp,
                "f_score": float(f_score), "a_score": float(a_score),
                "score": total_score,
                "h2OmegaGW": [float(x) for x in h2OmegaGW.tolist()]
            })
            
            print(f"    alpha={alpha:.2e}, beta_H={beta_H:.2e}, T*={Treh:.2e}")
            print(f"    f_peak={peak_f:.2e}, h2Omega={peak_amp:.2e}, score={total_score:.4f}")
        except Exception as e:
            print(f"    Error: {e}")
            continue
    
    best_points.sort(key=lambda x: x["score"], reverse=True)
    
    csv_data = [{
        "rank": i+1, "g_D": p["g_D"], "v": p["v"], "alpha": p["alpha"],
        "beta_H": p["beta_H"], "T_star": p["T_star"],
        "f_peak_Hz": p["f_peak_Hz"], "h2OmegaGW_peak": p["h2OmegaGW_peak"],
        "f_score": p["f_score"], "a_score": p["a_score"],
        "score": p["score"], "status": "viable"
    } for i, p in enumerate(best_points)]
    
    pd.DataFrame(csv_data).to_csv(output_csv, index=False)
    print(f"Saved {len(csv_data)} points to {output_csv}")
    
    json_data = {
        "model": "SU2_conformal", "template": template,
        "pta_frequencies_Hz": f_pta_list,
        "best_fit_points": [{
            "rank": i+1, "name": f"pta_point_{i:03d}",
            "parameters": {"g_D": p["g_D"], "v": p["v"]},
            "alpha": p["alpha"], "beta_H": p["beta_H"], "T_star": p["T_star"],
            "f_peak_Hz": p["f_peak_Hz"], "h2OmegaGW_peak": p["h2OmegaGW_peak"],
            "score": p["score"],
            "spectrum": {
                "frequency_Hz": f_pta_list,
                "h2OmegaGW": p["h2OmegaGW"]
            }
        } for i, p in enumerate(best_points[:10])]
    }
    
    with open(output_json, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Saved {len(json_data['best_fit_points'])} points to {output_json}")
    
    print("\n=== Summary ===")
    print(f"Template: {template}, Points: {len(best_points)}")
    if best_points:
        for i, p in enumerate(best_points[:3]):
            print(f"  #{i+1}: g_D={p['g_D']:.4f}, v={p['v']:.4e}, score={p['score']:.4f}")


if __name__ == "__main__":
    main()
