# Model Specification: conformal-SU2

## Overview

A classically scale-invariant SU(2)_X gauge theory with one complex scalar doublet and no fermions. The tree-level scalar potential contains only a quartic term (no mass term). Symmetry breaking is radiatively induced via the Coleman-Weinberg mechanism: one-loop gauge boson contributions generate a nontrivial minimum. This model is designed to produce nHz stochastic gravitational waves from a first-order phase transition in the early universe.

**Model is compatible** with the `backend/semianalytic_pipeline.py` backend.

---

## Gauge Groups and Symmetries

| Group | Coupling | Status |
|-------|----------|--------|
| SU(2)_X | g | Fully broken (SU(2) -> nothing) |

No global symmetries, no U(1) factors, no SM coupling.

---

## Particle Content

| Field | Spin | SU(2)_X Rep | dof (before SSB) | dof (after SSB) | Statistics |
|-------|:----:|:-----------:|:-----------------:|:----------------:|:----------:|
| Phi | 0 | Fundamental (doublet) | 4 (complex) | 1 radial + 3 Goldstones | Boson |
| W^a_mu | 1 | Adjoint (triplet) | 6 (massless) | 9 (massive) | Boson |

**DoF conservation**: 10 dof before SSB (4 + 6), 10 dof after SSB (1 + 9).

---

## Lagrangian

### Gauge kinetic term
```
-1/4 * W^a_{munu} * W^{a,munu}
```
Standard SU(2) Yang-Mills with field strength:
W^a_{munu} = partial_mu W^a_nu - partial_nu W^a_mu + g * epsilon^{abc} W^b_mu W^c_nu

### Scalar kinetic term
```
(D_mu Phi)^\dagger * (D^mu Phi)
```
Covariant derivative: D_mu = partial_mu + i * g * W^a_mu * tau^a, with tau^a = sigma^a/2.

### Scalar potential (tree level)
```
lambda * (Phi^\dagger * Phi)^2
```
Classically scale-invariant quartic term. No quadratic mass term. The quartic coupling lambda is radiatively generated and fixed by the CW mechanism; it is never a free scan parameter.

---

## Parameters

### Independent (scan parameters)

| Parameter | Description | Range | Unit |
|-----------|-------------|-------|------|
| g | SU(2)_X gauge coupling | [0.1, 3.0] | dimensionless |
| chi0 | Scalar VEV at T=0 | [0.1, 10000.0] | GeV |

### Dependent (computed from independent parameters)

| Parameter | Expression | Description |
|-----------|-----------|-------------|
| beta_lambda | 9 * g**4 / (128 * pi**2) | CW quartic coefficient (9 dof, gb = g/2) |
| m_chi2 | beta_lambda * chi0**2 | Radial scalar mass squared |
| gb_scalar | sqrt(beta_lambda) | Scalar mass-over-vev ratio (auto-computed by backend) |
| delta_V | beta_lambda * chi0**4 / 16 | Vacuum energy difference (T=0) |

### CW derivation

The beta_lambda coefficient is computed from the general CW relation:
```
beta_lambda = (1/(8*pi^2)) * (sum_B n_B * gb^4 - sum_F n_F * gf^4)
```

For this model:
- 3 massive gauge bosons x 3 polarizations = 9 real dof
- Each polarization: gb = g/2
- No fermions

```
beta_lambda = 9 * (g/2)^4 / (8*pi^2) = 9 * g^4 / (128 * pi^2) > 0
```

The condition beta_lambda > 0 is satisfied (bosons dominate), enabling radiative symmetry breaking.

---

## Symmetry Breaking Pattern

SU(2)_X is completely broken to nothing by the VEV of the scalar doublet:

- **VEV direction**: Phi_0 = (0, chi0/sqrt(2))^T (neutral component)
- **Order parameter**: chi (background field of the radial scalar mode)
- **Unbroken generators**: none (all three generators broken)

Field expansion around the background:
```
Phi = (G1 + i*G2, (chi + h + i*G3)) / sqrt(2)
```
where G_{1,2,3} are Goldstones (absorbed as longitudinal modes), h is the physical radial mode, and chi is the classical background field.

---

## Field-Dependent Masses

### Gauge bosons
```
m_W^2(chi) = g**2 * chi**2 / 4      (3 vectors, 9 dof)
gb_W = g / 2
```
Derived by substituting Phi = (0, chi/sqrt(2))^T into (D_mu Phi)^\dagger (D^mu Phi).

### Radial scalar
```
m_chi^2(chi) = beta_lambda * chi**2      (1 dof)
gb_scalar = sqrt(beta_lambda)            (auto-computed by backend)
```

---

## Thermal Masses (Debye / Daisy resummation)

| Particle | dof | m_D^2 | Notes |
|----------|:---:|-------|-------|
| W^a longitudinal | 3 | g**2 * T**2 | SU(2) Debye: m_D^2 = g^2 T^2 (N/3 + N_s/12) with N=2, N_s=4 real scalars |
| chi (radial scalar) | 1 | 3/16 * g**2 * T**2 | C_f * g^2 * T^2 / 4 with C_f = 3/4 |
| Goldstones | 3 | 3/16 * g**2 * T**2 | Same as scalar from gauge interactions |

---

## Backend Compatibility

**Backend**: `semianalytic_pipeline.py`

**Status**: Compatible

**Mapping**:
```python
SemiAnalyticPipeline(
    chi0=chi0,
    boson_gbs={"W": g/2},
    boson_dofs={"W": 9},
    fermion_gfs={},
    fermion_dofs={},
)
```

The backend auto-computes:
- `get_beta_lambda()`: 9 * (g/2)^4 / (8*pi^2) = 9*g^4/(128*pi^2)
- `get_scalar_mass()`: sqrt(beta_lambda) * chi0
- `get_delta_V()`: beta_lambda * chi0^4 / 16

---

## Parameter Space and Constraints

Parameter ranges are chosen to produce nHz GW signals:
- **g** in [0.1, 3.0]: perturbative, consistent with literature benchmarks (g ~ 0.6-1.4)
- **chi0** in [0.1, 10000] GeV: MeV-scale VEVs produce MeV-scale transition temperatures, mapping to nHz peak frequencies

### Known constraints (to be evaluated downstream)
- **Delta N_eff**: Stable dark SU(2) sector contributes to N_eff and is constrained by BBN/CMB (arXiv:2306.09411). The model has no decay portal to the SM.
- **Percolation**: Strong supercooling must satisfy the percolation condition (checked by the backend).
- **BBN timing**: Phase transition must complete before BBN (T > ~1 MeV).
- **Perturbativity**: g < 4*pi (satisfied by the scan range).

---

## Literature Context

The exact same model (SU(2)_D with one complex scalar doublet, CW mechanism, nHz GW target) has been studied in:
- **arXiv:2109.11558** (Borah, Dasgupta, Kang, 2021): original study with NANOGrav 12.5 yr benchmarks

Structurally similar models with related physics:
- **arXiv:2602.09092**: Conformal U(1)' model (CW, PTA fit) -- structurally similar but U(1)' gauge group
- **arXiv:2210.07075**: SU(2)_X + SM Higgs (SU(2)cSM) -- LISA-band (mHz) signal with additional Higgs portal
- **arXiv:2306.09411**: Constraints on stable dark sectors from Delta N_eff

This model is a minimal, self-contained CW gauge theory for FOPT+GW production, compatible with the semianalytic pipeline backend and ready for scanning.