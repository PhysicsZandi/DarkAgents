"""
Dark U(1)_D conformal model implementation for FOPT analysis.

This module implements the classically scale-invariant Abelian Higgs model
with a complex scalar Phi charged under U(1)_D. The Coleman-Weinberg
mechanism generates the scalar vev radiatively.

Independent parameters:
    v (float): scalar vev in GeV
    g_D (float): U(1)_D gauge coupling (dimensionless)

Dependent parameters (computed from v, g_D):
    lambda_Phi (float): tree-level quartic (CW-fixed)
    m_A_prime (float): dark photon mass = g_D * v (GeV)
    m_rho (float): radial mode mass = sqrt(3/8) * g_D^2 * v / pi (GeV)
    beta_lambda (float): one-loop quartic beta function coefficient

The backend (SemiAnalyticPipeline) takes:
    chi0 = v
    boson_gbs = {"Aprime": g_D}
    boson_dofs = {"Aprime": 3}
"""

import sys
import os
import numpy as np

# Add backend directory to path
_backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from semianalytic_pipeline import SemiAnalyticPipeline


def compute_dependent_params(v, g_D):
    """Compute dependent parameters from independent ones.

    Parameters
    ----------
    v : float
        Scalar vev in GeV.
    g_D : float
        U(1)_D gauge coupling.

    Returns
    -------
    dict
        Dependent parameters: lambda_Phi, m_A_prime, m_rho, beta_lambda.
    """
    # beta_lambda = 3 * g_D^4 / (8 * pi^2)  from boson contribution
    beta_lambda = 3.0 * g_D**4 / (8.0 * np.pi**2)

    # m_A' = g_D * v
    m_A_prime = g_D * v

    # m_rho^2 = 3 * g_D^4 * v^2 / (8 * pi^2) = beta_lambda * v^2
    m_rho = np.sqrt(beta_lambda) * v

    # lambda_Phi: CW-fixed quartic. Not used directly by backend but
    # can be estimated as lambda_Phi ~ beta_lambda/4 for CSI models
    lambda_Phi = beta_lambda / 4.0

    return {
        "lambda_Phi": lambda_Phi,
        "m_A_prime": m_A_prime,
        "m_rho": m_rho,
        "beta_lambda": beta_lambda,
    }


def build_model(v, g_D):
    """Construct and return a SemiAnalyticPipeline instance for this model.

    Parameters
    ----------
    v : float
        Scalar vev in GeV
    g_D : float
        U(1)_D gauge coupling

    Returns
    -------
    SemiAnalyticPipeline
        Configured pipeline instance.
    """
    boson_gbs = {"Aprime": float(g_D)}
    boson_dofs = {"Aprime": 3}
    fermion_gfs = {}
    fermion_dofs = {}

    model = SemiAnalyticPipeline(
        chi0=float(v),
        boson_gbs=boson_gbs,
        boson_dofs=boson_dofs,
        fermion_gfs=fermion_gfs,
        fermion_dofs=fermion_dofs,
        verbose=False,
    )
    return model


def compute_fopt(v, g_D, gstar_interpolator=None):
    """Compute FOPT parameters for given independent parameters.

    Parameters
    ----------
    v : float
        Scalar vev in GeV.
    g_D : float
        U(1)_D gauge coupling.
    gstar_interpolator : callable, optional
        Interpolator for g*(T) from the CSV file. If None, loads it.

    Returns
    -------
    dict
        Dictionary with keys:
            alpha, beta_H, Tn, Tp, Tr, f_peak_est,
            eternal_inflation, dependent_params,
            status, failure_reason
        On failure, status is "physical_failure" or "numerical_failure".
    """
    result = {
        "v": v,
        "g_D": g_D,
        "alpha": None,
        "beta_H": None,
        "Tn": None,
        "Tp": None,
        "Tr": None,
        "f_peak_est": None,
        "eternal_inflation": None,
        "dependent_params": {},
        "status": "numerical_failure",
        "failure_reason": "",
    }

    # Physical guards
    if v <= 0:
        result["status"] = "physical_failure"
        result["failure_reason"] = "vev v <= 0"
        return result
    if g_D <= 0:
        result["status"] = "physical_failure"
        result["failure_reason"] = "gauge coupling g_D <= 0"
        return result
    if g_D >= np.sqrt(4.0 * np.pi):
        result["status"] = "physical_failure"
        result["failure_reason"] = "non-perturbative coupling g_D >= sqrt(4*pi)"
        return result

    # Compute dependent parameters
    result["dependent_params"] = compute_dependent_params(v, g_D)

    # Build model and compute FOPT parameters
    try:
        model = build_model(v, g_D)
    except Exception as e:
        result["status"] = "numerical_failure"
        result["failure_reason"] = f"model build failed: {e}"
        return result

    # Per-point FOPT computation with error handling
    try:
        Tn = model.get_Tn()
        if Tn is None or not np.isfinite(Tn) or Tn <= 0:
            result["failure_reason"] = f"Tn invalid: {Tn}"
            return result
        result["Tn"] = float(Tn)
    except Exception as e:
        result["failure_reason"] = f"Tn computation failed: {e}"
        return result

    try:
        Tp = model.get_Tp()
        if Tp is None or not np.isfinite(Tp) or Tp <= 0:
            result["failure_reason"] = f"Tp invalid: {Tp}"
            return result
        result["Tp"] = float(Tp)
    except Exception as e:
        result["failure_reason"] = f"Tp computation failed: {e}"
        return result

    try:
        alpha = model.get_alpha()
        if alpha is None or not np.isfinite(alpha) or alpha <= 0:
            result["failure_reason"] = f"alpha invalid: {alpha}"
            return result
        result["alpha"] = float(alpha)
    except Exception as e:
        result["failure_reason"] = f"alpha computation failed: {e}"
        return result

    try:
        beta_H = model.get_beta_H()
        if beta_H is None or not np.isfinite(beta_H) or beta_H <= 0:
            result["failure_reason"] = f"beta_H invalid: {beta_H}"
            return result
        result["beta_H"] = float(beta_H)
    except Exception as e:
        result["failure_reason"] = f"beta_H computation failed: {e}"
        return result

    try:
        Tr = model.get_Tr()
        if Tr is None or not np.isfinite(Tr) or Tr <= 0:
            result["failure_reason"] = f"Tr invalid: {Tr}"
            return result
        result["Tr"] = float(Tr)
    except Exception as e:
        result["failure_reason"] = f"Tr computation failed: {e}"
        return result

    try:
        eternal = model.get_check_eternal_inflation()
        if np.isscalar(eternal):
            result["eternal_inflation"] = bool(eternal)
        else:
            result["eternal_inflation"] = bool(eternal.item())
    except Exception as e:
        result["eternal_inflation"] = None
        result["failure_reason"] = f"eternal inflation check failed: {e}"
        return result

    # Compute f_peak estimate
    if result["eternal_inflation"]:
        result["status"] = "physical_failure"
        result["failure_reason"] = "eternal inflation occurs"
        return result

    try:
        gstar_eff = model.get_gstar_eff(Tr)
        if np.isfinite(gstar_eff) and gstar_eff > 0:
            f_peak = 1.6e-5 * beta_H * (Tr / 100.0) * (gstar_eff / 100.0) ** (1.0 / 6.0)
            result["f_peak_est"] = float(f_peak)
        else:
            # Fallback with g* ~ 10 (typical for MeV-scale)
            f_peak = 1.6e-5 * beta_H * (Tr / 100.0) * (10.0 / 100.0) ** (1.0 / 6.0)
            result["f_peak_est"] = float(f_peak)
    except Exception as e:
        result["failure_reason"] = f"f_peak estimate failed: {e}"
        return result

    # All checks passed
    result["status"] = "viable"
    result["failure_reason"] = ""
    return result


def smoke_test():
    """Run a smoke test on a known benchmark point.

    Uses parameters close to arXiv:2501.11619:
        g_D = 0.59, v = 0.182 GeV (M_A' = 107.3 MeV)
    """
    print("=" * 60)
    print("FOPT Model Smoke Test")
    print("=" * 60)

    # Test point 1: from 2501.11619 (g_D=0.59, v=182 MeV -> 0.182 GeV)
    v_test = 0.182
    g_D_test = 0.59

    print(f"\nTest point: v = {v_test:.4f} GeV, g_D = {g_D_test:.4f}")
    print(f"  Expected: M_A' = {g_D_test * v_test:.4f} GeV (107.3 MeV = 0.1073 GeV)")
    print(f"  Expected: m_rho = sqrt(3/8) * {g_D_test}^2 * {v_test} / pi")

    dep = compute_dependent_params(v_test, g_D_test)
    print(f"  m_A'  = {dep['m_A_prime']:.6f} GeV")
    print(f"  m_rho = {dep['m_rho']:.6f} GeV")
    print(f"  beta_lambda = {dep['beta_lambda']:.6e}")

    result = compute_fopt(v_test, g_D_test)
    print(f"\n  Status: {result['status']}")
    if result["status"] == "viable":
        print(f"  Tn    = {result['Tn']:.6e} GeV")
        print(f"  Tp    = {result['Tp']:.6e} GeV")
        print(f"  Tr    = {result['Tr']:.6e} GeV")
        print(f"  alpha = {result['alpha']:.4e}")
        print(f"  beta/H = {result['beta_H']:.4f}")
        print(f"  f_peak_est = {result['f_peak_est']:.4e} Hz")
        print(f"  Eternal inflation = {result['eternal_inflation']}")
    else:
        print(f"  Failure: {result['failure_reason']}")

    # Test point 2: from 2502.19478 Point A (v=92.9 MeV, g_D=0.877)
    v_test2 = 0.0929
    g_D_test2 = 0.877

    print(f"\nTest point 2: v = {v_test2:.4f} GeV, g_D = {g_D_test2:.4f}")

    dep2 = compute_dependent_params(v_test2, g_D_test2)
    print(f"  m_A'  = {dep2['m_A_prime']:.6f} GeV")
    print(f"  m_rho = {dep2['m_rho']:.6f} GeV")
    print(f"  beta_lambda = {dep2['beta_lambda']:.6e}")

    result2 = compute_fopt(v_test2, g_D_test2)
    print(f"\n  Status: {result2['status']}")
    if result2["status"] == "viable":
        print(f"  Tn    = {result2['Tn']:.6e} GeV")
        print(f"  Tp    = {result2['Tp']:.6e} GeV")
        print(f"  Tr    = {result2['Tr']:.6e} GeV")
        print(f"  alpha = {result2['alpha']:.4e}")
        print(f"  beta/H = {result2['beta_H']:.4f}")
        print(f"  f_peak_est = {result2['f_peak_est']:.4e} Hz")
        print(f"  Eternal inflation = {result2['eternal_inflation']}")
    else:
        print(f"  Failure: {result2['failure_reason']}")

    # Test point 3: from 2501.15649 BP1 (v=0.5 GeV, g_D=0.75)
    v_test3 = 0.5
    g_D_test3 = 0.75

    print(f"\nTest point 3: v = {v_test3:.4f} GeV, g_D = {g_D_test3:.4f}")

    dep3 = compute_dependent_params(v_test3, g_D_test3)
    print(f"  m_A'  = {dep3['m_A_prime']:.6f} GeV")
    print(f"  m_rho = {dep3['m_rho']:.6f} GeV")

    result3 = compute_fopt(v_test3, g_D_test3)
    print(f"\n  Status: {result3['status']}")
    if result3["status"] == "viable":
        print(f"  Tn    = {result3['Tn']:.6e} GeV")
        print(f"  Tp    = {result3['Tp']:.6e} GeV")
        print(f"  Tr    = {result3['Tr']:.6e} GeV")
        print(f"  alpha = {result3['alpha']:.4e}")
        print(f"  beta/H = {result3['beta_H']:.4f}")
        print(f"  f_peak_est = {result3['f_peak_est']:.4e} Hz")
        print(f"  Eternal inflation = {result3['eternal_inflation']}")
    else:
        print(f"  Failure: {result3['failure_reason']}")

    print("\n" + "=" * 60)
    print("Smoke test complete.")
    print("=" * 60)


if __name__ == "__main__":
    smoke_test()