# Validated Model: Dark U(1) Conformal

## Model Specification

### Gauge Group and Symmetries

- **Gauge group**: Dark U(1)_D, anomaly-free (no chiral fermions charged under it)
- **Global symmetry**: Classical scale invariance at tree level (no dimensionful parameters)
- **SSB pattern**: U(1)_D -> nothing (complete breaking)

### Particle Content

| Particle | Type | Spin | U(1)_D charge | dof (before SSB) | dof (after SSB) | Mass |
|----------|------|------|---------------|------------------|-----------------|------|
| Phi | Complex scalar | 0 | +1 | 2 | 2 (decomposes into rho + G) | Tree-level 0 |
| rho | Real scalar (radial) | 0 | 0 | - | 1 (physical Higgs) | radiatively generated |
| A' | Gauge boson | 1 | 0 (adjoint) | 2 (transverse) | 3 (massive) | m_A' = g_D v |
| G | Goldstone mode | 0 | 0 | - | 0 (eaten by A') | 0 |

### Lagrangian

```
L_D = |D_mu Phi|^2 - lambda_Phi |Phi|^4 - 1/4 F'_mu_nu F'^mu_nu
D_mu = partial_mu - i g_D A'_mu
F'_mu_nu = partial_mu A'_nu - partial_nu A'_mu
```

Optional portals (assumed small for FOPT analysis):
- Higgs portal: lambda_{HPhi} |H|^2 |Phi|^2
- Gauge kinetic mixing: (epsilon/2) F'_mu_nu F^mu_nu

### VEV Convention

```
Phi(x) = (chi + rho(x) + i G(x)) / sqrt(2)
```

where chi is the classical background field (RGI direction), rho is the radial mode, and G is the Goldstone mode. The vev is v = <chi> at the minimum of the effective potential.

### Tree-Level Potential

```
V_tree(chi) = lambda_Phi * chi^4 / 4
```

### Field-Dependent Masses

- **A' (dark photon)**: m_A'^2(chi) = g_D^2 * chi^2, dof = 3 (massive gauge boson)
- **rho (radial mode)**: m_rho^2(chi) = 3 * g_D^4 * chi^2 / (8 * pi^2), dof = 1 (real scalar)
- **G (Goldstone)**: m_G^2 = 0 (eaten by A' in unitary gauge)

### CW Relations

```
beta_lambda = 3 * g_D^4 / (8 * pi^2)
delta_V = beta_lambda * v^4 / 16
m_rho^2(v) = beta_lambda * v^2
```

The quartic lambda_Phi is fixed by the CW minimization condition dV_eff/d chi|_{chi=v} = 0 and is a dependent parameter.

### Parameter Basis

**Independent** (free parameters to scan):
- v: vev [GeV], range 1e-2 to 1e3
- g_D: gauge coupling [dimensionless], range 0.1 to 4*pi

**Dependent** (determined by model relations):
- lambda_Phi: tree-level quartic (CW-fixed)
- m_rho: radial mode mass, m_rho^2 = 3 * g_D^4 * v^2 / (8 * pi^2)
- m_A': dark photon mass, m_A' = g_D * v
- beta_lambda: 3 * g_D^4 / (8 * pi^2)

**Fixed** (assumed values):
- xi = T_dark/T_visible = 1 (thermalised sectors)
- epsilon: kinetic mixing (value unspecified, assumed small)
- lambda_HPhi: Higgs portal (value unspecified, assumed small)

### Thermalisation

- Dark and visible sectors assumed thermalised at same temperature (xi = 1)
- Dark sector dofs contribute to g_*: 3 (massive A') + 1 (rho) = 4 bosonic dofs
- No fermionic dark dofs

### Backend Compatibility

The model is fully compatible with `backend/semianalytic_pipeline.py`. Input mapping:
```python
SemiAnalyticPipeline(
    chi0 = v,                    # scalar vev
    boson_gbs = {"Aprime": g_D}, # g_b = m_b/v = g_D,
    boson_dofs = {"Aprime": 3},  # 3 dofs for massive gauge boson
    fermion_gfs = {},            # no fermions
    fermion_dofs = {},           # no fermions
)
```

### Key Assumptions

1. Portal couplings are small enough to not affect the effective potential or FOPT dynamics
2. Dark and visible sectors are in thermal equilibrium (xi = 1)
3. No fermionic dark matter in the minimal version
4. One-loop CW approximation with daisy resummation (Arnold-Espinosa scheme)
5. Runaway bubble walls (v_w -> 1) typical of supercooled transitions

### SymPy-Compatible Expression Strings

- `mAprime_sq(chi)` = `gD**2 * chi**2`
- `mrho_sq(chi)` = `3 * gD**4 * chi**2 / (8 * pi**2)`
- `beta_lambda` = `3 * gD**4 / (8 * pi**2)`
- `delta_V` = `3 * gD**4 * v**4 / (128 * pi**2)`

### Literature Context

This model has been extensively studied in the literature (see preliminary librarian report). The most directly relevant references are:
- Goncalves et al. (2025, arXiv:2501.11619) -- conformal dark U(1)' with PTArcade fit to NANOGrav
- Christiansen et al. (2025, arXiv:2511.02910) -- methodology for conformal Abelian Higgs model
- Balan et al. (2025, arXiv:2502.19478) -- similar model with fermionic DM and GAMBIT fit