"""
PTArcade model file for SU2_conformal FOPT GW spectrum.

This file defines the spectrum function that PTArcade will use for inference.
Uses the Spectrum class from backend/spectrum.py with the dbf template
for strongly supercooled phase transitions.
"""
from ptarcade.models_utils import prior
from pathlib import Path
import sys
import numpy as np

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from spectrum import Spectrum
from semianalytic_pipeline import SemiAnalyticPipeline


# Define priors on independent model parameters
# Based on FOPT scan that found viable points in these ranges
parameters = {
    "log10_g_D": prior("Uniform", np.log10(0.5), np.log10(3.0)),
    "log10_v_GeV": prior("Uniform", np.log10(0.01), np.log10(10.0)),
}


def spectrum(f, log10_g_D, log10_v_GeV):
    """
    Compute h^2 Omega_GW spectrum for SU2_conformal model.
    
    Parameters:
    -----------
    f : array
        Frequency values in Hz
    log10_g_D : float or array
        log10 of SU(2)_D gauge coupling
    log10_v_GeV : float or array
        log10 of VEV in GeV
        
    Returns:
    --------
    h2omegagw : array
        h^2 Omega_GW values at frequencies f
    """
    # Handle array inputs (PTArcade passes parameters as arrays)
    # Extract scalar values
    log10_g_D = float(
        np.asarray(log10_g_D).item()
        if np.asarray(log10_g_D).size == 1
        else np.asarray(log10_g_D).flat[0]
    )
    log10_v_GeV = float(
        np.asarray(log10_v_GeV).item()
        if np.asarray(log10_v_GeV).size == 1
        else np.asarray(log10_v_GeV).flat[0]
    )
    
    # Convert back to linear scale
    g_D = 10.0 ** log10_g_D
    v_GeV = 10.0 ** log10_v_GeV
    
    # Validate inputs
    if not np.isfinite(g_D) or not np.isfinite(v_GeV):
        return np.zeros_like(f)
    if g_D <= 0 or v_GeV <= 0:
        return np.zeros_like(f)
    
    # Map SU2_conformal model to backend
    chi0 = v_GeV
    boson_gbs = {"W": g_D / 2, "W3": 0.0}
    boson_dofs = {"W": 6, "W3": 2}
    fermion_gfs = {}
    fermion_dofs = {}
    
    try:
        # Compute FOPT parameters
        model = SemiAnalyticPipeline(
            chi0=chi0,
            boson_gbs=boson_gbs,
            boson_dofs=boson_dofs,
            fermion_gfs=fermion_gfs,
            fermion_dofs=fermion_dofs,
            verbose=False,
        )
        
        # Check for eternal inflation first (before computing FOPT params)
        # get_check_eternal_inflation() returns True when eternal inflation occurs
        eternal_inflation_check = model.get_check_eternal_inflation()
        # Return zeros if eternal inflation occurs (True), Tp==0 (0), or NaN
        # bool is subclass of int in Python, so check True first, then check type for 0
        if eternal_inflation_check is True:
            return np.zeros_like(f)
        if type(eternal_inflation_check) is int and eternal_inflation_check == 0:
            return np.zeros_like(f)
        if not np.isfinite(eternal_inflation_check):
            return np.zeros_like(f)
        # eternal_inflation_check is False (bool) -> continue
        
        alpha = model.get_alpha()
        beta_H = model.get_beta_H()
        Treh = model.get_Tr()
        
        # Validate FOPT outputs
        if not np.isfinite(alpha) or not np.isfinite(beta_H) or not np.isfinite(Treh):
            return np.zeros_like(f)
        if alpha <= 0 or beta_H <= 0 or Treh <= 0:
            return np.zeros_like(f)
        
        # Use dbf template for large alpha (SU2_conformal typically has alpha >> 0.5)
        # Switch to higgsless if alpha is small
        template = "dbf" if alpha > 0.5 else "higgsless"
        
        spectrum = Spectrum(template=template)
        
        # Compute spectrum
        h2omegagw = spectrum.h2OmegaGW(f, Treh, alpha, beta_H)
        
        # Handle non-finite values
        h2omegagw = np.where(np.isfinite(h2omegagw), h2omegagw, 0.0)
        
        return h2omegagw
        
    except Exception as e:
        # If any error occurs, return zeros
        return np.zeros_like(f)
