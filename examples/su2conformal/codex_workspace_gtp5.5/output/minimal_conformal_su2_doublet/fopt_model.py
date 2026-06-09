"""FOPT implementation for minimal_conformal_su2_doublet.

The independent parameters are gD and vD.  The backend mapping follows the
critic-authoritative convention m_WD(chi) = gD * chi / 2.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path


MODEL_DIR = Path(__file__).resolve().parent
PROJECT_DIR = MODEL_DIR.parents[1]
BACKEND_DIR = PROJECT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from semianalytic_pipeline import SemiAnalyticPipeline  # noqa: E402


PTA_F_MIN_HZ = 1.0e-9
PTA_F_MAX_HZ = 1.0e-7
MAX_PERTURBATIVE_GD = math.sqrt(4.0 * math.pi)


def _finite_positive(*values: float) -> bool:
    return all(math.isfinite(float(value)) and float(value) > 0.0 for value in values)


def gstar_from_backend(model: SemiAnalyticPipeline, temperature_gev: float) -> float:
    value = float(model.get_gstar_eff(temperature_gev))
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"non-positive or non-finite gstar_eff at T={temperature_gev}: {value}")
    return value


def f_peak_estimate_hz(beta_H: float, Treh_gev: float, gstar_eff: float) -> float:
    return 1.6e-5 * beta_H * (Treh_gev / 100.0) * (gstar_eff / 100.0) ** (1.0 / 6.0)


def build_model(gD: float, vD: float, verbose: bool = False) -> SemiAnalyticPipeline:
    gD = float(gD)
    vD = float(vD)
    if not (math.isfinite(gD) and math.isfinite(vD)):
        raise ValueError("gD and vD must be finite")
    if gD <= 0.0 or vD <= 0.0:
        raise ValueError("gD and vD must be positive")
    if gD >= MAX_PERTURBATIVE_GD:
        raise ValueError(f"gD={gD} violates perturbativity guard gD < sqrt(4*pi)")

    return SemiAnalyticPipeline(
        chi0=vD,
        boson_gbs={"W_D": gD / 2.0},
        boson_dofs={"W_D": 9},
        fermion_gfs={},
        fermion_dofs={},
        verbose=verbose,
    )


def evaluate_point(gD: float, vD: float, verbose: bool = False) -> dict:
    model = build_model(gD, vD, verbose=verbose)

    Tn = float(model.get_Tn())
    Tp = float(model.get_Tp())
    alpha = float(model.get_alpha())
    beta_H = float(model.get_beta_H())
    Treh = float(model.get_Tr())
    eternal_inflation = model.get_check_eternal_inflation()
    beta_lambda = float(model.get_beta_lambda())
    m_chi = float(model.get_scalar_mass())
    m_WD = float(gD * vD / 2.0)
    gstar_eff = gstar_from_backend(model, Treh if math.isfinite(Treh) and Treh > 0 else Tp)
    f_peak_est = f_peak_estimate_hz(beta_H, Treh, gstar_eff)

    percolation_checked = math.isfinite(Tp)
    eternal_inflation_checked = isinstance(eternal_inflation, bool)
    viable = (
        _finite_positive(Tn, Tp, alpha, beta_H, Treh, f_peak_est, beta_lambda, m_chi, m_WD)
        and percolation_checked
        and eternal_inflation_checked
        and not eternal_inflation
    )

    if viable:
        status = "viable"
        failure_reason = ""
    elif eternal_inflation is True:
        status = "physical_failure"
        failure_reason = "eternal_inflation"
    elif not _finite_positive(Tn, Tp, alpha, beta_H, Treh):
        status = "not_fopt"
        failure_reason = "missing_finite_positive_transition_observables"
    else:
        status = "physical_failure"
        failure_reason = "failed_viability_checks"

    return {
        "gD": float(gD),
        "vD": float(vD),
        "m_WD": m_WD,
        "gb_WD": float(gD / 2.0),
        "beta_lambda": beta_lambda,
        "m_chi": m_chi,
        "Tn": Tn,
        "Tp": Tp,
        "Treh": Treh,
        "alpha": alpha,
        "beta_H": beta_H,
        "gstar_eff": gstar_eff,
        "f_peak_est": f_peak_est,
        "eternal_inflation": eternal_inflation,
        "percolation_checked": percolation_checked,
        "perturbativity_checked": True,
        "status": status,
        "failure_reason": failure_reason,
        "in_pta_band_est": bool(PTA_F_MIN_HZ <= f_peak_est <= PTA_F_MAX_HZ)
        if math.isfinite(f_peak_est)
        else False,
    }


def smoke_test() -> dict:
    gD = 1.37
    m_zd_gev = 8.23e-3
    vD = 2.0 * m_zd_gev / gD
    return evaluate_point(gD, vD)


if __name__ == "__main__":
    result = smoke_test()
    keys = ("gD", "vD", "Tn", "Tp", "Treh", "alpha", "beta_H", "f_peak_est", "status")
    for key in keys:
        print(f"{key}: {result[key]}")
