# Scale-Invariant Dark U(1) with Z' and Dirac Dark Fermion

**Model name:** `scale-invariant-dark-u1-zprime`
**Branch:** `fopt-pta`
**Backend:** `semianalytic_pipeline.py` (classically scale-invariant single-scalar Coleman-Weinberg)

## 1. Overview

A classically scale-invariant (conformal) hidden sector with a gauged dark
`U(1)_D`. The sector contains a single complex scalar `Phi`, the dark gauge
boson `Z'`, and one Dirac dark fermion `chi`. There are **no explicit mass
scales** in the Lagrangian: the only dimensionful scale is generated
dynamically by radiative (Coleman-Weinberg) symmetry breaking of `U(1)_D`,
driven by the `Z'` loop. The resulting supercooled, strongly first-order phase
transition produces a stochastic gravitational-wave background in the
nanohertz band relevant for the NANOGrav/PTA signal.

The dark sector communicates with the Standard Model only gravitationally in
the minimal proposal (an optional Higgs-portal `lambda_p |H|^2 |Phi|^2` and
gauge kinetic mixing `epsilon` are allowed by the symmetries but set to zero /
negligible for the FOPT analysis; they do not affect the single-field
conformal dynamics).

## 2. Symmetries

- **Gauge:** `U(1)_D` (new), with the SM gauge group untouched. The dark sector
  is a SM gauge singlet.
- **Classical scale invariance:** the tree-level Lagrangian contains only
  dimension-4 operators; no mass terms and no dimensionful couplings.
- **Global / discrete:** the Lagrangian preserves a dark fermion number
  `U(1)_chi` (the fermion mass term is Dirac and number-conserving), making the
  lightest dark fermion stable — a potential dark-matter candidate. A residual
  `Z_2` (charge conjugation of the dark sector) is also present but not used.

## 3. Field content and charges

| Field    | Spin | `U(1)_D` charge | SM rep    | Statistics | DOF | Comment |
|----------|------|-----------------|-----------|------------|-----|---------|
| `Phi`    | 0    | `+1`            | singlet   | boson      | 2   | complex dark scalar (radial = pseudo-dilaton) |
| `Z'`     | 1    | adjoint (0)     | singlet   | boson      | 3   | dark gauge boson, massive after SSB |
| `psi_L`  | 1/2  | `+1/2`          | singlet   | fermion    | 2   | left Weyl, forms Dirac `chi` |
| `psi_R`  | 1/2  | `-1/2`          | singlet   | fermion    | 2   | right Weyl, forms Dirac `chi` |
| `eta_L`  | 1/2  | `-1/2`          | singlet   | fermion    | 2   | left Weyl spectator (anomaly partner) |
| `eta_R`  | 1/2  | `+1/2`          | singlet   | fermion    | 2   | right Weyl spectator (anomaly partner) |

`psi_{L,R}` combine into a Dirac dark fermion `chi` with `U(1)_D` charges
`(q_L, q_R) = (+1/2, -1/2)`. The pair `eta_{L,R}` form a second Dirac fermion
with the **opposite** chiral charge assignment `(-1/2, +1/2)`, so the full
fermion content is **vector-like** as a whole and exactly anomaly-free (see
Sec. 4). Both Dirac fermions acquire mass from the same Yukawa coupling to
`Phi`; they are mass-degenerate and together constitute the dark fermion `chi`
with total fermionic degrees of freedom `n_chi = 8`.

(One may alternatively view this as a single vector-like Dirac fermion with
charge `+1/2` plus its mirror with charge `-1/2`; the physics and the masses
are identical. The doubling is the minimal way to cancel the gauge and
gravitational anomalies while keeping a Yukawa mass `~ Phi`.)

## 4. Anomaly cancellation

Writing all fermions as left-handed Weyl fields, the charges are:
- `psi_L`: `+1/2`
- `(psi_R)^c`: `+1/2`
- `eta_L`: `-1/2`
- `(eta_R)^c`: `-1/2`

- `U(1)_D^3` anomaly: `(1/2)^3 + (1/2)^3 + (-1/2)^3 + (-1/2)^3 = 0`.
- `U(1)_D`-gravitational (mixed) anomaly: `(1/2)+(1/2)+(-1/2)+(-1/2) = 0`.

Both anomalies vanish. The dark fermion sector is anomaly-free. (Equivalently:
the spectrum is vector-like, `{+1/2, -1/2}` Dirac plus its charge mirror, so it
is automatically anomaly-free.)

## 5. Lagrangian

All terms are dimension-4; no mass scale appears.

```
L = -1/4 * Fp_{mu nu} * Fp^{mu nu}
    + |D_mu Phi|^2
    + i * psibar * gammaslash_D * psi
    + i * etabar * gammaslash_D * eta
    - ( y * Phi * psibar_L * psi_R + y * Phi * etabar_L * eta_R + h.c. )
    - lambda * |Phi|^4
```

with covariant derivatives
```
D_mu Phi   = ( d_mu - i * g_D * 1   * Zp_mu ) Phi
D_mu psi_L = ( d_mu - i * g_D * (1/2) * Zp_mu ) psi_L
D_mu psi_R = ( d_mu - i * g_D * (-1/2) * Zp_mu ) psi_R
(and the charge-conjugate assignment for eta)
Fp_{mu nu} = d_mu Zp_nu - d_nu Zp_mu
```

The Yukawa term `y * Phi * psibar_L * psi_R` is gauge invariant because
`q(Phi) + q(psi_R) - q(psi_L) = 1 + (-1/2) - (1/2) = 0`. Same for `eta`.

There is **no** tree-level mass term and **no** quadratic scalar term, by
classical scale invariance. The tree potential is purely quartic.

## 6. Radiative symmetry breaking (Coleman-Weinberg)

Write `Phi = (1/sqrt(2)) * chi * exp(i theta)`, with `chi` the real radial
direction (the flat direction / pseudo-dilaton) and `theta` the Goldstone
eaten by `Z'`. The tree-level potential along the flat direction is
```
V_tree(chi) = (lambda/4) * chi**4
```
For small `lambda` the Coleman-Weinberg one-loop correction generates a minimum
at a non-zero `chi = w` (the vev), dynamically breaking `U(1)_D` and fixing the
quartic by the minimization (CW) condition. In the backend's
model-independent form,
```
beta_lambda = (1/(8*pi**2)) * ( sum_B n_B * gb**4  -  sum_F n_F * gf**4 )
```
with radiative breaking requiring `beta_lambda > 0` (bosonic `Z'` contribution
must dominate the fermionic one). The CW radial-scalar (pseudo-dilaton) mass is
the dependent quantity
```
m_chi_radial**2 = beta_lambda * w**2
```
The quartic `lambda` itself is renormalization-scale dependent, is fixed by the
CW condition (dependent), and is **not** scanned or used by the backend.

## 7. Mass spectrum (after `<chi> = w`)

| Particle        | Mass                | mass/vev ratio          | DOF |
|-----------------|---------------------|-------------------------|-----|
| `Z'`            | `g_D * w`           | `gb_gauge = g_D`        | 3   |
| `chi` (Dirac x2)| `y * w / sqrt(2)`   | `gf_fermion = y/sqrt(2)`| 8   |
| radial `chi`    | `sqrt(beta_lambda)*w`| dependent (CW)         | 1   |
| Goldstone       | 0 (eaten by `Z'`)   | —                       | —   |

Backend inputs (the only quantities the semianalytic pipeline needs):
- `gb_gauge = g_D`, `dof = 3`
- `gf_fermion = y / sqrt(2)`, `dof = 8`
- `chi0 = w` (the vev, in GeV)

The scalar/Goldstone contributions are negligible and not supplied to the
backend, as instructed.

## 8. Field-dependent and thermal masses

Background field `chi` (real), `Phi -> chi/sqrt(2)`.

Field-dependent (tree, along the flat direction):
- `Z'`:   `m2 = g_D**2 * chi**2`,           dof 3, boson
- `chi`:  `m2 = (y**2 / 2) * chi**2`,        dof 8, fermion
- radial: `m2 = 3 * lambda * chi**2`,        dof 1, boson (negligible)
- Goldstone: `m2 = lambda * chi**2`,         dof 1, boson (negligible)

Thermal (Debye) masses (leading high-T, used to build the thermally generated
barrier; longitudinal `Z'` Debye mass dominant):
- `Z'` longitudinal Debye: `Pi_Zp = (1/3) * g_D**2 * T**2 * (q_Phi**2 + sum_f q_f**2)`
  With one complex scalar of charge 1 and the dark fermions of charge `1/2`,
  `Pi_Zp = g_D**2 * T**2 * ( 1/3 + (1/3) * n_chi_eff )`; the backend internally
  applies the standard high-T thermal-mass structure for the bosonic sector.

The semianalytic pipeline reconstructs the thermally generated barrier from the
high-temperature expansion using `gb_gauge`, `gf_fermion`, and the dof, so only
those ratios and the vev are required as user input; the analytic thermal
structure above is provided for completeness and verification.

## 9. Parameters

**Independent (scannable):**
- `g_D` — dark gauge coupling. Range `[0.1, 1.5]`. Sets `gb_gauge` and the
  strength of the transition; must dominate fermions for `beta_lambda > 0`.
- `y` — dark Yukawa coupling. Range `[0.0, 1.0]`. Sets `gf_fermion = y/sqrt(2)`;
  bounded above so bosons dominate.
- `w` — radiatively generated vev (GeV). Range `~[1e2, 1e6]` GeV; sets the
  overall scale so that the nucleation/percolation temperature lands in the
  PTA/nanohertz window (`T ~ MeV–GeV` after strong supercooling).

**Dependent:**
- `lambda` — fixed by the CW minimization condition (dependent, not scanned).
- `beta_lambda = (1/(8*pi**2)) * ( 3*g_D**4 - 8*(y/sqrt(2))**4 )`.
- `m_chi_radial = sqrt(beta_lambda) * w`.
- `m_Zp = g_D * w`, `m_chi = y*w/sqrt(2)`.

**Fixed / assumptions:**
- Higgs portal `lambda_p = 0`, kinetic mixing `epsilon = 0` (negligible;
  decoupled SM in the FOPT dynamics).
- Renormalization scale `mu = w`; no RG running, no Daisy resummation
  (backend convention).

## 10. Assumptions, caveats, limitations

- Single-field conformal approximation: the FOPT is driven entirely by the
  `U(1)_D` radial direction; SM and portal back-reaction neglected.
- `beta_lambda > 0` (bosons dominate) is required — enforced by `y` small
  relative to `g_D`.
- High-temperature expansion + Gaussian percolation approximation of the
  backend (validated in arXiv:2602.02829 for the supercooled regime).
- No RG running / no Daisy resummation (`mu = w`).
- The strong supercooling needed for a nanohertz PTA signal requires small
  `g_D`/`lambda`; the vev `w` is chosen so the percolation temperature lands in
  the relevant range.
- Eternal-inflation regions (decay rate < Hubble) must be excluded downstream.

## 11. Backend compatibility

Compatible with `semianalytic_pipeline.py`: single classically scale-invariant
scalar, all masses `~ w`, no tree mass term, CW-fixed quartic. Inputs map to
`chi0 = w`, `boson_gbs = {Zp: g_D}` / `boson_dofs = {Zp: 3}`,
`fermion_gfs = {chi: y/sqrt(2)}` / `fermion_dofs = {chi: 8}`.
