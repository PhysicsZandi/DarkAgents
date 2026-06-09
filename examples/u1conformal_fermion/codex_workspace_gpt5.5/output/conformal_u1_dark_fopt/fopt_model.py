"""FOPT wrapper for the conformal U(1)_D dark-sector model.

Independent parameters are v_D [GeV], g_D, and y_D.  The Coleman-Weinberg
dependent quantities are computed at every point and lambda_D is never scanned.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from semianalytic_pipeline import SemiAnalyticPipeline, gstar  # noqa: E402


PTA_F_MIN_HZ = 1.0e-9
PTA_F_MAX_HZ = 1.0e-7
MAX_PERTURBATIVE_COUPLING = math.sqrt(4.0 * math.pi)


@dataclass(frozen=True)
class DependentParameters:
    gb_X: float
    gf_psi: float
    beta_lambda: float
    m_X_GeV: float
    m_psi_GeV: float
    m_chi_GeV: float


def compute_dependent(v_D: float, g_D: float, y_D: float) -> DependentParameters:
    gb_X = 2.0 * g_D
    gf_psi = y_D / math.sqrt(2.0)
    beta_lambda = (3.0 * gb_X**4 - 4.0 * gf_psi**4) / (8.0 * math.pi**2)
    m_chi_sq = beta_lambda * v_D**2
    return DependentParameters(
        gb_X=gb_X,
        gf_psi=gf_psi,
        beta_lambda=beta_lambda,
        m_X_GeV=gb_X * v_D,
        m_psi_GeV=gf_psi * v_D,
        m_chi_GeV=math.sqrt(m_chi_sq) if m_chi_sq > 0.0 else math.nan,
    )


def validate_inputs(v_D: float, g_D: float, y_D: float) -> str | None:
    values = (v_D, g_D, y_D)
    if not all(np.isfinite(values)):
        return "nonfinite_input"
    if v_D <= 0.0:
        return "nonpositive_v_D"
    if g_D <= 0.0:
        return "nonpositive_g_D"
    if y_D < 0.0:
        return "negative_y_D"
    if g_D >= MAX_PERTURBATIVE_COUPLING or y_D >= MAX_PERTURBATIVE_COUPLING:
        return "nonperturbative_coupling"
    dep = compute_dependent(v_D, g_D, y_D)
    if not np.isfinite(dep.beta_lambda) or dep.beta_lambda <= 0.0:
        return "nonpositive_beta_lambda"
    return None


def make_backend(v_D: float, g_D: float, y_D: float, verbose: bool = False) -> SemiAnalyticPipeline:
    dep = compute_dependent(v_D, g_D, y_D)
    return SemiAnalyticPipeline(
        chi0=v_D,
        boson_gbs={"X_mu": dep.gb_X},
        boson_dofs={"X_mu": 3},
        fermion_gfs={"psi_degenerate_majorana_pair": dep.gf_psi},
        fermion_dofs={"psi_degenerate_majorana_pair": 4},
        verbose=verbose,
    )


def estimate_f_peak(beta_H: float, Treh: float) -> float:
    g_eff = float(gstar(Treh))
    return 1.6e-5 * beta_H * (Treh / 100.0) * (g_eff / 100.0) ** (1.0 / 6.0)


def evaluate_point(v_D: float, g_D: float, y_D: float, verbose: bool = False) -> dict[str, Any]:
    failure = validate_inputs(v_D, g_D, y_D)
    dep = compute_dependent(v_D, g_D, y_D) if all(np.isfinite((v_D, g_D, y_D))) else None
    base: dict[str, Any] = {
        "v_D": float(v_D),
        "g_D": float(g_D),
        "y_D": float(y_D),
        "status": "physical_failure" if failure else "numerical_failure",
        "failure_reason": failure or "",
    }
    if dep is not None:
        base.update(asdict(dep))
    if failure:
        return base

    model = make_backend(v_D, g_D, y_D, verbose=verbose)
    Tn = float(model.get_Tn())
    Tp = float(model.get_Tp())
    Treh = float(model.get_Tr())
    alpha = float(model.get_alpha())
    beta_H = float(model.get_beta_H())
    eternal_inflation = model.get_check_eternal_inflation()
    f_peak_est = estimate_f_peak(beta_H, Treh) if np.isfinite((beta_H, Treh)).all() else math.nan

    base.update(
        {
            "Tn": Tn,
            "Tp": Tp,
            "Treh": Treh,
            "alpha": alpha,
            "beta_H": beta_H,
            "f_peak_est": float(f_peak_est),
            "eternal_inflation": bool(eternal_inflation) if isinstance(eternal_inflation, bool) else eternal_inflation,
            "gstar_Treh": float(gstar(Treh)) if np.isfinite(Treh) and Treh > 0.0 else math.nan,
        }
    )

    required = (Tn, Tp, Treh, alpha, beta_H, f_peak_est)
    if not all(np.isfinite(required)):
        base["status"] = "numerical_failure"
        base["failure_reason"] = "nonfinite_backend_output"
    elif Tn <= 0.0 or Tp <= 0.0 or Treh <= 0.0 or alpha <= 0.0 or beta_H <= 0.0:
        base["status"] = "physical_failure"
        base["failure_reason"] = "nonpositive_transition_observable"
    elif eternal_inflation is True:
        base["status"] = "not_fopt"
        base["failure_reason"] = "eternal_inflation"
    else:
        base["status"] = "viable"
        base["failure_reason"] = ""
    return base


if __name__ == "__main__":
    smoke = evaluate_point(v_D=0.173, g_D=0.34, y_D=0.224)
    print(smoke)
