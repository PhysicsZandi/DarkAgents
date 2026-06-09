"""
fopt_model.py -- FOPT model definition for the conformal U(1)_D dark sector.

Model: classically scale-invariant U(1)_D with complex scalar Phi (charge +1),
       dark gauge boson A'_mu, and two Dirac fermions psi_1 (charge +1/2),
       psi_2 (charge -1/2).

Backend: semianalytic_pipeline (SemiAnalyticPipeline)
"""

import sys
import os
import numpy as np

# Add backend directory to path
_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from semianalytic_pipeline import SemiAnalyticPipeline


def compute_dependent_params(g_D, y_psi, v):
    """
    Compute dependent parameters from independent ones.

    Parameters
    ----------
    g_D : float
        Dark U(1)_D gauge coupling (independent).
    y_psi : float
        Yukawa coupling (independent).
    v : float
        Dark Higgs vev in GeV (independent).

    Returns
    -------
    dict
        Dependent parameters: beta_lambda, lambda_Phi, m_Aprime, m_psi, m_chi, gb_scalar.
    """
    beta_lambda = (3.0 * g_D**4 - 2.0 * y_psi**4) / (8.0 * np.pi**2)
    lambda_Phi = beta_lambda / 4.0
    m_Aprime = g_D * v
    m_psi = y_psi * v / np.sqrt(2.0)
    m_chi = np.sqrt(beta_lambda) * v
    gb_scalar = np.sqrt(beta_lambda)

    return {
        "beta_lambda": beta_lambda,
        "lambda_Phi": lambda_Phi,
        "m_Aprime": m_Aprime,
        "m_psi": m_psi,
        "m_chi": m_chi,
        "gb_scalar": gb_scalar,
    }


def build_model(g_D, y_psi, v):
    """
    Build and return a SemiAnalyticPipeline instance for the given parameters.

    Parameters
    ----------
    g_D : float
        Dark gauge coupling.
    y_psi : float
        Yukawa coupling.
    v : float
        Dark Higgs vev in GeV.

    Returns
    -------
    SemiAnalyticPipeline
        Configured pipeline instance.
    """
    # Backend mapping from handoff_model.json
    boson_gbs = {"gauge": g_D, "scalar": 0}
    boson_dofs = {"gauge": 3, "scalar": 1}
    fermion_gfs = {"psi": y_psi / np.sqrt(2.0)}
    fermion_dofs = {"psi": 8}

    model = SemiAnalyticPipeline(
        chi0=v,
        boson_gbs=boson_gbs,
        boson_dofs=boson_dofs,
        fermion_gfs=fermion_gfs,
        fermion_dofs=fermion_dofs,
        verbose=False,
    )

    return model


def compute_fopt(g_D, y_psi, v):
    """
    Compute FOPT observables for given model parameters.

    Parameters
    ----------
    g_D : float
        Dark gauge coupling.
    y_psi : float
        Yukawa coupling.
    v : float
        Dark Higgs vev in GeV.

    Returns
    -------
    dict
        FOPT results with keys: alpha, beta_H, Tn, Tp, Treh, eternal_inflation,
        f_peak_est, and dependent parameters.
    """
    # Compute dependent parameters
    dep = compute_dependent_params(g_D, y_psi, v)

    # Build model
    model = build_model(g_D, y_psi, v)

    # Compute FOPT observables
    try:
        Tn = model.get_Tn()
    except Exception:
        Tn = np.nan

    try:
        Tp = model.get_Tp()
    except Exception:
        Tp = np.nan

    try:
        alpha = model.get_alpha()
    except Exception:
        alpha = np.nan

    try:
        beta_H = model.get_beta_H()
    except Exception:
        beta_H = np.nan

    try:
        Treh = model.get_Tr()
    except Exception:
        Treh = np.nan

    try:
        eternal_inflation = model.get_check_eternal_inflation()
    except Exception:
        eternal_inflation = np.nan

    # Estimate redshifted peak frequency (template-independent, order-of-magnitude)
    # f_peak ~ 1.6e-5 Hz * (beta/H) * (Treh / 100 GeV) * (g*/100)^{1/6}
    if np.isfinite(beta_H) and np.isfinite(Treh) and beta_H > 0 and Treh > 0:
        try:
            gstar_eff = model.get_gstar_eff(Tp) if np.isfinite(Tp) else model.get_gstar_eff(Treh)
            f_peak_est = 1.6e-5 * beta_H * (Treh / 100.0) * (gstar_eff / 100.0) ** (1.0 / 6.0)
        except Exception:
            f_peak_est = np.nan
    else:
        f_peak_est = np.nan

    result = {
        "g_D": g_D,
        "y_psi": y_psi,
        "v": v,
        "alpha": alpha,
        "beta_H": beta_H,
        "Tn": Tn,
        "Tp": Tp,
        "Treh": Treh,
        "f_peak_est": f_peak_est,
        "eternal_inflation": eternal_inflation,
        **dep,
    }

    return result


def is_viable(result):
    """
    Check if a FOPT result corresponds to a viable point.

    A viable point must have:
    - Finite positive alpha
    - Finite positive beta/H
    - Positive Tp
    - Positive Treh
    - No eternal inflation (get_check_eternal_inflation() returns False)
    - beta_lambda > 0 (CW condition)
    - g_D > y_psi / sqrt(2) (supercooling condition: m_A' > m_psi)

    Parameters
    ----------
    result : dict
        FOPT result from compute_fopt().

    Returns
    -------
    bool
        True if the point is viable.
    """
    # Physical guards
    if result["beta_lambda"] <= 0:
        return False
    if result["g_D"] <= result["y_psi"] / np.sqrt(2.0):
        return False
    if result["g_D"] <= 0 or result["y_psi"] < 0 or result["v"] <= 0:
        return False

    # FOPT observables
    if not np.isfinite(result["alpha"]) or result["alpha"] <= 0:
        return False
    if not np.isfinite(result["beta_H"]) or result["beta_H"] <= 0:
        return False
    if not np.isfinite(result["Tp"]) or result["Tp"] <= 0:
        return False
    if not np.isfinite(result["Treh"]) or result["Treh"] <= 0:
        return False
    if not np.isfinite(result["Tn"]) or result["Tn"] <= 0:
        return False

    # Eternal inflation check
    if result["eternal_inflation"] is True or not np.isfinite(result["eternal_inflation"]):
        return False

    return True


def smoke_test():
    """Run a smoke test on a benchmark point from Balan et al. (2502.19478)."""
    print("=" * 60)
    print("Smoke test: Balan et al. inspired benchmark")
    print("=" * 60)

    # Point A from Balan et al.: g=0.677, y=0.224, v=173 MeV = 0.173 GeV
    g_D = 0.677
    y_psi = 0.224
    v = 0.173  # GeV

    print(f"Parameters: g_D={g_D}, y_psi={y_psi}, v={v} GeV")
    print()

    dep = compute_dependent_params(g_D, y_psi, v)
    print("Dependent parameters:")
    for key, val in dep.items():
        print(f"  {key} = {val:.6g}")
    print()

    result = compute_fopt(g_D, y_psi, v)
    print("FOPT observables:")
    for key in ["alpha", "beta_H", "Tn", "Tp", "Treh", "f_peak_est", "eternal_inflation"]:
        val = result[key]
        if np.isfinite(val):
            print(f"  {key} = {val:.6g}")
        else:
            print(f"  {key} = NaN (not finite)")

    print()
    print(f"Viable: {is_viable(result)}")
    print("=" * 60)


if __name__ == "__main__":
    smoke_test()
