"""
FOPT model implementation: classically scale-invariant dark U(1)_D (u1conformal).

Backend: backend/semianalytic_pipeline.py (semianalytic_pipeline).

Model: complex scalar Phi (charge +1) + dark gauge boson A', Coleman-Weinberg
radiative symmetry breaking, classically scale-invariant (no tree mass term).

Independent scan parameters:
  - v   : dark-sector vev [GeV]
  - g_D : U(1)_D gauge coupling

Dependent quantities (computed internally / as diagnostics, NOT scanned):
  - lambda_Phi : CW-fixed scalar quartic (handled internally by backend)
  - m_A'   = g_D * v
  - m_rho  = sqrt(beta_lambda) * v,  beta_lambda = 3 g_D^4 / (8 pi^2)

Backend mapping (single-field scale-invariant):
  chi0 = v, boson_gbs = {"Aprime": g_D}, boson_dofs = {"Aprime": 3},
  empty fermion dicts. Scalar/Goldstone excluded (computed internally).
  m_A'/v = g_D, so gb_gauge = g_D.
"""

import os
import sys
import numpy as np

# Make the backend importable
_BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "backend")
)
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from semianalytic_pipeline import SemiAnalyticPipeline, gstar  # noqa: E402

# Physical / scan guards
G_D_MAX = np.sqrt(4 * np.pi)  # perturbativity bound on the gauge coupling

# PTA band (Hz) for f_peak anchoring (order of magnitude)
PTA_FMIN = 1e-9
PTA_FMAX = 1e-7


def dependent_parameters(v, g_D):
    """Return dependent diagnostics from independent (v, g_D)."""
    beta_lambda = 3.0 * g_D**4 / (8.0 * np.pi**2)
    m_Aprime = g_D * v
    m_rho = np.sqrt(beta_lambda) * v
    return {
        "beta_lambda": beta_lambda,
        "m_Aprime_GeV": m_Aprime,
        "m_rho_GeV": m_rho,
    }


def build_model(v, g_D, verbose=False):
    """Instantiate the backend pipeline for given independent parameters."""
    boson_gbs = {"Aprime": g_D}  # m_A'/v = g_D
    boson_dofs = {"Aprime": 3}   # massive vector
    fermion_gfs = {}
    fermion_dofs = {}
    return SemiAnalyticPipeline(
        chi0=float(v),
        boson_gbs=boson_gbs,
        boson_dofs=boson_dofs,
        fermion_gfs=fermion_gfs,
        fermion_dofs=fermion_dofs,
        verbose=verbose,
    )


def estimate_f_peak(beta_H, Treh_GeV):
    """
    Template-independent, order-of-magnitude redshifted peak frequency [Hz]:
      f_peak ~ 1.6e-5 Hz * (beta/H) * (Treh/100 GeV) * (g_*/100)^(1/6)
    g_* read at Treh from the backend table.
    This is NOT the true spectral peak; it only anchors the scale for the PTA agent.
    """
    if not (np.isfinite(beta_H) and np.isfinite(Treh_GeV)) or Treh_GeV <= 0:
        return np.nan
    gs = float(gstar(Treh_GeV))
    return 1.6e-5 * beta_H * (Treh_GeV / 100.0) * (gs / 100.0) ** (1.0 / 6.0)


def physical_guards(v, g_D):
    """Enforce physical scan bounds. Return (ok, reason)."""
    if not (np.isfinite(v) and np.isfinite(g_D)):
        return False, "non_finite_input"
    if v <= 0:
        return False, "non_positive_vev"
    if g_D <= 0:
        return False, "non_positive_coupling"
    if g_D > G_D_MAX:
        return False, "non_perturbative_coupling"
    return True, ""


def evaluate_point(v, g_D, verbose=False):
    """
    Evaluate one (v, g_D) point. Returns a dict of results with a status label:
      viable | physical_failure | numerical_failure | not_fopt
    """
    dep = dependent_parameters(v, g_D)
    result = {
        "v": float(v),
        "g_D": float(g_D),
        "lambda_Phi": np.nan,  # CW-fixed internally by the backend
        "beta_lambda": dep["beta_lambda"],
        "m_Aprime_GeV": dep["m_Aprime_GeV"],
        "m_rho_GeV": dep["m_rho_GeV"],
        "Tn": np.nan,
        "Tp": np.nan,
        "Treh": np.nan,
        "alpha": np.nan,
        "beta_H": np.nan,
        "eternal_inflation": None,
        "f_peak_est": np.nan,
        "status": "numerical_failure",
        "failure_reason": "",
    }

    ok, reason = physical_guards(v, g_D)
    if not ok:
        result["status"] = "physical_failure"
        result["failure_reason"] = reason
        return result

    try:
        model = build_model(v, g_D, verbose=verbose)
        Tn = model.get_Tn()
        Tp = model.get_Tp()
        alpha = model.get_alpha()
        beta_H = model.get_beta_H()
        Treh = model.get_Tr()
        eternal = model.get_check_eternal_inflation()
    except Exception as e:  # backend failure / non-convergence
        result["failure_reason"] = f"backend_exception: {type(e).__name__}: {e}"
        return result

    result["Tn"] = float(Tn) if Tn is not None else np.nan
    result["Tp"] = float(Tp) if Tp is not None else np.nan
    result["alpha"] = float(alpha) if alpha is not None else np.nan
    result["beta_H"] = float(beta_H) if beta_H is not None else np.nan
    result["Treh"] = float(Treh) if Treh is not None else np.nan
    result["eternal_inflation"] = eternal

    # Finiteness check
    vals = [result["Tn"], result["Tp"], result["alpha"],
            result["beta_H"], result["Treh"]]
    if not all(np.isfinite(x) for x in vals):
        result["status"] = "not_fopt"
        result["failure_reason"] = "non_finite_observable (no FOPT found / bracket fail)"
        return result

    # Physical positivity
    if not (result["Tn"] > 0 and result["Tp"] > 0 and result["Treh"] > 0
            and result["alpha"] > 0 and result["beta_H"] > 0):
        result["status"] = "physical_failure"
        result["failure_reason"] = "non_positive_observable"
        return result

    # Eternal inflation guard
    if eternal is True:
        result["status"] = "physical_failure"
        result["failure_reason"] = "eternal_inflation"
        return result
    if eternal is not False:
        result["status"] = "numerical_failure"
        result["failure_reason"] = "eternal_inflation_check_failed"
        return result

    result["f_peak_est"] = estimate_f_peak(result["beta_H"], result["Treh"])
    result["status"] = "viable"
    return result


def _smoke_test():
    """Smoke test on a literature-anchored benchmark (2502.19478 Point A)."""
    v = 0.173  # GeV
    g_D = 0.677
    print("Smoke test: u1conformal FOPT model (v=173 MeV, g_D=0.677)")
    res = evaluate_point(v, g_D, verbose=False)
    for k in ["v", "g_D", "m_Aprime_GeV", "m_rho_GeV", "beta_lambda",
              "Tn", "Tp", "Treh", "alpha", "beta_H", "eternal_inflation",
              "f_peak_est", "status", "failure_reason"]:
        print(f"  {k:18s}: {res[k]}")
    assert res["status"] in (
        "viable", "physical_failure", "numerical_failure", "not_fopt"
    )
    return res


if __name__ == "__main__":
    _smoke_test()
