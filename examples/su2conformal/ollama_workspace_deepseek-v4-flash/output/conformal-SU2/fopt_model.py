"""
fopt_model.py -- conformal-SU2 model implementation using semianalytic_pipeline backend.

Computes first-order phase transition parameters for the classically scale-invariant
SU(2)_X model with one complex scalar doublet.

Independent parameters: g (gauge coupling), chi0 (VEV in GeV).
All other parameters are CW-fixed dependent parameters.

Backend: semianalytic_pipeline (conformal/CW single-field models only).
"""

import sys
import os
import traceback

import numpy as np

# Add the backend directory to the path
backend_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "backend")
sys.path.insert(0, os.path.abspath(backend_dir))

from semianalytic_pipeline import SemiAnalyticPipeline


def compute_fopt(g, chi0, verbose=False):
    """
    Compute FOPT parameters for the conformal-SU2 model.

    Parameters
    ----------
    g : float
        SU(2)_X gauge coupling (dimensionless).
    chi0 : float
        Scalar VEV at zero temperature (GeV).
    verbose : bool
        Whether to print debug output.

    Returns
    -------
    dict
        Dictionary with keys:
        - 'g': input gauge coupling
        - 'chi0': input VEV (GeV)
        - 'alpha': phase transition strength (dimensionless)
        - 'beta_H': characteristic timescale (dimensionless)
        - 'Tn': nucleation temperature (GeV)
        - 'Tp': percolation temperature (GeV)
        - 'Treh': reheating temperature (GeV)
        - 'f_peak_est': estimated redshifted peak frequency (Hz)
        - 'beta_lambda': CW beta_lambda coefficient (dependent)
        - 'm_chi': scalar mass (GeV) (dependent)
        - 'delta_V': vacuum energy difference (GeV^4) (dependent)
        - 'gstar_eff': effective degrees of freedom at Tp
        - 'eternal_inflation': whether eternal inflation occurs
        - 'status': 'viable', 'physical_failure', 'numerical_failure', 'not_fopt'
        - 'failure_reason': explanation if not viable
    """
    result = {
        'g': g,
        'chi0': chi0,
        'alpha': None,
        'beta_H': None,
        'Tn': None,
        'Tp': None,
        'Treh': None,
        'f_peak_est': None,
        'beta_lambda': None,
        'm_chi': None,
        'delta_V': None,
        'gstar_eff': None,
        'eternal_inflation': None,
        'status': 'numerical_failure',
        'failure_reason': '',
    }

    # Physical guards before calling backend
    if g <= 0:
        result['status'] = 'physical_failure'
        result['failure_reason'] = 'g <= 0'
        return result
    if chi0 <= 0:
        result['status'] = 'physical_failure'
        result['failure_reason'] = 'chi0 <= 0'
        return result
    if not np.isfinite(g) or not np.isfinite(chi0):
        result['status'] = 'physical_failure'
        result['failure_reason'] = 'non-finite input'
        return result
    # Perturbativity guard
    if g >= 4 * np.pi:
        result['status'] = 'physical_failure'
        result['failure_reason'] = 'g >= 4*pi (non-perturbative)'
        return result

    # Dependent parameters (for diagnostics only -- the backend computes internally)
    beta_lambda = 9 * g**4 / (128 * np.pi**2)
    if beta_lambda <= 0:
        result['status'] = 'physical_failure'
        result['failure_reason'] = 'beta_lambda <= 0 (no CW minimum)'
        return result

    # Build backend inputs
    boson_gbs = {"W": g / 2.0}
    boson_dofs = {"W": 9}
    fermion_gfs = {}
    fermion_dofs = {}

    try:
        model = SemiAnalyticPipeline(
            chi0=chi0,
            boson_gbs=boson_gbs,
            boson_dofs=boson_dofs,
            fermion_gfs=fermion_gfs,
            fermion_dofs=fermion_dofs,
            verbose=verbose,
        )

        # Compute beta_lambda from backend for consistency
        beta_lambda_backend = model.get_beta_lambda()
        if not np.isfinite(beta_lambda_backend) or beta_lambda_backend <= 0:
            result['status'] = 'physical_failure'
            result['failure_reason'] = 'backend beta_lambda <= 0'
            return result

        # Compute FOPT parameters
        Tn = model.get_Tn()
        Tp = model.get_Tp()
        Treh = model.get_Tr()
        alpha = model.get_alpha()
        beta_H = model.get_beta_H()
        m_chi = model.get_scalar_mass()
        delta_V = model.get_delta_V()
        gstar_eff = model.get_gstar_eff(Tp)
        eternal_inflation = model.get_check_eternal_inflation()

        # Check finite values
        if not all(np.isfinite(x) for x in [Tn, Tp, Treh, alpha, beta_H, m_chi, delta_V, gstar_eff]):
            result['status'] = 'numerical_failure'
            result['failure_reason'] = 'non-finite backend output'
            # Still record whatever we have
            result['Tn'] = Tn
            result['Tp'] = Tp
            result['Treh'] = Treh
            result['alpha'] = alpha
            result['beta_H'] = beta_H
            result['beta_lambda'] = beta_lambda_backend
            result['m_chi'] = m_chi
            result['delta_V'] = delta_V
            result['gstar_eff'] = gstar_eff
            result['eternal_inflation'] = eternal_inflation
            return result

        # Physical positivity guards
        if Tn <= 0:
            result['status'] = 'physical_failure'
            result['failure_reason'] = 'Tn <= 0'
            result['Tn'] = Tn
            return result
        if Tp <= 0:
            result['status'] = 'physical_failure'
            result['failure_reason'] = 'Tp <= 0'
            result['Tp'] = Tp
            return result
        if Treh <= 0:
            result['status'] = 'physical_failure'
            result['failure_reason'] = 'Treh <= 0'
            result['Treh'] = Treh
            return result
        if alpha <= 0 or not np.isfinite(alpha):
            result['status'] = 'physical_failure'
            result['failure_reason'] = 'alpha <= 0 or non-finite'
            result['alpha'] = alpha
            return result
        if beta_H <= 0 or not np.isfinite(beta_H):
            result['status'] = 'physical_failure'
            result['failure_reason'] = 'beta_H <= 0 or non-finite'
            result['beta_H'] = beta_H
            return result

        # Check for eternal inflation
        if eternal_inflation:
            result['status'] = 'physical_failure'
            result['failure_reason'] = 'eternal inflation (false vacuum decay too slow)'
            # Record values anyway for diagnostics
            result['Tn'] = Tn
            result['Tp'] = Tp
            result['Treh'] = Treh
            result['alpha'] = alpha
            result['beta_H'] = beta_H
            result['beta_lambda'] = beta_lambda_backend
            result['m_chi'] = m_chi
            result['delta_V'] = delta_V
            result['gstar_eff'] = gstar_eff
            result['eternal_inflation'] = eternal_inflation
            return result

        # Compute estimated peak frequency
        # f_peak_est ~ 1.6e-5 Hz * (beta/H) * (Treh/100 GeV) * (g_*/100)^(1/6)
        f_peak_est = 1.6e-5 * beta_H * (Treh / 100.0) * (gstar_eff / 100.0) ** (1.0 / 6.0)

        # Fill result
        result['Tn'] = float(Tn)
        result['Tp'] = float(Tp)
        result['Treh'] = float(Treh)
        result['alpha'] = float(alpha)
        result['beta_H'] = float(beta_H)
        result['f_peak_est'] = float(f_peak_est)
        result['beta_lambda'] = float(beta_lambda_backend)
        result['m_chi'] = float(m_chi)
        result['delta_V'] = float(delta_V)
        result['gstar_eff'] = float(gstar_eff)
        result['eternal_inflation'] = bool(eternal_inflation)
        result['status'] = 'viable'
        result['failure_reason'] = ''

    except Exception as e:
        result['status'] = 'numerical_failure'
        result['failure_reason'] = f'backend exception: {str(e)}'
        if verbose:
            traceback.print_exc()

    return result


def smoke_test():
    """Run a quick smoke test on the literature benchmark points."""
    print("=" * 60)
    print("conformal-SU2 FOPT Smoke Test")
    print("=" * 60)

    # BP from arXiv:2109.11558: g=1.37, chi0=2*M_Z/g ~ 2*8.23e-3/1.37 GeV ~ 0.012 GeV
    # M_Z = g*chi0/2 => chi0 = 2*M_Z/g
    benchmark_points = [
        {
            "name": "arXiv:2109.11558 BP1",
            "g": 1.37,
            "chi0": 2 * 8.23e-3 / 1.37,  # ~0.012 GeV
        },
        {
            "name": "arXiv:2109.11558 BP2",
            "g": 1.37,
            "chi0": 2 * 817e-6 / 1.37,  # ~0.0012 GeV
        },
        {
            "name": "arXiv:2602.09092 best-fit (U(1)' adapted, same g)",
            "g": 0.692,
            "chi0": 0.14,  # v = 0.14 GeV directly
        },
    ]

    for bp in benchmark_points:
        print(f"\n--- {bp['name']} ---")
        print(f"  g = {bp['g']}, chi0 = {bp['chi0']:.6e} GeV")
        result = compute_fopt(bp['g'], bp['chi0'], verbose=False)
        print(f"  status: {result['status']}")
        if result.get('failure_reason'):
            print(f"  failure_reason: {result['failure_reason']}")
        for key in ['alpha', 'beta_H', 'Tn', 'Tp', 'Treh', 'f_peak_est', 'beta_lambda', 'm_chi']:
            val = result.get(key)
            if val is not None and np.isfinite(val):
                print(f"  {key}: {val:.6e}")
            elif val is not None:
                print(f"  {key}: {val} (non-finite)")
            else:
                print(f"  {key}: None")
        print(f"  eternal_inflation: {result.get('eternal_inflation')}")

    print("\n" + "=" * 60)
    print("Smoke test complete.")
    print("=" * 60)


if __name__ == "__main__":
    smoke_test()