"""FOPT model implementation for the classically scale-invariant gauged dark
U(1)_D (Coleman-Weinberg) model.

Independent free parameters (scan axes):
    g_D : dark gauge coupling, in [0.1, 1.5]
    y   : dark Yukawa coupling, in [0.0, 1.0]   (hard cut: y**4 < 1.5 * g_D**4)
    w   : radiatively generated vev in GeV, in [0.05, 10.0]

Backend mapping (semianalytic_pipeline), from post-critic handoff_model.json:
    chi0          = w
    bosons {Zp}:  gb_gauge   = g_D,        dof = 3
    fermions {chi}: gf_fermion = y/sqrt(2), dof = 8   (two degenerate Dirac fermions)

Dependent (computed internally, NOT scanned):
    beta_lambda = (1/(8 pi^2)) * (3 g_D^4 - 8 (y/sqrt2)^4)   (must be > 0)
    m_chi_radial (scalon) = sqrt(beta_lambda) * w
    m_Zp = g_D * w,   m_chi = y * w / sqrt(2)

All masses proportional to the single vev w -> single-field conformal model,
compatible with backend/semianalytic_pipeline.py.
"""

import sys
from pathlib import Path
import numpy as np

# make backend importable
_BACKEND = Path("/Users/mattezandi/Desktop/code/run_folder/claude_workspace/backend")
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from semianalytic_pipeline import SemiAnalyticPipeline, gstar  # noqa: E402

# physical / scan bounds (independent params)
G_D_BOUNDS = (0.1, 1.5)
Y_BOUNDS = (0.0, 1.0)
W_BOUNDS = (0.05, 10.0)  # GeV

ZP_DOF = 3
CHI_DOF = 8

# PTA band for f_peak anchoring (Hz)
PTA_BAND = (1e-9, 1e-7)


def beta_lambda(g_D, y):
    """CW beta-function combination (dependent). Must be > 0 for radiative SSB."""
    gf = y / np.sqrt(2.0)
    return (1.0 / (8.0 * np.pi**2)) * (ZP_DOF * g_D**4 - CHI_DOF * gf**4)


def passes_physical_guards(g_D, y, w):
    """Enforce physical scan bounds before calling the backend."""
    if not (G_D_BOUNDS[0] <= g_D <= G_D_BOUNDS[1]):
        return False, "g_D out of bounds"
    if not (Y_BOUNDS[0] <= y <= Y_BOUNDS[1]):
        return False, "y out of bounds"
    if not (W_BOUNDS[0] <= w <= W_BOUNDS[1]):
        return False, "w out of bounds"
    # perturbativity
    if g_D <= 0 or g_D > 4.0 or y > 4.0 or y < 0:
        return False, "non-perturbative coupling"
    # hard cut y^4 < 1.5 g_D^4  (equivalent to beta_lambda > 0 since
    # 3 g_D^4 - 8 (y/sqrt2)^4 = 3 g_D^4 - 2 y^4 > 0  <=>  y^4 < 1.5 g_D^4)
    if y**4 >= 1.5 * g_D**4:
        return False, "hard cut y^4 >= 1.5 g_D^4 (beta_lambda<=0)"
    if beta_lambda(g_D, y) <= 0:
        return False, "beta_lambda <= 0"
    return True, ""


def build_model(g_D, y, w, verbose=False):
    """Instantiate the backend pipeline for a given (g_D, y, w) point."""
    boson_gbs = {"Zp": g_D}
    boson_dofs = {"Zp": ZP_DOF}
    fermion_gfs = {"chi": y / np.sqrt(2.0)}
    fermion_dofs = {"chi": CHI_DOF}
    return SemiAnalyticPipeline(
        chi0=w,
        boson_gbs=boson_gbs,
        boson_dofs=boson_dofs,
        fermion_gfs=fermion_gfs,
        fermion_dofs=fermion_dofs,
        verbose=verbose,
    )


def f_peak_est(beta_H, Treh_GeV):
    """Template-independent, order-of-magnitude redshifted peak frequency (Hz).

    f_peak ~ 1.6e-5 Hz * (beta/H) * (Treh/100 GeV) * (g*/100)^(1/6)
    """
    if not (np.isfinite(beta_H) and np.isfinite(Treh_GeV)) or Treh_GeV <= 0:
        return np.nan
    try:
        gs = float(gstar(Treh_GeV))
    except Exception:
        gs = 10.0
    if not np.isfinite(gs) or gs <= 0:
        gs = 10.0
    return 1.6e-5 * beta_H * (Treh_GeV / 100.0) * (gs / 100.0) ** (1.0 / 6.0)


def evaluate_point(g_D, y, w, verbose=False):
    """Compute FOPT parameters for one point. Returns a result dict.

    status in {viable, physical_failure, numerical_failure, not_fopt}.
    """
    res = {
        "g_D": g_D, "y": y, "w": w,
        "beta_lambda": beta_lambda(g_D, y),
        "m_Zp": g_D * w,
        "m_chi": y * w / np.sqrt(2.0),
        "m_scalon": np.sqrt(max(beta_lambda(g_D, y), 0.0)) * w,
        "Tn": np.nan, "Tp": np.nan, "Treh": np.nan,
        "alpha": np.nan, "beta_H": np.nan,
        "eternal_inflation": None, "f_peak_est": np.nan,
        "status": "physical_failure", "failure_reason": "",
    }

    ok, why = passes_physical_guards(g_D, y, w)
    if not ok:
        res["failure_reason"] = why
        return res

    try:
        m = build_model(g_D, y, w, verbose=verbose)
        Tn = m.get_Tn()
        Tp = m.get_Tp()
        alpha = m.get_alpha()
        beta_H = m.get_beta_H()
        Treh = m.get_Tr()
        eternal = m.get_check_eternal_inflation()
    except Exception as e:
        res["status"] = "numerical_failure"
        res["failure_reason"] = f"backend exception: {e}"
        return res

    res.update({"Tn": Tn, "Tp": Tp, "Treh": Treh, "alpha": alpha,
                "beta_H": beta_H, "eternal_inflation": eternal})

    finite = all(np.isfinite(x) for x in (Tn, Tp, Treh, alpha, beta_H))
    if not finite:
        res["status"] = "numerical_failure"
        res["failure_reason"] = "non-finite backend output"
        return res

    positive = (Tp > 0 and Tn > 0 and Treh > 0 and alpha > 0 and beta_H > 0)
    if not positive:
        res["status"] = "not_fopt"
        res["failure_reason"] = "non-positive temperature/strength/timescale"
        return res

    if eternal is True:
        res["status"] = "physical_failure"
        res["failure_reason"] = "eternal inflation (transition never completes)"
        return res

    res["f_peak_est"] = f_peak_est(beta_H, Treh)
    res["status"] = "viable"
    return res


def smoke_test():
    """Validate against literature anchor Point A (arXiv:2502.19478)."""
    g_D, y, w = 0.877, 0.363, 92.9e-3  # w in GeV
    print("Smoke test: literature anchor Point A (g_D=0.877, y=0.363, w=92.9 MeV)")
    print("  beta_lambda =", beta_lambda(g_D, y), "(must be > 0)")
    r = evaluate_point(g_D, y, w, verbose=False)
    for k in ("status", "Tn", "Tp", "Treh", "alpha", "beta_H",
              "eternal_inflation", "f_peak_est", "failure_reason"):
        print(f"  {k:18s} = {r[k]}")
    print("  Literature target: T_p=8.36 MeV, T_reh=12.9 MeV, alpha=4.99, beta/H=21.1")
    return r


if __name__ == "__main__":
    smoke_test()
