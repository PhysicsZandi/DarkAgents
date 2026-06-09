"""FOPT model implementation for su2cw-dark.

Classically conformal dark SU(2)_D with one complex scalar doublet, no fermions.
Coleman-Weinberg radiative symmetry breaking, supercooled FOPT.

Independent free parameters:
    g    : dark SU(2)_D gauge coupling
    chi0 : scalar radial vev <chi> in GeV

Backend mapping (from handoff_model.json):
    boson_gbs  = {"Wprime": g/2}   (m_W = g*chi/2 => gb = m_W/chi0 = g/2)
    boson_dofs = {"Wprime": 9}     (3 massive dark vectors x 3 polarizations)
    fermions   = none
    scalar (radial CW mode) added automatically by the backend.

Dependent quantities computed internally by the backend:
    beta_lambda = (9*(g/2)^4 + gb_scalar^4)/(8 pi^2)
    m_chi       = sqrt(beta_lambda) * chi0
"""

import sys
from pathlib import Path

import numpy as np

# Make the backend importable
_BACKEND_DIR = Path(__file__).resolve().parents[2] / "backend"
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from semianalytic_pipeline import SemiAnalyticPipeline  # noqa: E402

# PTA band for the order-of-magnitude redshifted peak frequency estimate (Hz)
PTA_F_LOW = 1e-9
PTA_F_HIGH = 1e-7


def build_model(g, chi0, verbose=False):
    """Instantiate the backend pipeline for a given (g, chi0) point."""
    gb_W = g / 2.0
    boson_gbs = {"Wprime": gb_W}
    boson_dofs = {"Wprime": 9}
    fermion_gfs = {}
    fermion_dofs = {}
    return SemiAnalyticPipeline(
        chi0=chi0,
        boson_gbs=boson_gbs,
        boson_dofs=boson_dofs,
        fermion_gfs=fermion_gfs,
        fermion_dofs=fermion_dofs,
        verbose=verbose,
    )


def estimate_f_peak(beta_H, T_reh, gstar_eff):
    """Template-independent order-of-magnitude redshifted peak frequency (Hz).

    f_peak ~ 1.6e-5 Hz * (beta/H) * (T_reh/100 GeV) * (gstar/100)^(1/6)
    """
    return 1.6e-5 * beta_H * (T_reh / 100.0) * (gstar_eff / 100.0) ** (1.0 / 6.0)


def compute_point(g, chi0, verbose=False):
    """Compute all FOPT observables for one independent-parameter point.

    Returns a dict. 'status' is one of:
        viable             : finite, positive observables, completes (no eternal infl.)
        physical_failure   : non-finite / non-positive observable, or eternal inflation
        numerical_failure  : backend raised an exception
    """
    out = {
        "g": g,
        "chi0": chi0,
        "beta_lambda": np.nan,
        "m_chi": np.nan,
        "Tn": np.nan,
        "Tp": np.nan,
        "Treh": np.nan,
        "alpha": np.nan,
        "beta_H": np.nan,
        "gstar_eff": np.nan,
        "eternal_inflation": None,
        "f_peak_est": np.nan,
        "status": "numerical_failure",
        "failure_reason": "",
    }

    try:
        model = build_model(g, chi0, verbose=verbose)
        out["beta_lambda"] = float(model.get_beta_lambda())
        out["m_chi"] = float(model.get_scalar_mass())

        Tn = float(model.get_Tn())
        Tp = float(model.get_Tp())
        alpha = float(model.get_alpha())
        beta_H = float(model.get_beta_H())
        Treh = float(model.get_Tr())
        eternal = model.get_check_eternal_inflation()

        out["Tn"] = Tn
        out["Tp"] = Tp
        out["alpha"] = alpha
        out["beta_H"] = beta_H
        out["Treh"] = Treh
        out["eternal_inflation"] = bool(eternal) if eternal is not None else None

    except Exception as e:  # backend numerical failure
        out["status"] = "numerical_failure"
        out["failure_reason"] = f"backend exception: {type(e).__name__}: {e}"
        return out

    # Physical guards
    obs = {"Tn": out["Tn"], "Tp": out["Tp"], "Treh": out["Treh"],
           "alpha": out["alpha"], "beta_H": out["beta_H"]}
    bad = [k for k, v in obs.items() if (not np.isfinite(v)) or v <= 0]
    if bad:
        out["status"] = "physical_failure"
        out["failure_reason"] = f"non-finite or non-positive: {','.join(bad)}"
        return out

    if out["eternal_inflation"] is True:
        out["status"] = "physical_failure"
        out["failure_reason"] = "eternal inflation: transition does not complete"
        return out

    # gstar at percolation, then peak-frequency estimate using Treh
    try:
        gstar_eff = float(model.get_gstar_eff(out["Tp"]))
        out["gstar_eff"] = gstar_eff
        out["f_peak_est"] = float(estimate_f_peak(out["beta_H"], out["Treh"], gstar_eff))
    except Exception as e:
        out["status"] = "physical_failure"
        out["failure_reason"] = f"gstar/f_peak failure: {e}"
        return out

    out["status"] = "viable"
    return out


def smoke_test():
    """Run one literature-anchored benchmark (arXiv:2109.11558 Scenario 1).

    g_D = 1.37, M_ZD = 8.23 MeV => chi0 = 2*M_ZD/g_D ~ 0.01201 GeV.
    """
    g = 1.37
    chi0 = 2.0 * 8.23e-3 / g  # GeV
    res = compute_point(g, chi0, verbose=False)
    print("=== smoke test: arXiv:2109.11558 Scenario 1 ===")
    print(f"g = {g}, chi0 = {chi0:.5g} GeV")
    for k in ("beta_lambda", "m_chi", "Tn", "Tp", "Treh", "alpha",
              "beta_H", "gstar_eff", "eternal_inflation", "f_peak_est",
              "status", "failure_reason"):
        print(f"  {k:18s}: {res[k]}")
    return res


if __name__ == "__main__":
    smoke_test()
