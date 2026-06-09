"""
SU2_conformal model implementation for first-order phase transition (FOPT) analysis.

This module implements the minimal non-abelian conformal model with SU(2)_D gauge group
and a complex scalar doublet Phi, following the classically scale-invariant approach
with Coleman-Weinberg mechanism.

Model details:
- Gauge group: SU(2)_D
- Scalar: Complex doublet Phi (4 real dof)
- Gauge bosons: W^1, W^2, W^3 (3 gauge fields, 6 dof in unbroken phase)
- After SSB: SU(2)_D -> U(1)_D with 2 massive W^+, W^- (6 dof) + 1 massless W^3 (2 dof)
- Tree-level potential: -lambda * (Phi^dagger Phi)^2 (classically conformal)
- lambda fixed by Coleman-Weinberg: beta_lambda = 3*g_D^4/(64*pi^2)

References:
- Backend: semianalytic_pipeline (arXiv:2602.02829)
- Model: 2109.11558 (Borah et al., 2021), 2210.07075 (Kierkla et al., 2023)
- Handoff: output/SU2_conformal/handoff_model.json
"""

import numpy as np
from backend.semianalytic_pipeline import SemiAnalyticPipeline


class SU2ConformalFOPT:
    """
    SU2_conformal model wrapper for FOPT computation.
    
    Independent parameters:
    - g_D: SU(2)_D gauge coupling (dimensionless)
    - v: Vacuum expectation value of background field chi (GeV)
    
    Dependent parameters (computed internally):
    - lambda: Quartic coupling (fixed by CW)
    - beta_lambda: CW beta function = 3*g_D^4/(64*pi^2)
    - m_rho: Radial scalar mass = sqrt(beta_lambda) * v
    
    Field-dependent masses:
    - W (2 massive gauge bosons): m_W = g_D * chi / 2, gb = g_D/2, dof = 6
    - W3 (massless gauge boson): m_W3 = 0, gb = 0, dof = 2
    - rho (radial scalar): m_rho = sqrt(3*lambda) * chi, gb = sqrt(3*lambda), dof = 1
    - G (pseudo-Goldstone): m_G = sqrt(lambda) * chi, gb = sqrt(lambda), dof = 1
    
    The backend (SemiAnalyticPipeline) automatically adds the scalar contribution,
    so we only need to provide gauge bosons.
    """
    
    def __init__(self, g_D, v, verbose=False):
        """
        Initialize SU2_conformal model with given parameters.
        
        Args:
            g_D (float): SU(2)_D gauge coupling
            v (float): Vacuum expectation value in GeV
            verbose (bool): Print debug information
        """
        self.g_D = float(g_D)
        self.v = float(v)
        self.verbose = verbose
        
        # Physical guards
        assert self.g_D > 0, f"g_D must be positive, got {self.g_D}"
        assert self.v > 0, f"v must be positive, got {self.v}"
        assert self.g_D < 4 * np.pi, f"g_D must be < 4*pi (~12.56) for perturbativity, got {self.g_D}"
        
        # Gauge boson contributions to backend
        # W: 2 massive gauge bosons (W^+, W^-) with gb = g_D/2, dof = 6
        # W3: 1 massless gauge boson with gb = 0, dof = 2
        boson_gbs = {
            "W": self.g_D / 2.0,
            "W3": 0.0,
        }
        boson_dofs = {
            "W": 6,  # 2 transverse + 1 longitudinal x 2 gauge bosons
            "W3": 2,  # 2 transverse only (massless)
        }
        
        # No fermions in this model
        fermion_gfs = {}
        fermion_dofs = {}
        
        # Initialize backend pipeline
        self.pipeline = SemiAnalyticPipeline(
            chi0=self.v,
            boson_gbs=boson_gbs,
            boson_dofs=boson_dofs,
            fermion_gfs=fermion_gfs,
            fermion_dofs=fermion_dofs,
            verbose=verbose,
        )
    
    def get_beta_lambda(self):
        """Compute Coleman-Weinberg beta function for lambda."""
        return self.pipeline.get_beta_lambda()
    
    def get_lambda(self):
        """Compute CW-fixed quartic coupling."""
        beta_lambda = self.get_beta_lambda()
        # From handoff: lambda = beta_lambda (for this model)
        # But the actual CW relation is that beta_lambda is the beta function,
        # and the fixed point gives lambda = beta_lambda * log(...)
        # However, the backend computes this internally
        # The handoff says: beta_lambda = 3 * g_D**4 / (64 * pi**2)
        return 3 * self.g_D**4 / (64 * np.pi**2)
    
    def get_scalar_mass(self):
        """Compute radial scalar (pseudo-dilaton) mass."""
        return self.pipeline.get_scalar_mass()
    
    def get_Tn(self):
        """Nucleation temperature (GeV)."""
        return self.pipeline.get_Tn()
    
    def get_Tp(self):
        """Percolation temperature (GeV)."""
        return self.pipeline.get_Tp()
    
    def get_Tr(self):
        """Reheating temperature (GeV)."""
        return self.pipeline.get_Tr()
    
    def get_alpha(self):
        """Transition strength parameter (dimensionless)."""
        return self.pipeline.get_alpha()
    
    def get_beta_H(self):
        """Inverse duration parameter (1/GeV)."""
        return self.pipeline.get_beta_H()
    
    def check_eternal_inflation(self):
        """Check if eternal inflation occurs."""
        return self.pipeline.get_check_eternal_inflation()
    
    def get_f_peak_est(self):
        """
        Estimate redshifted peak frequency in Hz (order-of-magnitude).
        
        Uses: f_peak ≈ 1.6e-5 Hz * (beta/H) * (T_reh/100 GeV) * (g_*/100)^(1/6)
        """
        Tp = self.get_Tp()
        Tr = self.get_Tr()
        beta_H = self.get_beta_H()
        
        if not all(np.isfinite([Tp, Tr, beta_H])):
            return np.nan
        
        if beta_H <= 0:
            return np.nan
        
        # Get g* at percolation temperature
        gstar_eff = self.pipeline.get_gstar_eff(Tp)
        
        # Use Tr for frequency estimation
        f_peak = 1.6e-5 * beta_H * (Tr / 100.0) * (gstar_eff / 100.0)**(1/6)
        return f_peak
    
    def get_all_parameters(self):
        """Return dictionary of all computed parameters."""
        Tn = self.get_Tn()
        Tp = self.get_Tp()
        Tr = self.get_Tr()
        alpha = self.get_alpha()
        beta_H = self.get_beta_H()
        eternal_inflation = self.check_eternal_inflation()
        beta_lambda = self.get_beta_lambda()
        scalar_mass = self.get_scalar_mass()
        f_peak_est = self.get_f_peak_est()
        
        return {
            "g_D": self.g_D,
            "v": self.v,
            "lambda": self.get_lambda(),
            "beta_lambda": beta_lambda,
            "m_rho": scalar_mass,
            "Tn": Tn,
            "Tp": Tp,
            "Tr": Tr,
            "alpha": alpha,
            "beta_H": beta_H,
            "f_peak_est": f_peak_est,
            "eternal_inflation": eternal_inflation,
        }


def compute_point(g_D, v, verbose=False):
    """
    Compute FOPT parameters for a single point in parameter space.
    
    Args:
        g_D (float): Gauge coupling
        v (float): Vacuum expectation value in GeV
        verbose (bool): Print debug info
        
    Returns:
        dict: Dictionary of computed parameters with status
    """
    try:
        model = SU2ConformalFOPT(g_D, v, verbose=verbose)
        params = model.get_all_parameters()
        
        # Check viability
        status = "viable"
        failure_reason = ""
        
        # Check for non-finite values
        for key in ["Tn", "Tp", "Tr", "alpha", "beta_H"]:
            if not np.isfinite(params[key]) or params[key] <= 0:
                status = "physical_failure"
                failure_reason = f"Non-finite or non-positive {key}: {params[key]}"
                break
        
        # Check eternal inflation
        if params["eternal_inflation"]:
            status = "physical_failure"
            failure_reason = "Eternal inflation detected"
        
        # Check if temperatures are below v (supercooling expected but not required)
        # We allow Tp < v
        
        params["status"] = status
        params["failure_reason"] = failure_reason
        
        return params
        
    except Exception as e:
        return {
            "g_D": g_D,
            "v": v,
            "status": "numerical_failure",
            "failure_reason": str(e),
        }


# Smoke test
if __name__ == "__main__":
    print("Running smoke test for SU2_conformal FOPT model...")
    
    # Test benchmark from literature hints: g_D ~ 1.0, v ~ 1000 GeV
    test_point = compute_point(g_D=1.0, v=1000.0, verbose=True)
    
    print("\nResults:")
    for key, val in test_point.items():
        if key not in ["status", "failure_reason"]:
            print(f"  {key}: {val:.4g}")
    print(f"  status: {test_point['status']}")
    if test_point["status"] != "viable":
        print(f"  failure_reason: {test_point['failure_reason']}")
    
    print("\nSmoke test complete.")
