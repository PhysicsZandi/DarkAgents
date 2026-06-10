"""Plot PTArcade posteriors and MAP spectrum for u1conformal."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import natpy as nat
import la_forge.core as co
import numpy as np
from getdist import MCSamples
from ptarcade import chains_utils as c_utils
from ptarcade import plot_utils as p_utils


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from pta_spectrum import SELECTED_TEMPLATE, evaluate_fopt, h2omega_from_fopt  # noqa: E402


CHAINS_DIR = HERE / "chains" / "np_model"
POSTERIORS_TARGET = HERE / "pta_posteriors.pdf"
SPECTRUM_TARGET = HERE / "pta_ptarcade_spectrum.pdf"
BAYES_JSON = HERE / "ptarcade_bayes.json"


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


def convert_point(raw: dict[str, float]) -> dict[str, float]:
    out = {}
    if "log10-v" in raw:
        out["v"] = 10.0 ** float(raw["log10-v"])
    if "log10_v" in raw:
        out["v"] = 10.0 ** float(raw["log10_v"])
    if "g-D" in raw:
        out["g_D"] = float(raw["g-D"])
    if "g_D" in raw:
        out["g_D"] = float(raw["g_D"])
    return out


def finite_percentiles(values: np.ndarray) -> dict[str, dict[str, float]]:
    finite = values[np.isfinite(values)]
    levels = {
        "1sigma": (15.865, 84.135),
        "2sigma": (2.275, 97.725),
        "3sigma": (0.135, 99.865),
    }
    if finite.size == 0:
        return {}
    return {
        label: {"low": float(np.percentile(finite, lo)), "high": float(np.percentile(finite, hi))}
        for label, (lo, hi) in levels.items()
    }


def plot_map_spectrum(map_est: dict[str, float]) -> None:
    params = convert_point(map_est)
    if "v" not in params or "g_D" not in params:
        return
    windows = np.loadtxt(
        BACKEND_DIR / "pta_violin_windows.csv",
        delimiter=",",
        skiprows=1,
        usecols=(2,),
    )
    fine_f = np.logspace(float(np.min(windows)) - 0.08, float(np.max(windows)) + 0.08, 400)
    point = evaluate_fopt(params["v"], params["g_D"])
    omega = h2omega_from_fopt(fine_f, point, template=SELECTED_TEMPLATE)
    mask = omega > 0.0
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    h2_omega_viol, _ = load_violins(correlations=False)
    plot_violins(ax, h2_omega_viol, N_f=14)
    ax.plot(np.log10(fine_f[mask]), np.log10(omega[mask]), color="#1b9e77", lw=2.1, label="PTArcade MAP")
    ax.set_xlabel(r"$\log_{10}(f/{\rm Hz})$")
    ax.set_ylabel(r"$\log_{10}(h^2\Omega_{\rm GW})$")
    ax.set_xlim(float(np.min(windows)) - 0.1, float(np.max(windows)) + 0.1)
    ax.set_ylim(-12.5, -5.2)
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(SPECTRUM_TARGET)
    plt.close(fig)


def main() -> None:
    params, chain = c_utils.import_chains(str(CHAINS_DIR) + "/")
    param_names = list(params.keys())
    params_for_filter = np.array(param_names, dtype=object)
    filtered = c_utils.chain_filter(chain, params_for_filter, None, None)
    filtered_array = filtered[0]
    filtered_params = filtered[1]
    filtered_priors = {
        k.replace("_", "-"): v
        for k, v in params.items()
        if k.replace("_", "-") in filtered_params
        and (v is not None and not np.isnan(v).any())
    }
    samples = MCSamples(
        samples=filtered_array,
        names=filtered_params,
        labels=[r"\log_{10} v", r"g_D"],
        ranges=filtered_priors,
        ignore_rows=1,
    )
    bayes_est = c_utils.get_bayes_est(samples, filtered_params)
    max_pos = c_utils.get_max_pos(filtered_params, bayes_est, samples, filtered_priors)
    sigma_regions = {}
    for idx, param in enumerate(filtered_params):
        sigma_regions[param] = finite_percentiles(filtered_array[:, idx])
    if "log10-v" in filtered_params:
        idx = list(filtered_params).index("log10-v")
        sigma_regions["v"] = finite_percentiles(10.0 ** filtered_array[:, idx])
    elif "log10_v" in filtered_params:
        idx = list(filtered_params).index("log10_v")
        sigma_regions["v"] = finite_percentiles(10.0 ** filtered_array[:, idx])

    output = {
        "raw_bayes_est": {p: {"mean": float(v[0]), "std": float(v[1])} for p, v in bayes_est.items()},
        "raw_map_est": {k: float(v) for k, v in max_pos.items()},
        "map_est": convert_point(max_pos),
        "sigma_regions": sigma_regions,
    }
    BAYES_JSON.write_text(json.dumps(output, indent=2, sort_keys=True))
    p_utils.plot_posteriors(
        [chain],
        [params],
        par_names=[[r"$\log_{10} v$", r"$g_D$"]],
        samples_name=["u1conformal"],
        model_name="pta",
        plots_dir=str(HERE) + "/",
        save=True,
        verbose=True,
        hpi_levels=[0.68, 0.95, 0.99],
        levels=[0.68, 0.95, 0.99],
    )
    produced = HERE / "pta_posteriors.pdf"
    if produced.exists() and produced != POSTERIORS_TARGET:
        produced.replace(POSTERIORS_TARGET)
    plot_map_spectrum(max_pos)


if __name__ == "__main__":
    main()
