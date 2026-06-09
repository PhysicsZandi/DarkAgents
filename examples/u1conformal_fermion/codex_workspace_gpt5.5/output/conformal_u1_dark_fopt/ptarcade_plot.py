"""Post-process PTArcade chains and plot posterior/MAP spectrum."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import natpy as nat
import la_forge.core as co
import numpy as np
from getdist import MCSamples
from ptarcade import chains_utils as c_utils
from ptarcade import plot_utils as p_utils

OUTDIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(OUTDIR) not in sys.path:
    sys.path.insert(0, str(OUTDIR))

from pta_spectrum import evaluate_spectrum  # noqa: E402


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


def convert_stats(stats):
    out = {}
    for key, value in stats.items():
        if key == "log10-v-D":
            out["v_D"] = {"mean": float(10.0 ** value[0]), "std_log10": float(value[1])}
        else:
            out[key.replace("-", "_")] = {"mean": float(value[0]), "std": float(value[1])}
    return out


def main() -> None:
    chains_dir = OUTDIR / "chains" / "conformal_u1_dark_fopt"
    params, chain = c_utils.import_chains(str(chains_dir) + "/")
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
    if filtered_array.size == 0 or not np.isfinite(filtered_array).any():
        raise RuntimeError("No finite final PTArcade chain samples found")

    samples = MCSamples(samples=filtered_array, names=filtered_params, ranges=filtered_priors, ignore_rows=1)
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
            label: {"low": float(np.percentile(finite, lo)), "high": float(np.percentile(finite, hi))}
            for label, (lo, hi) in sigma_percentiles.items()
        }

    output = {
        "bayes_est": convert_stats(bayes_est),
        "map_est": {k.replace("-", "_"): float(v) for k, v in max_pos.items()},
        "sigma_regions": sigma_regions,
    }
    (OUTDIR / "ptarcade_bayes.json").write_text(json.dumps(output, indent=2) + "\n")

    p_utils.plot_posteriors(
        [chain],
        [params],
        par_names=[[r"$\log_{10}(v_D/{\rm GeV})$", r"$g_D$", r"$y_D$"]],
        samples_name=["conformal_u1_dark_fopt"],
        model_name="pta",
        plots_dir=str(OUTDIR) + "/",
        save=True,
        verbose=True,
        hpi_levels=[0.68, 0.95, 0.99],
        levels=[0.68, 0.95, 0.99],
    )
    posterior = OUTDIR / "pta_posteriors.pdf"
    generated = OUTDIR / "pta_posteriors.pdf"
    if not posterior.exists() and generated.exists():
        generated.rename(posterior)

    map_params = output["map_est"]
    log10_v = map_params.get("log10_v_D", map_params.get("log10-v-D"))
    g_D = map_params.get("g_D")
    y_D = map_params.get("y_D")
    if log10_v is not None and g_D is not None and y_D is not None:
        fgrid = np.logspace(-9.2, -6.8, 600)
        _, values = evaluate_spectrum(fgrid, 10.0 ** float(log10_v), float(g_D), float(y_D))
        h2_omega_viol, _ = load_violins(correlations=False)
        fig, ax = plt.subplots(figsize=(7.0, 4.8))
        plot_violins(ax, h2_omega_viol, N_f=14)
        mask = values > 0.0
        ax.plot(np.log10(fgrid[mask]), np.log10(values[mask]), color="#0b6e69", lw=1.8, label="PTArcade MAP")
        ax.set_xlim(-9.15, -6.95)
        ax.set_ylim(-12.2, -5.8)
        ax.set_xlabel(r"$\log_{10}(f/{\rm Hz})$")
        ax.set_ylabel(r"$\log_{10}(h^2\Omega_{\rm GW})$")
        ax.set_title(r"PTArcade MAP spectrum")
        ax.grid(alpha=0.25, lw=0.5)
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(OUTDIR / "pta_ptarcade_spectrum.pdf")


if __name__ == "__main__":
    main()
