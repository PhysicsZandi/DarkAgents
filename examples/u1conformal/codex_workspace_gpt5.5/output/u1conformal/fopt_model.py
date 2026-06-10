"""FOPT wrapper for the minimal conformal U(1)_D model.

The independent scan parameters are v [GeV] and g_D.  All other model
quantities are Coleman-Weinberg/backend-dependent diagnostics.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np


MODEL = "u1conformal"
BRANCH = "fopt-pta"
PTA_FREQUENCY_BAND_HZ = (1.0e-9, 1.0e-7)
PERTURBATIVE_G_MAX = math.sqrt(4.0 * math.pi)
PERTURBATIVE_BETA_LAMBDA_MAX = 1.0

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from semianalytic_pipeline import SemiAnalyticPipeline  # noqa: E402


@dataclass
class FOPTPoint:
    v: float
    g_D: float
    lambda_Phi: float | None
    beta_lambda: float | None
    m_Aprime: float | None
    m_rho: float | None
    Tn: float | None
    Tp: float | None
    Treh: float | None
    alpha: float | None
    beta_H: float | None
    g_star: float | None
    f_peak_est: float | None
    eternal_inflation: bool | None
    status: str
    failure_reason: str


def _as_float(value: Any) -> float | None:
    try:
        out = float(value)
    except Exception:
        return None
    if not math.isfinite(out):
        return None
    return out


def _positive_finite(value: Any) -> bool:
    out = _as_float(value)
    return out is not None and out > 0.0


def beta_lambda(g_D: float) -> float:
    """Gauge-only Coleman-Weinberg beta coefficient in the backend convention."""
    return 3.0 * g_D**4 / (8.0 * math.pi**2)


def dependent_parameters(v: float, g_D: float) -> dict[str, float | None]:
    """Return dependent quantities; lambda_Phi is backend-fixed but not exported."""
    beta = beta_lambda(g_D)
    return {
        "lambda_Phi": None,
        "beta_lambda": beta,
        "m_Aprime": g_D * v,
        "m_rho": math.sqrt(beta) * v if beta > 0.0 else None,
    }


def perturbativity_failure(v: float, g_D: float) -> str | None:
    if not math.isfinite(v) or v <= 0.0:
        return "non-positive or non-finite v"
    if not math.isfinite(g_D) or g_D <= 0.0:
        return "non-positive or non-finite g_D"
    if g_D >= PERTURBATIVE_G_MAX:
        return f"perturbativity failure: g_D={g_D:.6g} >= sqrt(4*pi)"
    beta = beta_lambda(g_D)
    if beta >= PERTURBATIVE_BETA_LAMBDA_MAX:
        return f"perturbativity failure: beta_lambda={beta:.6g} >= 1"
    return None


def build_backend(v: float, g_D: float, verbose: bool = False) -> SemiAnalyticPipeline:
    return SemiAnalyticPipeline(
        chi0=v,
        boson_gbs={"Aprime": g_D},
        boson_dofs={"Aprime": 3},
        fermion_gfs={},
        fermion_dofs={},
        verbose=verbose,
    )


def _load_gstar_table() -> tuple[np.ndarray, np.ndarray]:
    table = np.loadtxt(BACKEND_DIR / "T_vs_g_gs_GeV.csv", delimiter=",", dtype=float)
    order = np.argsort(table[:, 0])
    return table[order, 0], table[order, 1]


def gstar_sm(T_gev: float) -> float | None:
    """Interpolate the SM g_* table, clamping outside the tabulated range."""
    T = _as_float(T_gev)
    if T is None or T <= 0.0:
        return None
    x, y = _load_gstar_table()
    logT = math.log10(T)
    logx = np.log10(x)
    return float(np.interp(logT, logx, y, left=y[0], right=y[-1]))


def estimate_f_peak(beta_H: float, Treh: float, g_star: float) -> float | None:
    if not (_positive_finite(beta_H) and _positive_finite(Treh) and _positive_finite(g_star)):
        return None
    return 1.6e-5 * beta_H * (Treh / 100.0) * (g_star / 100.0) ** (1.0 / 6.0)


def evaluate_point(v: float, g_D: float, verbose: bool = False) -> FOPTPoint:
    deps = dependent_parameters(v, g_D)
    failure = perturbativity_failure(v, g_D)
    if failure:
        return FOPTPoint(v, g_D, **deps, Tn=None, Tp=None, Treh=None, alpha=None, beta_H=None,
                         g_star=None, f_peak_est=None, eternal_inflation=None,
                         status="physical_failure", failure_reason=failure)

    try:
        model = build_backend(v, g_D, verbose=verbose)
        Tn = _as_float(model.get_Tn())
        if Tn is None or Tn <= 0.0:
            return FOPTPoint(v, g_D, **deps, Tn=Tn, Tp=None, Treh=None, alpha=None, beta_H=None,
                             g_star=None, f_peak_est=None, eternal_inflation=None,
                             status="not_fopt", failure_reason="nucleation failure: non-finite or non-positive Tn")

        Tp = _as_float(model.get_Tp())
        if Tp is None or Tp <= 0.0:
            return FOPTPoint(v, g_D, **deps, Tn=Tn, Tp=Tp, Treh=None, alpha=None, beta_H=None,
                             g_star=None, f_peak_est=None, eternal_inflation=None,
                             status="not_fopt", failure_reason="percolation failure: non-finite or non-positive Tp")

        alpha = _as_float(model.get_alpha())
        beta_h = _as_float(model.get_beta_H())
        Treh = _as_float(model.get_Tr())
        eternal = model.get_check_eternal_inflation()
        eternal_bool = bool(eternal) if isinstance(eternal, (bool, np.bool_)) else None
        g_star = gstar_sm(Treh) if Treh is not None else None
        f_peak = estimate_f_peak(beta_h, Treh, g_star) if g_star is not None else None

        checks = {
            "alpha": alpha,
            "beta_H": beta_h,
            "Treh": Treh,
        }
        bad = [name for name, value in checks.items() if not _positive_finite(value)]
        if bad:
            return FOPTPoint(v, g_D, **deps, Tn=Tn, Tp=Tp, Treh=Treh, alpha=alpha, beta_H=beta_h,
                             g_star=g_star, f_peak_est=f_peak, eternal_inflation=eternal_bool,
                             status="physical_failure",
                             failure_reason="non-finite or non-positive " + ", ".join(bad))
        if eternal_bool is True:
            return FOPTPoint(v, g_D, **deps, Tn=Tn, Tp=Tp, Treh=Treh, alpha=alpha, beta_H=beta_h,
                             g_star=g_star, f_peak_est=f_peak, eternal_inflation=eternal_bool,
                             status="physical_failure", failure_reason="eternal inflation")
        if eternal_bool is None:
            return FOPTPoint(v, g_D, **deps, Tn=Tn, Tp=Tp, Treh=Treh, alpha=alpha, beta_H=beta_h,
                             g_star=g_star, f_peak_est=f_peak, eternal_inflation=eternal_bool,
                             status="physical_failure",
                             failure_reason="eternal-inflation check returned non-finite value")

        return FOPTPoint(v, g_D, **deps, Tn=Tn, Tp=Tp, Treh=Treh, alpha=alpha, beta_H=beta_h,
                         g_star=g_star, f_peak_est=f_peak, eternal_inflation=eternal_bool,
                         status="viable", failure_reason="")
    except Exception as exc:
        return FOPTPoint(v, g_D, **deps, Tn=None, Tp=None, Treh=None, alpha=None, beta_H=None,
                         g_star=None, f_peak_est=None, eternal_inflation=None,
                         status="numerical_failure",
                         failure_reason=f"backend exception: {type(exc).__name__}: {exc}")


def point_to_dict(point: FOPTPoint) -> dict[str, Any]:
    out = asdict(point)
    for key, value in list(out.items()):
        if isinstance(value, float) and not math.isfinite(value):
            out[key] = None
    return out


def smoke_test() -> dict[str, Any]:
    point = evaluate_point(v=0.173, g_D=0.677)
    return point_to_dict(point)


if __name__ == "__main__":
    print(json.dumps(smoke_test(), indent=2, sort_keys=True))
