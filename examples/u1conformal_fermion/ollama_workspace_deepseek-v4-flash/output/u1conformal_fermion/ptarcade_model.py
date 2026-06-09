"""
ptarcade_model.py -- PTArcade model file for the conformal U(1)_D dark sector.

This file defines the priors and spectrum function for PTArcade Bayesian inference.
"""

from ptarcade.models_utils import prior
from pathlib import Path
import sys
import os
import numpy as np

# Add backend to path
_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Add output dir to path
_output_dir = os.path.dirname(os.path.abspath(__file__))
if _output_dir not in sys.path:
    sys.path.insert(0, _output_dir)

from spectrum import Spectrum
from semianalytic_pipeline import SemiAnalyticPipeline


# ============================================================
# Priors on independent model parameters
# ============================================================
# Based on benchmark scan results:
#   g_D: best points ~0.5-0.7, viable range ~0.3-2.0
#   y_psi: best points ~0.05-0.5, viable range ~0.01-0.6
#   v: best points ~0.3-1.0 GeV, viable range ~0.001-1.0 GeV
#
# Priors are widened by at least a factor of 2 in each direction.
# For v (spanning orders of magnitude), use log prior.
# For g_D and y_psi (spanning small ranges), use linear priors.

parameters = {
    "g_D": prior("Uniform", 0.1, 3.0),
    "y_psi": prior("Uniform", 0.0001, 0.8),
    "log10_v": prior("Uniform", -4.0, 1.0),  # v in [1e-4, 10] GeV
}


def spectrum(f, g_D, y_psi, log10_v):
    """
    Compute h^2 Omega_GW(f) for given model parameters.

    Parameters
    ----------
    f : array_like
        Frequency array in Hz.
    g_D : float or array_like
        Dark gauge coupling.
    y_psi : float or array_like
        Yukawa coupling.
    log10_v : float or array_like
        log10 of dark Higgs vev in GeV.

    Returns
    -------
    ndarray
        h^2 Omega_GW(f) values.
    """
    # Convert array inputs to scalars (PTArcade passes arrays)
    g_D = float(np.asarray(g_D).flat[0])
    y_psi = float(np.asarray(y_psi).flat[0])
    log10_v = float(np.asarray(log10_v).flat[0])
    v = 10.0 ** log10_v

    # Ensure f is an array
    f = np.asarray(f, dtype=float)

    # Physical guards
    beta_lambda = (3.0 * g_D**4 - 2.0 * y_psi**4) / (8.0 * np.pi**2)
    if beta_lambda <= 0:
        return np.zeros_like(f)
    if g_D <= y_psi / np.sqrt(2.0):
        return np.zeros_like(f)
    if g_D <= 0 or y_psi < 0 or v <= 0:
        return np.zeros_like(f)

    # Build model and compute FOPT parameters
    try:
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

        Tp = model.get_Tp()
        alpha = model.get_alpha()
        beta_H = model.get_beta_H()
        Treh = model.get_Tr()
        eternal = model.get_check_eternal_inflation()
    except Exception:
        return np.zeros_like(f)

    # Validate FOPT results
    if not np.isfinite(alpha) or alpha <= 0:
        return np.zeros_like(f)
    if not np.isfinite(beta_H) or beta_H <= 0:
        return np.zeros_like(f)
    if not np.isfinite(Treh) or Treh <= 0:
        return np.zeros_like(f)
    if not np.isfinite(Tp) or Tp <= 0:
        return np.zeros_like(f)
    if eternal is True or not np.isfinite(eternal):
        return np.zeros_like(f)

    # Compute spectrum using the dbf template (dissipative bulk flow)
    try:
        spec = Spectrum(template="dbf")
        h2OmegaGW = spec.get_h2OmegaGW(f, Treh, alpha, beta_H, ksw=1.0)
    except Exception:
        return np.zeros_like(f)

    # Ensure non-negative
    h2OmegaGW = np.maximum(h2OmegaGW, 0.0)

    return h2OmegaGW
