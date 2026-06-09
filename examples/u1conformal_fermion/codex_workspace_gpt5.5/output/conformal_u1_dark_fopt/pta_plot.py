"""Plot PTA benchmark spectra against NANOGrav violin bands."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import natpy as nat
import la_forge.core as co
import numpy as np
import pandas as pd

OUTDIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(OUTDIR) not in sys.path:
    sys.path.insert(0, str(OUTDIR))

from pta_spectrum import SELECTED_TEMPLATE, spectrum_from_fopt  # noqa: E402


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


def select_diverse(rows: pd.DataFrame, n: int = 4) -> pd.DataFrame:
    viable = rows[rows["status"] == "viable"].copy()
    if viable.empty:
        return rows.head(0)
    viable = viable.sort_values(["inside_bins", "window_rms_distance_log10"], ascending=[False, True]).head(40)
    selected = [viable.iloc[0]]
    while len(selected) < min(n, len(viable)):
        chosen = []
        for _, row in viable.iterrows():
            if any(row["spectrum_id"] == s["spectrum_id"] for s in selected):
                continue
            distances = []
            for s in selected:
                distances.append(
                    (
                        np.log10(row["v_D"]) - np.log10(s["v_D"])
                    ) ** 2
                    + (row["g_D"] - s["g_D"]) ** 2
                    + (row["y_D"] - s["y_D"]) ** 2
                )
            chosen.append((min(distances), row))
        if not chosen:
            break
        selected.append(max(chosen, key=lambda item: item[0])[1])
    return pd.DataFrame(selected)


def main() -> None:
    scan = pd.read_csv(OUTDIR / "pta_benchmark_scan.csv")
    selected = select_diverse(scan)
    h2_omega_viol, _ = load_violins(correlations=False)

    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    plot_violins(ax, h2_omega_viol, N_f=14)
    fgrid = np.logspace(-9.2, -6.8, 600)
    colors = ["#0b6e69", "#b23a48", "#2d5aa7", "#7a5c00"]
    for color, (_, row) in zip(colors, selected.iterrows()):
        values = spectrum_from_fopt(fgrid, row.to_dict(), template=SELECTED_TEMPLATE)
        mask = values > 0.0
        label = (
            rf"{row['name']} "
            rf"({int(row['inside_bins'])}/{int(row['total_bins'])})"
        )
        ax.plot(np.log10(fgrid[mask]), np.log10(values[mask]), lw=1.7, color=color, label=label)

    ax.set_xlim(-9.15, -6.95)
    ax.set_ylim(-12.2, -5.8)
    ax.set_xlabel(r"$\log_{10}(f/{\rm Hz})$")
    ax.set_ylabel(r"$\log_{10}(h^2\Omega_{\rm GW})$")
    ax.set_title(r"Conformal $U(1)_D$ FOPT benchmark spectra")
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(fontsize=7, loc="upper left", frameon=False)
    fig.tight_layout()
    fig.savefig(OUTDIR / "pta_benchmark_spectrum.pdf")
    print(f"wrote {OUTDIR / 'pta_benchmark_spectrum.pdf'}")


if __name__ == "__main__":
    main()
