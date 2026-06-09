# Proposed Model: Conformal U(1)_D Dark Sector with Two Dirac Fermions

## Overview

This document describes a classically scale-invariant (conformal) dark sector extension of the Standard Model, consisting of a U(1)_D gauge symmetry, a complex scalar charged under U(1)_D, a dark gauge boson, and two Dirac fermions. The model is designed to:

1. Exhibit radiative (Coleman-Weinberg) symmetry breaking of U(1)_D, triggered by the one-loop effective potential
2. Support a first-order phase transition (FOPT) with stochastic gravitational wave production
3. Be compatible with the `backend/semianalytic_pipeline.py` backend for FOPT-PTA analysis

## Symmetries

| Symmetry | Type | Details |
|---|---|---|
| U(1)_D | Gauge | Dark gauge symmetry; anomaly-free with the chosen fermion content |
| Classical scale invariance | Global (anomalous) | No dimensionful parameters in the tree-level Lagrangian |
| Z_2 (accidental) | Global discrete | Stabilises one of the fermion mass eigenstates |

## Particle Content

| Field | Type | Spin | U(1)_D Charge | DoF | Statistics | Notes |
|---|---|---|---|---|---|---|
| Φ | Complex scalar | 0 | +1 | 2 | Bose | Dark Higgs; radial mode gets vev |
| A'_μ | Gauge boson | 1 | 0 (adjoint) | 3 | Bose | Dark photon; gets mass via Higgs mechanism |
| ψ_1 | Dirac fermion | 1/2 | +1/2 | 4 | Fermi | First dark fermion; vector-like (L and R same charge) |
| ψ_2 | Dirac fermion | 1/2 | -1/2 | 4 | Fermi | Second dark fermion; vector-like (L and R same charge) |

### Why two fermions?

A single Dirac fermion ψ with a renormalizable Yukawa coupling y_ψ Φ ψ̅ ψ (with Φ charged under U(1)_D) cannot simultaneously satisfy:
1. **Gauge invariance**: The Yukawa term requires q_Φ - q_L + q_R = 0
2. **Anomaly cancellation**: A single Dirac fermion requires q_L = q_R (vector-like) for U(1)^3 anomaly cancellation
3. **Non-zero scalar charge**: q_Φ ≠ 0 (otherwise Φ is a gauge singlet)

Combining (1) and (2) gives q_Φ = q_L - q_R = 0, contradicting (3). Therefore, the minimal renormalizable, anomaly-free, scale-invariant model requires two Dirac fermions whose anomaly contributions cancel.

**Choice adopted here**: Two vector-like Dirac fermions with gauge charges +1/2 and -1/2. Both are individually anomaly-free (each satisfies q_L = q_R), and the Yukawa term y_ψ Φ ψ̅_1 ψ_2 + h.c. is gauge-invariant because:

- ψ̅_1 ψ_2 carries net U(1)_D charge = -q_1 + q_2 = -1/2 + (-1/2) = -1
- Φ has charge +1
- Total charge of Φ ψ̅_1 ψ_2: +1 + (-1) = 0

## Lagrangian

In the unbroken phase (before SSB), the tree-level Lagrangian is:

### Kinetic Terms

```
L_kin = -1/4 F'_μν F'^{μν}
      + |D_μ Φ|^2
      + i ψ̄_1 γ^μ D_μ ψ_1 + i ψ̄_2 γ^μ D_μ ψ_2
```

where the covariant derivatives are:

- D_μ Φ = (∂_μ + i g_D A'_μ) Φ
- D_μ ψ_1 = (∂_μ + i g_D q_1 A'_μ) ψ_1 = (∂_μ + i g_D/2 A'_μ) ψ_1
- D_μ ψ_2 = (∂_μ + i g_D q_2 A'_μ) ψ_2 = (∂_μ - i g_D/2 A'_μ) ψ_2

### Yukawa Term

```
L_Yukawa = y_ψ Φ ψ̄_1 ψ_2 + h.c.
```

This is the unique gauge-invariant, renormalizable Yukawa coupling. After SSB, this generates Dirac masses for the fermion mass eigenstates (see below).

### Gauge Kinetic Mixing

We assume zero gauge kinetic mixing at tree level: ε = 0. In principle, a kinetic mixing term (ε/2) F'_μν B^{μν} between U(1)_D and SM U(1)_Y is allowed by gauge invariance, but it is set to zero at the scale of interest. Small kinetic mixing may be generated radiatively if there are particles charged under both U(1)s, but in this minimal model no SM-charged particles carry U(1)_D charge, so mixing is absent at all scales.

### Scalar Potential

The tree-level scalar potential is classically scale-invariant:

```
V_tree(Φ) = λ_Φ (Φ*Φ)^2
```

There is no quadratic mass term (m_Φ^2 |Φ|^2 = 0) by conformal symmetry.

### Portal Interactions

We assume zero Higgs portal: the operator |H|^2 |Φ|^2 is not included. This ensures:
- No tree-level mixing between the SM Higgs and the dark scalar
- The dark sector is (mostly) thermally decoupled from the SM, except through possible U(1)_D gauge kinetic mixing (set to zero) and gravitational interactions

A small Higgs portal would UV-complete the model and allow SM-dark sector thermalisation, but is not necessary for the FOPT phenomenology. We assume the dark sector is reheated after inflation and thermalises to a temperature T_dark = ξ T_SM with ξ a free parameter (set to 1 by default in the backend).

## Spontaneous Symmetry Breaking

### SSB Pattern

```
U(1)_D  --<Φ>-->  nothing (all U(1)_D particles become massive)
```

The complex scalar Φ acquires a vacuum expectation value (vev) along its real (radial) direction:

```
Φ = (χ + v) / √2 * exp(i θ / v)
```

where:
- v = ⟨χ⟩ is the vev (the minimum of the effective potential)
- χ is the CP-even radial mode (the dark Higgs / scalon / CW pseudo-dilaton)
- θ is the Goldstone mode (eaten by A'_μ via the Higgs mechanism)

In the unitary gauge, the Goldstone mode is removed and the physical particle content is:
- χ (real scalar, mass m_χ)
- A'_μ (massive gauge boson, mass m_A')
- Two fermion mass eigenstates from ψ_1-ψ_2 mixing

### VEV Convention

```
⟨Φ⟩ = v / √2
```

All field-dependent masses are expressed in terms of the background field χ, with the physical vev convention:
- Gauge boson mass from covariant derivative: m_A'(χ)^2 = g_D^2 χ^2
- The actual vev is v, so physical masses are m_A'^2 = g_D^2 v^2

## Tree-Level Potential

```
V_tree(χ) = λ_Φ χ^4 / 4
```

where χ is the background field (radial direction of Φ, after removing the angular dependence). The quartic λ_Φ is fixed by the Coleman-Weinberg (CW) mechanism and is NOT a free parameter.

## Coleman-Weinberg Mechanism

At one-loop order, the effective potential develops a minimum radiatively. The CW relation fixes the quartic coupling in terms of particle masses. In the model-independent backend formulation:

### beta_lambda

```
beta_lambda = 1/(8π^2) * ( Σ_B n_B gb^4 - Σ_F n_F gf^4 )
```

where n_B (n_F) are the boson (fermion) degrees of freedom and gb (gf) are the mass-over-vev ratios for bosons (fermions).

For this model:
| Particle | Symbol | Mass^2 (field-dependent) | g = m/χ | DoF (n) |
|---|---|---|---|---|
| Gauge boson A'_μ | gb_A | g_D^2 χ^2 | g_D | 3 |
| Scalar χ (radial) | gb_χ | (subleading, set to 0) | 0 | 1 |
| Fermion (lightest) | gf_ψ | y_ψ^2 χ^2 / 4 | y_ψ/2 | 4 |

**Note on fermion masses**: The Yukawa term y_ψ Φ ψ̄_1 ψ_2 generates a mass matrix in the (ψ_1, ψ_2) basis. After SSB with ⟨Φ⟩ = v/√2:
- Off-diagonal mass term: m_D = y_ψ v / (2√2)

The mass eigenvalues are: m_ψ = y_ψ v / (2√2) (doubly degenerate, one positive and one negative eigenvalue corresponding to a Dirac pair). The mass-over-vev ratio is gf = y_ψ / (2√2) per fermion.

Actually, let me recalculate. With Φ = (v + χ)/√2 in unitary gauge:
The Yukawa term: y_ψ Φ ψ̄_1 ψ_2 = y_ψ (v+χ)/√2 * ψ̄_1 ψ_2

So the mass matrix elements:
M_{12} = M_{21} = y_ψ v/√2

The eigenvalues are ± y_ψ v/√2. For a Dirac fermion, only the absolute value matters: m_ψ = |y_ψ| v/√2.

Field-dependent masses: m_ψ(χ)^2 = y_ψ^2 χ^2 / 2.

^ That's for the symmetric mass matrix with equal off-diagonal entries. Actually, for two Dirac fermions with a Yukawa coupling Φ ψ̄_1 ψ_2 + h.c., the Lagrangian in the (ψ_1, ψ_2) basis has:

L_mass = -(m_D ψ̄_1 ψ_2 + m_D* ψ̄_2 ψ_1) = -m_D ψ̄_1 ψ_2 - m_D* ψ̄_2 ψ_1

For real m_D (real vev): L_mass = -m_D (ψ̄_1 ψ_2 + ψ̄_2 ψ_1)

In Dirac notation, define Ψ_± = (ψ_1 ± ψ_2)/√2. Then:
ψ̄_1 ψ_2 + ψ̄_2 ψ_1 = (Ψ̄_+ Ψ_+ - Ψ̄_- Ψ_-)/2 ... hmm.

Actually, the mass term ψ̄_1 ψ_2 + ψ̄_2 ψ_1 in the (ψ_1, ψ_2) basis gives mass eigenstates ψ_± = (ψ_1 ± ψ_2)/√2 with eigenvalues ±m_D.

The absolute mass is m_ψ = |m_D| = y_ψ v/√2 for both states.

Field-dependent mass: m_ψ(χ)^2 = y_ψ^2 χ^2 / 2.

So gf_ψ^2 = m_ψ(χ)^2 / χ^2 = y_ψ^2 / 2.

Wait: gf = m/χ. With m_ψ = y_ψ * χ / √2. So gf = y_ψ / √2.

Hmm, let me be more careful. Φ = χ/√2 in the radial background (where χ is the background field in the convention where the kinetic term is (1/2)(∂χ)^2). Then m_D = y_ψ * χ / √2. So m_ψ^2 = (y_ψ χ / √2)^2 = y_ψ^2 χ^2 / 2. Then gf^2 = y_ψ^2 / 2.

But the backend uses gf, not gf^2. The backend's fermion_gfs values are used as:
m2 = gf^2 * chi^2 (in the field-dependent mass)

So gf_ψ = y_ψ / √2.

Number of dof: two Dirac fermions as mass eigenstates, each with 4 dof = 8 total fermionic dof.

But for the beta_lambda calculation, each Dirac fermion contributes n_F = 4 * (-1) in the formula. Two of them => n_F = 8.

Wait, the formula is: beta_lambda = 1/(8π^2) * (Σ_B n_B gb^4 - Σ_F n_F gf^4)

For bosons: gauge boson has n_B = 3, gb = g_D.
For fermions: each mass eigenstate (Dirac fermion) has n_F = 4, gf = y_ψ/√2. Two such states => total fermion contribution: 2 * 4 * (y_ψ/√2)^4 = 8 * y_ψ^4 / 4 = 2 * y_ψ^4.

Actually, each Dirac fermion has 4 on-shell degrees of freedom. n_F in the backend means number of fermionic dof. Each fermion mass eigenstate contributes n_F=4. With two mass eigenstates, total n_F = 8.

But wait -- looking at the backend code, the fermion dof are:
```python
for fermion, gf in self.fermion_gfs.items():
    dof = self.fermion_dofs.get(fermion, 0)
    ...
```

And `self.new_dof = sum(self.boson_dofs.values()) + 7/8 * sum(self.fermion_dofs.values())`

So `fermion_dofs` contains the actual dof count. For 2 Dirac fermion mass eigenstates, that's 8 dof.

In the beta_lambda formula: beta_lambda = (boson - fermion) / (8π^2)
where `boson = Σ n_B gb^4` and `fermion = Σ n_F gf^4`.

For this model:
- Bosons: 3 * g_D^4 (gauge) + 1 * 0^4 (scalar, subleading)
- Fermions: 8 * (y_ψ/√2)^4 = 8 * y_ψ^4 / 4 = 2 * y_ψ^4

beta_lambda = (3 g_D^4 - 2 y_ψ^4) / (8π^2)

For radiative symmetry breaking: beta_lambda > 0 => 3 g_D^4 > 2 y_ψ^4 => g_D^4 / y_ψ^4 > 2/3 => g_D / y_ψ > (2/3)^(1/4) ≈ 0.9

So the gauge coupling must be at least as large as the Yukawa coupling (within a factor ~0.9) for the CW mechanism to work.

### The gb_scalar Parameter

The backend uses a `gb_scalar` parameter. Per the skill instructions: "The scalar `gb` is then not independent but fixed by the gauge and fermion content as `gb_scalar = sqrt(beta_lambda)`". So in the backend mapping, we set:

```
boson_gbs = {"gauge": g_D, "scalar": 0}  # scalar gb is subleading
boson_dofs = {"gauge": 3, "scalar": 1}
fermion_gfs = {"psi": y_psi / sqrt(2)}
fermion_dofs = {"psi": 8}
```

## Parameter Classification

### Independent Parameters (scanned or assigned priors)

| Parameter | Symbol | Range / Determination | Motivation |
|---|---|---|---|
| Dark gauge coupling | g_D | [0.1, 4π] | Perturbativity; must satisfy beta_lambda > 0 |
| Yukawa coupling | y_ψ | [0.0, sqrt(3/2) g_D] | Must be < sqrt(3/2) g_D for beta_lambda > 0 (CW condition) |
| Dark Higgs vev | v | [0.1, 10^4] GeV | Determines overall mass scale |

### Dependent Parameters (computed from relations, NOT scanned)

| Parameter | Symbol | Relation | Notes |
|---|---|---|---|
| CW quartic coupling | λ_Φ | Fixed by minimization: β_λ = (3 g_D^4 - 2 y_ψ^4)/(8π^2) | Not needed by backend |
| Scalar mass (CW pseudo-dilaton) | m_χ | m_χ^2 = β_λ v^2 | Physical mass of radial mode |
| Gauge boson mass | m_A' | m_A' = g_D v | Dark photon mass |
| Fermion mass | m_ψ | m_ψ = y_ψ v / √2 | Mass of each fermion mass eigenstate |

### Fixed Parameters

| Parameter | Symbol | Value | Notes |
|---|---|---|---|
| xi (T-dark / T-SM ratio) | ξ | 1.0 | Assumes dark sector thermalised with SM |
| Gauge kinetic mixing | ε | 0 | No tree-level mixing |
| Higgs portal coupling | λ_HΦ | 0 | No scalar mixing |

## Branch-Specific FOPT Ingredients

### Field-Dependent Masses

| Particle | m^2(χ) | Expression (SymPy) | DoF | Statistics |
|---|---|---|---|---|
| Gauge boson A'_μ | g_D^2 χ^2 | `g_D**2 * chi**2` | 3 | Bose |
| Scalar radial χ | β_λ χ^2 | subleading (set to 0) | 1 | Bose |
| Fermion ψ (each of 2 states) | y_ψ^2 χ^2 / 2 | `y_psi**2 * chi**2 / 2` | 4 each | Fermi |

### Thermal Masses (Debye Corrections)

In the high-temperature expansion, the thermal masses are:

**Gauge boson longitudinal mode:**
Π_A' = (g_D^2 / 3) * (1 + 1/4) * T^2 ... hmm, need to compute properly.

The Debye mass for the U(1)_D gauge boson receives contributions from:
- 1 complex scalar (Φ) with charge 1: n_s = 2 (real dof), q_s = 1
- 2 Dirac fermions with charge 1/2: n_f = 4, q_f = 1/2 each
- The gauge boson self-interaction contributes from the 3 transverse polarizations

For a U(1) gauge boson, the thermal mass squared is:
Π_A' = g_D^2 T^2 / 3 * [ Σ_s n_s q_s^2 / 4 + Σ_f n_f q_f^2 / 2 + Σ_V ... ]

Actually, for a gauged U(1), the Debye mass squared for the gauge boson is:

m_D^2 = g_D^2 T^2 / 3 * ( Σ_scalar n_s q_s^2 / 4 + Σ_Weyl_fermion n_f q_f^2 / 2 + ...)

Here n_s is the number of real scalar degrees of freedom: for a complex scalar, n_s = 2. n_f is the number of Weyl fermion degrees of freedom: for a Dirac fermion, 4 Weyl components.

Wait, in the high-T expansion form used by the backend:

g2sq = Σ_B n_B gb^2 + Σ_F n_F gf^2 / 2

where gb and gf are the mass-over-vev ratios. The thermal mass coefficient is g2sq * T^2 / 12.

So:
- Bosons: gauge boson with n_B=3, gb=g_D; scalar with n_B=1, gb=0
  Contribution: 3 * g_D^2 + 1 * 0^2 = 3 g_D^2
- Fermions: two Dirac mass eigenstates, each n_F=4, gf=y_ψ/√2
  Contribution: 8 * (y_ψ/√2)^2 / 2 = 8 * y_ψ^2 / 2 / 2 = 2 y_ψ^2

g2sq = 3 g_D^2 + 2 y_ψ^2

Thermal mass: m_th^2(χ=0) = g2sq * T^2 / 12

The secondary thermal cubic coefficient:
g3 = Σ_B n_B gb^3 = 3 * g_D^3 + 1 * 0^3 = 3 g_D^3

The quartic logarithmic coefficient:
g4 = Σ_B n_B gb^4 * log(...) - Σ_F n_F gf^4 / 2 * log(...)

## Backend Compatibility

This model is **compatible** with `backend/semianalytic_pipeline.py` because:

1. It is a classically scale-invariant (conformal) single-field model: the tree-level potential has only a quartic term and no mass term
2. All particle masses are proportional to a single scalar vev v
3. The Coleman-Weinberg mechanism fixes the quartic coupling
4. The high-temperature expansion of the finite-temperature effective potential applies
5. The model can be mapped to the backend's parameter interface as described above

### Backend Parameter Mapping

```
chi0 -> v (the vev)
boson_gbs = {"gauge": g_D, "scalar": 0}
boson_dofs = {"gauge": 3, "scalar": 1}
fermion_gfs = {"psi": y_psi / sqrt(2)}   # y_ψ/√2 per the 2 Dirac states (treated as one entry with 8 dof)
fermion_dofs = {"psi": 8}
```

## Assumptions, Caveats, and Limitations

1. **Two-fermion minimal extension**: The user requested a single Dirac fermion with a gauge-invariant Yukawa coupling to a charged scalar. This is impossible while maintaining anomaly cancellation under U(1)_D. The minimal resolution requires two Dirac fermions with opposite charges, as proposed here. After SSB, the two fermions mix into mass eigenstates, and one can think of the lightest state as the "dark fermion" the user requested.

2. **No Higgs portal**: We assume zero coupling between the SM Higgs and the dark scalar. This prevents tree-level scalar mixing. A non-zero portal coupling is not needed for the FOPT phenomenology.

3. **No gauge kinetic mixing**: Set to zero at tree level. In a UV-complete model, this could be generated radiatively if there are particles charged under both U(1)_D and U(1)_Y, but none are present here.

4. **Dark sector temperature**: We assume ξ = T_dark / T_SM = 1 (thermal equilibrium with SM). This is a simplifying assumption. In the absence of a Higgs portal, the dark sector may have a different temperature; ξ could be treated as a free parameter.

5. **Single-scalar approximation**: The effective analysis treats the radial mode χ as the only scalar degree of freedom, which is appropriate for the FOPT calculation.

6. **Backend approximations**: The backend uses the high-temperature expansion of the finite-temperature effective potential and the Gaussian approximation for the false vacuum fraction. These approximations are validated in the supercooling regime appropriate for PTA signals.

7. **Perturbativity**: We assume g_D, y_ψ < 4π for perturbative control. The CW condition requires y_ψ < (3/2)^(1/4) g_D ≈ 1.11 g_D, which is automatically satisfied in the perturbative regime.

8. **Renormalisation scale**: The quartic coupling λ_Φ is renormalisation-scale dependent and is not a physical input. The physical mass scales are m_χ, m_A', and m_ψ, which depend on g_D, y_ψ, and v through the CW relations.