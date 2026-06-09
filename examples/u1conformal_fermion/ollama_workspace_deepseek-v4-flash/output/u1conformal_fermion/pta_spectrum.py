"""
pta_spectrum.py -- Gravitational-wave spectrum for the conformal U(1)_D dark sector.

Template choice: "dbf" (dissipative bulk flow) from Lewicki & Vaskonen (2025), arXiv:2511.15687.

Rationale:
- The FOPT parameters for this model show very large alpha ~ 10^4 (strongly supercooled),
  beta/H ~ 42, and runaway bubble walls (v_w ~ 1).
- The "higgsless" template (arXiv:2209.04369) is designed for sound waves in weak-to-intermediate
  phase transitions (alpha ~ 0.005-0.5) and is not valid for strongly supercooled transitions.
- The "dbf" (dissipative bulk flow) template from Lewicki & Vaskonen (2025) is specifically
  designed for strongly supercooled transitions with alpha >> 1 and ultra-relativistic walls.
- The "bf" (bulk flow) template is also valid but the "dbf" template includes dissipative effects
  that are relevant for the moderate beta/H ~ 42 regime.

Caveats:
- The dbf template assumes thin-wall, ultra-relativistic bubble expansion (v_w ~ 1), which is
  consistent with the runaway regime expected for strongly supercooled transitions.
- The template was calibrated for beta/H in the range ~4 to >100, which covers our beta/H ~ 42.
- The template assumes the vacuum energy dominates before the transition (alpha >> 1), which
  is satisfied by our alpha ~ 10^4.
"""

import sys
import os
import numpy as np

# Add backend directory to path
_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from spectrum import Spectrum


def get_spectrum(f, Treh, alpha, beta_H, template="dbf", ksw=1.0):
    """
    Compute the gravitational-wave spectrum h^2 Omega_GW(f) for given FOPT parameters.

    Parameters
    ----------
    f : array_like
        Frequency array in Hz.
    Treh : float
        Reheating temperature in GeV.
    alpha : float
        Phase transition strength parameter.
    beta_H : float
        Inverse duration parameter (beta/H).
    template : str, optional
        Spectrum template: "dbf" (dissipative bulk flow), "bf" (bulk flow), or "higgsless".
    ksw : float, optional
        Sound wave efficiency factor (default 1.0).

    Returns
    -------
    ndarray
        h^2 Omega_GW(f) values.
    """
    # Validate inputs
    if not np.isfinite(Treh) or Treh <= 0:
        return np.zeros_like(np.asarray(f, dtype=float))
    if not np.isfinite(alpha) or alpha <= 0:
        return np.zeros_like(np.asarray(f, dtype=float))
    if not np.isfinite(beta_H) or beta_H <= 0:
        return np.zeros_like(np.asarray(f, dtype=float))

    spectrum = Spectrum(template=template)
    h2OmegaGW = spectrum.get_h2OmegaGW(f, Treh, alpha, beta_H, ksw=ksw)

    # Ensure non-negative
    h2OmegaGW = np.maximum(h2OmegaGW, 0.0)

    return h2OmegaGW


def compute_spectrum_for_point(f, g_D, y_psi, v, template="dbf"):
    """
    Compute the GW spectrum for a given model parameter point.

    This function builds the model, computes FOPT parameters, and returns the spectrum.

    Parameters
    ----------
    f : array_like
        Frequency array in Hz.
    g_D : float
        Dark gauge coupling.
    y_psi : float
        Yukawa coupling.
    v : float
        Dark Higgs vev in GeV.
    template : str, optional
        Spectrum template.

    Returns
    -------
    dict
        Dictionary with keys: 'f', 'h2OmegaGW', 'alpha', 'beta_H', 'Treh', 'Tp', 'Tn',
        and dependent parameters.
    """
    # Import the FOPT model
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from fopt_model import compute_fopt, is_viable

    # Compute FOPT parameters
    result = compute_fopt(g_D, y_psi, v)

    if not is_viable(result):
        return {
            "f": np.asarray(f),
            "h2OmegaGW": np.zeros_like(np.asarray(f, dtype=float)),
            "alpha": result.get("alpha", np.nan),
            "beta_H": result.get("beta_H", np.nan),
            "Treh": result.get("Treh", np.nan),
            "Tp": result.get("Tp", np.nan),
            "Tn": result.get("Tn", np.nan),
            "viable": False,
        }

    # Compute spectrum
    h2OmegaGW = get_spectrum(
        np.asarray(f, dtype=float),
        result["Treh"],
        result["alpha"],
        result["beta_H"],
        template=template,
    )

    return {
        "f": np.asarray(f),
        "h2OmegaGW": h2OmegaGW,
        "alpha": result["alpha"],
        "beta_H": result["beta_H"],
        "Treh": result["Treh"],
        "Tp": result["Tp"],
        "Tn": result["Tn"],
        "viable": True,
    }
