"""Post-process PTArcade chains and plot posteriors/MAP spectrum."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import natpy as nat
import la_forge.core as co
import numpy as np
import pandas as pd
from getdist import MCSamples
from ptarcade import chains_utils as c_utils
from ptarcade import plot_utils as p_utils


MODEL_DIR = Path(__file__).resolve().parent
PROJECT_DIR = MODEL_DIR.parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
if str(MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(MODEL_DIR))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from pta_spectrum import h2omega_from_model  # noqa: E402


CHAINS_DIR = MODEL_DIR / "chains" / "minimal_conformal_su2_doublet"
BAYES_FILE = MODEL_DIR / "ptarcade_bayes.json"
POSTERIORS_FILE = MODEL_DIR / "pta_posteriors.pdf"
SPECTRUM_FILE = MODEL_DIR / "pta_ptarcade_spectrum.pdf"
WINDOWS_FILE = BACKEND_DIR / "pta_violin_windows.csv"


def load_violins(correlations=False):
    def find_core(filename: str) -> Path:
        repo_root = Path(__file__).resolve().parents[2]
        matches = list(repo_root.rglob(filename))
        if matches:
            return matches[0]
        matches = list(Path.cwd().rglob(filename))
        if matches:
            return matches[0]
        return None

    filename = "30fCP_30fiRN_3A.core" if correlations else "30fCP_30fiRN_2A.core"
    corepath = find_core(filename)
    label_correlations = correlations
    if corepath is None and not correlations:
        corepath = find_core("30fCP_30fiRN_3A.core")
        label_correlations = True
    if corepath is None:
        raise FileNotFoundError(f"Could not find PTA core file: {filename}")

    c0 = co.Core(corepath=str(corepath))
    if label_correlations:
        labels = [p for p in c0.params if "gw_hd" in p]
    else:
        labels = [p for p in c0.params if "rho" in p]
    if not labels:
        raise ValueError(f"No PTA violin parameters found in {corepath}")

    freqs = c0.rn_freqs  # array of frequencies

    # load free spec samples
    viol = c0(labels)  # this is now a numpy array of Nsamples x Nfreq

    dfreq = np.diff(np.concatenate((np.array([0]), freqs[::1])))

    H_0byh = 100 * nat.convert(nat.km * nat.s**-1 * nat.Mpc**-1, nat.Hz)  # H_0/h in Hz
    h2_omega_viol = np.log10(
        24
        * np.pi**4
        * (10**viol) ** 2
        * 1
        / np.repeat(dfreq, 1)
        * freqs**5
        / (3 * H_0byh**2)
    )
    return h2_omega_viol, freqs


def plot_violins(ax, h2_omega_viol, N_f=14, border="silver"):
    Tspan = 505861299.1401644
    n_freq = min(N_f, h2_omega_viol.shape[1])
    freqs = np.arange(1, n_freq + 1) / Tspan

    v1 = ax.violinplot(
        h2_omega_viol[:, :n_freq],
        positions=np.log10(freqs),
        widths=0.05,
        showextrema=False,
    )

    for pc in v1["bodies"]:
        pc.set_facecolor("silver")
        pc.set_edgecolor(border)
        pc.set_linestyle("solid")

    return


def main():
    if not CHAINS_DIR.exists():
        raise FileNotFoundError(f"PTArcade chain directory not found: {CHAINS_DIR}")
    params, chain = c_utils.import_chains(str(CHAINS_DIR))
    param_names = list(params.keys())
    params_for_filter = np.array(param_names, dtype=object)
    filtered = c_utils.chain_filter(chain, params_for_filter, None, None)
    filtered_array = filtered[0]
    filtered_params = filtered[1]
    filtered_priors = {
        k.replace("_", "-"): v
        for k, v in params.items()
        if k.replace("_", "-") in filtered_params and (v is not None and not np.isnan(v).any())
    }
    samples = MCSamples(
        samples=filtered_array,
        names=filtered_params,
        ranges=filtered_priors,
        ignore_rows=1,
    )
    bayes_est = c_utils.get_bayes_est(samples, filtered_params)
    max_pos = c_utils.get_max_pos(filtered_params, bayes_est, samples, filtered_priors)
    sigma_percentiles = {
        "1sigma": (15.865, 84.135),
        "2sigma": (2.275, 97.725),
        "3sigma": (0.135, 99.865),
    }
    sigma_regions = {}
    for idx, param in enumerate(filtered_params):
        column = filtered_array[:, idx]
        finite = column[np.isfinite(column)]
        if finite.size == 0:
            continue
        sigma_regions[param] = {
            label: {
                "low": float(np.percentile(finite, lo)),
                "high": float(np.percentile(finite, hi)),
            }
            for label, (lo, hi) in sigma_percentiles.items()
        }

    output = {
        "bayes_est": {p: {"mean": float(v[0]), "std": float(v[1])} for p, v in bayes_est.items()},
        "map_est": {k: float(v) for k, v in max_pos.items()},
        "sigma_regions": sigma_regions,
        "chains_dir": str(CHAINS_DIR),
        "finite_samples": bool(np.isfinite(filtered_array).all() and filtered_array.size > 0),
    }
    BAYES_FILE.write_text(json.dumps(output, indent=2))
    p_utils.plot_posteriors(
        [chain],
        [params],
        par_names=[[r"$g_D$", r"$\log_{10}(v_D/{\rm GeV})$"]],
        samples_name=["minimal conformal SU(2) doublet"],
        model_name="pta",
        plots_dir=str(MODEL_DIR),
        save=True,
        verbose=True,
        hpi_levels=[0.68, 0.95, 0.99],
        levels=[0.68, 0.95, 0.99],
    )
    generated = MODEL_DIR / "pta_posteriors.pdf"
    if not generated.exists():
        candidates = sorted(MODEL_DIR.glob("*posteriors.pdf"))
        if candidates:
            candidates[-1].rename(POSTERIORS_FILE)
    windows = pd.read_csv(WINDOWS_FILE, index_col=False)
    map_gD = float(max_pos.get("gD", max_pos.get("gD-0", np.nan)))
    map_logv = float(max_pos.get("log10-vD", max_pos.get("log10_vD", np.nan)))
    f = np.logspace(windows["log10_f_Hz"].min() - 0.15, windows["log10_f_Hz"].max() + 0.15, 300)
    omega = h2omega_from_model(f, map_gD, 10.0**map_logv)
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    try:
        viol, _ = load_violins(False)
        plot_violins(ax, viol, N_f=len(windows))
    except Exception:
        for _, row in windows.iterrows():
            ax.fill_between(
                [row["log10_f_Hz"] - 0.025, row["log10_f_Hz"] + 0.025],
                row["ymin_log10_h2OmegaGW"],
                row["ymax_log10_h2OmegaGW"],
                color="silver",
                alpha=0.55,
            )
    good = np.isfinite(omega) & (omega > 0)
    ax.plot(np.log10(f[good]), np.log10(omega[good]), lw=1.8, label="PTArcade MAP")
    ax.set_xlabel(r"$\log_{10}(f/{\rm Hz})$")
    ax.set_ylabel(r"$\log_{10}(h^2\Omega_{\rm GW})$")
    ax.set_xlim(windows["log10_f_Hz"].min() - 0.2, windows["log10_f_Hz"].max() + 0.2)
    ax.set_ylim(windows["ymin_log10_h2OmegaGW"].min() - 1.0, windows["ymax_log10_h2OmegaGW"].max() + 0.8)
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(SPECTRUM_FILE)


if __name__ == "__main__":
    main()
