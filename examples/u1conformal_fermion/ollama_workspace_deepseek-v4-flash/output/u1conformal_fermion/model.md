# Validated Model: U(1)_D Conformal Dark Sector

## Model Specification (Validated by Critic Agent)

This document describes the classically scale-invariant U(1)_D dark sector model after critique and minimal fixes. The model is consistent, anomaly-free, and compatible with the `semianalytic_pipeline.py` backend.

## Gauge Groups and Symmetries

| Symmetry | Type | Notes |
|----------|------|-------|
| U(1)_D | Gauge (rank 1) | Dark U(1) with coupling g_D |
| Classical scale invariance | Global (anomalous) | No dimensionful parameters at tree level; broken radiatively |

## Particle Content

| Field | Type | Spin | U(1)_D Charge | DOF | Statistics |
|-------|------|------|----------------|-----|------------|
| Phi | Complex scalar | 0 | +1 | 2 | Bose |
| A'_mu | Gauge boson | 1 | 0 | 3 (massive) | Bose |
| psi_1 | Dirac fermion | 1/2 | +1/2 | 4 | Fermi |
| psi_2 | Dirac fermion | 1/2 | -1/2 | 4 | Fermi |

**Total DOF before SSB**: 2 + 2 + 4 + 4 = 12
**Total DOF after SSB**: 3 + 1 + 4 + 4 = 12 (Goldstone eated by A'_mu)

## Lagrangian

### Kinetic terms
```
L_gauge = -1/4 F'_mu_nu F'^mu_nu
L_scalar = (D_mu Phi)* (D^mu Phi),    D_mu = d_mu + i g_D A'_mu
L_psi1 = i psi1_bar gamma^mu D_mu psi1,    D_mu = d_mu + i g_D/2 A'_mu
L_psi2 = i psi2_bar gamma^mu D_mu psi2,    D_mu = d_mu - i g_D/2 A'_mu
```

### Yukawa term
```
L_yukawa = y_psi * Phi * psi1_bar * psi2 + h.c.
```
Gauge invariance verified: Phi charge +1 + psi1_bar charge -1/2 + psi2 charge -1/2 = 0.

### Scalar potential
```
V_tree = lambda_Phi * (Phi* Phi)^2
```

## Anomaly Cancellation

| Anomaly | Computation | Result |
|---------|-------------|--------|
| U(1)_D^3 | (+1/2)^3+(+1/2)^3 + (-1/2)^3+(-1/2)^3 = 1/4 - 1/4 | 0 (PASS) |
| U(1)_D-gravity | (+1/2)+(+1/2) + (-1/2)+(-1/2) = 1 - 1 | 0 (PASS) |
| U(1)_D-U(1)_Y mixed | No SM-charged dark fermions | 0 (PASS) |

The two Dirac fermions with opposite charges are the minimal anomaly-free fermion content for this gauge group and scalar charge.

## Symmetry Breaking Pattern

- U(1)_D -> nothing (fully broken)
- VEV convention: `Phi = (chi + v)/sqrt(2)` in unitary gauge
- Goldstone theta eaten by A'_mu (longitudinal mode)

## Free Parameters (Independent, Scanned)

| Parameter | Range | Description |
|-----------|-------|-------------|
| g_D | [0.1, 4.0] | Dark gauge coupling (perturbative: g_D < 4*pi) |
| y_psi | [0.0, 1.0] | Yukawa coupling; constrained by beta_lambda > 0 and g_D > y_psi/sqrt(2) |
| v | [100, 10000] GeV | Dark Higgs vev (sets mass scale) |

## Derived Parameters (Dependent, Not Scanned)

| Parameter | Expression | Description |
|-----------|------------|-------------|
| lambda_Phi | (3*g_D^4 - 2*y_psi^4) / (32*pi^2) | CW-fixed quartic (lambda_Phi = beta_lambda/4) |
| beta_lambda | (3*g_D^4 - 2*y_psi^4) / (8*pi^2) | CW beta function (beta_lambda > 0 required) |
| m_chi | chi^2 * sqrt(beta_lambda) * v | Scalar mass from CW curvature |
| m_Aprime | g_D * v | Dark photon mass |
| m_psi | y_psi * v / sqrt(2) | Dirac fermion mass (each of psi_1, psi_2) |

## Field-Dependent Masses

| Particle | m^2(chi) | DOF |
|----------|----------|-----|
| A'_mu | g_D^2 * chi^2 | 3 |
| chi | beta_lambda * chi^2 | 1 |
| psi | y_psi^2 * chi^2 / 2 | 8 |

## Thermal Masses (combined g2sq formula)

All thermal masses use the combined formula matching the backend:
```
Pi = (3*g_D^2 + 2*y_psi^2) * T^2 / 12
```
This applies to: A'_mu (longitudinal), chi (radial scalar), and Goldstone theta.

## Backend Mapping (semianalytic_pipeline.py)

```
chi0 = v
boson_gbs = {"gauge": g_D, "scalar": 0}
boson_dofs = {"gauge": 3, "scalar": 1}
fermion_gfs = {"psi": y_psi / sqrt(2)}
fermion_dofs = {"psi": 8}
```

The backend automatically computes:
- g2sq = 3*g_D^2 + 2*y_psi^2 for thermal mass
- beta_lambda = (3*g_D^4 - 2*y_psi^4)/(8*pi^2) for CW potential
- m_chi^2 = beta_lambda * v^2 for scalar mass

## Key Physical Constraints

1. **CW condition**: beta_lambda > 0 => y_psi < (3/2)^(1/4) * g_D approx 1.11*g_D
2. **Supercooling condition**: g_D > y_psi/sqrt(2) (m_A' > m_psi, Feng-Zhang)
3. **Perturbativity**: g_D < 4*pi, y_psi < 4*pi
4. **CW quartic**: lambda_Phi is derived, not scanned

## Files

- `/Users/mattezandi/Desktop/code/DarkAgents/ollama_workspace/output/u1conformal_fermion/handoff_model.json` -- Machine-readable validated model
- `/Users/mattezandi/Desktop/code/DarkAgents/ollama_workspace/output/u1conformal_fermion/handoff_critique.json` -- Machine-readable validation results
- `/Users/mattezandi/Desktop/code/DarkAgents/ollama_workspace/output/u1conformal_fermion/critique.md` -- Human-readable critique
