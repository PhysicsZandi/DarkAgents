"""
PTA spectrum computation for SU2_conformal model.
Uses the Spectrum class from backend/spectrum.py with the dbf template
for strongly supercooled phase transitions (valid for large alpha).
"""
import numpy as np
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from spectrum import Spectrum


def compute_spectrum(f, g_D, v, template="dbf", ksw=1, vw=1, cs=1/np.sqrt(3)):
    """
    Compute h^2 Omega_GW for SU2_conformal model.
    
    Parameters:
    -----------
    f : array-like
        Frequency values in Hz
    g_D : float or array-like
        SU(2)_D gauge coupling
    v : float or array-like
        VEV in GeV
    template : str
        Spectrum template: "higgsless", "dbf", or "bf"
    ksw : float
        Efficiency factor for sound waves
    vw : float
        Wall velocity
    cs : float
        Sound speed
    
    Returns:
    --------
    h2OmegaGW : array
        h^2 Omega_GW values at frequencies f
    """
    # Handle scalar inputs
    g_D = float(np.asarray(g_D).item() if np.asarray(g_D).size == 1 else np.asarray(g_D).flat[0])
    v = float(np.asarray(v).item() if np.asarray(v).size == 1 else np.asarray(v).flat[0])
    
    # Compute dependent parameters via Coleman-Weinberg
    beta_lambda = 3 * g_D**4 / (64 * np.pi**2)
    lambda_ = beta_lambda
    
    # Create spectrum instance
    spectrum = Spectrum(template=template)
    
    # We need T*, alpha, beta_H from FOPT
    # For now, we'll use the benchmark values from fopt_benchmarks.csv
    # But for the spectrum computation, we need to get these from the model
    # Since we don't have the full FOPT computation here, we'll use approximate values
    # In the actual implementation, these should come from the FOPT backend
    
    # For the SU2_conformal model, we use:
    # T* ≈ Treh (reheating temperature)
    # alpha ≈ alpha from FOPT
    # beta_H ≈ beta_H from FOPT
    
    # However, for the spectrum.py interface, we need:
    # - T: temperature (we'll use Treh as a proxy)
    # - alpha: strength parameter
    # - beta_H: rate parameter
    
    # Since this is a wrapper for PTArcade, we need to compute these from g_D and v
    # We'll use the semianalytic_pipeline to compute FOPT parameters
    
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
        from semianalytic_pipeline import SemiAnalyticPipeline
        
        # Map SU2_conformal model to backend
        chi0 = v
        boson_gbs = {"W": g_D / 2, "W3": 0.0}
        boson_dofs = {"W": 6, "W3": 2}
        fermion_gfs = {}
        fermion_dofs = {}
        
        model = SemiAnalyticPipeline(
            chi0=chi0,
            boson_gbs=boson_gbs,
            boson_dofs=boson_dofs,
            fermion_gfs=fermion_gfs,
            fermion_dofs=fermion_dofs,
            verbose=False,
        )
        
        alpha = model.get_alpha()
        beta_H = model.get_beta_H()
        Treh = model.get_Tr()
        
        # Check if values are valid
        if not np.isfinite(alpha) or not np.isfinite(beta_H) or not np.isfinite(Treh):
            return np.zeros_like(f)
        
        # Use Treh as T for spectrum computation
        T = Treh
        
    except Exception as e:
        # If FOPT computation fails, return zeros
        return np.zeros_like(f)
    
    # Compute spectrum
    try:
        h2OmegaGW = spectrum.h2OmegaGW(f, T, alpha, beta_H, ksw=ksw, vw=vw, cs=cs)
        # Handle non-finite values
        h2OmegaGW[~np.isfinite(h2OmegaGW)] = 0.0
        return h2OmegaGW
    except:
        return np.zeros_like(f)


def get_template_recommendation(g_D, v):
    """
    Recommend spectrum template based on FOPT parameters.
    For SU2_conformal, alpha can be very large (>> 0.5), so dbf/bf templates are preferred.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
        from semianalytic_pipeline import SemiAnalyticPipeline
        
        chi0 = v
        boson_gbs = {"W": g_D / 2, "W3": 0.0}
        boson_dofs = {"W": 6, "W3": 2}
        
        model = SemiAnalyticPipeline(
            chi0=chi0,
            boson_gbs=boson_gbs,
            boson_dofs=boson_dofs,
            fermion_gfs={},
            fermion_dofs={},
            verbose=False,
        )
        
        alpha = model.get_alpha()
        
        # Template selection based on alpha value
        if alpha <= 0.5:
            return "higgsless"
        else:
            # For large alpha, use dissipative bulk flow
            return "dbf"
    except:
        # Default to dbf for SU2_conformal
        return "dbf"


if __name__ == "__main__":
    # Test computation
    f_test = np.logspace(-9, -7, 100)
    g_D_test = 1.0
    v_test = 1.0
    
    h2OmegaGW = compute_spectrum(f_test, g_D_test, v_test, template="dbf")
    print(f"Test spectrum computed: {len(h2OmegaGW)} values")
    print(f"Max h2OmegaGW: {np.max(h2OmegaGW)}")
    print(f"Template recommendation: {get_template_recommendation(g_D_test, v_test)}")
