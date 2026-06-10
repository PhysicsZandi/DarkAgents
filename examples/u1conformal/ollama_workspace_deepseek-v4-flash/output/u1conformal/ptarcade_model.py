"""
PTArcade model file for the Dark U(1)_D conformal model.

Independent parameters:
- v: scalar vev in GeV (log-uniform prior)
- g_D: U(1)_D gauge coupling (uniform prior)

The spectrum is computed using the FOPT model (SemiAnalyticPipeline) and the
selected GW spectrum template ("dbf" - dissipative bulk flow).
"""
import sys
import os
import numpy as np
from pathlib import Path

# Add backend and model directories to path
_backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

_model_dir = os.path.dirname(os.path.abspath(__file__))
if _model_dir not in sys.path:
    sys.path.insert(0, _model_dir)

from ptarcade.models_utils import prior
from fopt_model import compute_fopt
from spectrum import Spectrum

# ---------------------------------------------------------------------------
# PTArcade requires: parameters dict, spectrum function
# ---------------------------------------------------------------------------

# Priors on independent model parameters
# v: scalar vev in GeV (log-uniform over [5e-4, 50] GeV)
#   Wide enough to cover the PTA-compatible region v ~ [0.01, 10] GeV
#   with margin on both sides
# g_D: dimensionless gauge coupling (uniform over [0.3, 1.5])
#   Wide enough to cover PTA-compatible region g_D ~ [0.49, 0.85]
#   with margin on both sides

parameters = {
    "log10_v": prior("Uniform", np.log10(5e-4), np.log10(50.0)),
    "g_D": prior("Uniform", 0.3, 1.5),
}

# Spectrum template: "dbf" (dissipative bulk flow)
TEMPLATE = "dbf"


def spectrum(f, log10_v, g_D):
    """
    Compute the stochastic GW spectrum at given frequencies.

    Parameters
    ----------
    f : ndarray
        Frequency array in Hz.
    log10_v : float or array
        log10(v) where v is the scalar vev in GeV.
    g_D : float or array
        U(1)_D gauge coupling.

    Returns
    -------
    h2OmegaGW : ndarray
        h^2 * Omega_GW values at frequencies f.
    """
    # PTArcade passes parameters as arrays; extract scalar values
    log10_v = float(np.asarray(log10_v).item()
                    if np.asarray(log10_v).size == 1
                    else np.asarray(log10_v).flat[0])
    g_D = float(np.asarray(g_D).item()
                if np.asarray(g_D).size == 1
                else np.asarray(g_D).flat[0])

    v = 10.0 ** log10_v

    # Physical guards
    if v <= 0 or g_D <= 0:
        return np.zeros_like(f, dtype=float)

    # Compute FOPT parameters
    fopt_result = compute_fopt(v, g_D)

    if fopt_result["status"] != "viable":
        return np.zeros_like(f, dtype=float)

    alpha = fopt_result["alpha"]
    beta_H = fopt_result["beta_H"]
    Tr = fopt_result["Tr"]

    # Validate FOPT outputs
    if not (np.isfinite(alpha) and np.isfinite(beta_H) and np.isfinite(Tr)
            and alpha > 0 and beta_H > 0 and Tr > 0):
        return np.zeros_like(f, dtype=float)

    # Compute GW spectrum
    spectrum_obj = Spectrum(template=TEMPLATE)
    try:
        h2Omega = spectrum_obj.get_h2OmegaGW(np.asarray(f, dtype=float),
                                              float(Tr), float(alpha), float(beta_H))
    except Exception:
        return np.zeros_like(f, dtype=float)

    # Replace non-finite values with zeros
    h2Omega = np.nan_to_num(h2Omega, nan=0.0, posinf=0.0, neginf=0.0)
    return h2Omega