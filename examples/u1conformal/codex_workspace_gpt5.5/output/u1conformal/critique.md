# Critique: u1conformal

Date: 2026-06-10  
Agent: critic-agent  
Branch: fopt-pta

## Verdict

The user-supplied classically scale-invariant dark `U(1)_D` model is internally consistent for the `fopt-pta` branch and is compatible with `backend/semianalytic_pipeline.py`.

No unresolved red flags were found. The model is validated with warnings. The validated downstream model is written in `output/u1conformal/model.md` and `output/u1conformal/handoff_model.json`.

## Gauge Group, Charge Convention, and Degrees of Freedom

- Gauge group: `U(1)_D`.
- Scalar: one complex scalar `Phi` with charge `q_Phi = 1`, fixed by `D_mu = partial_mu - i * g_D * A'_mu`.
- Gauge boson: one Abelian gauge field `A'_mu`.
- Before symmetry breaking: the dark sector has 2 real scalar degrees of freedom plus 2 transverse massless gauge-boson polarizations.
- After symmetry breaking: `U(1)_D` is fully Higgsed; the Goldstone `G` is eaten, giving one massive vector with 3 polarizations plus one real radial scalar `rho`.
- The degree-of-freedom count matches: `2 + 2 = 1 + 3 = 4`.

Because the model has no new chiral fermions, there are no new gauge, mixed gauge-gravity, or cubic Abelian chiral anomalies to cancel. Scalar matter does not generate chiral gauge anomalies.

## Lagrangian Checks

The dark-sector terms

```text
|D_mu Phi|**2 - lambda_Phi * |Phi|**4 - (1/4) * F'_munu * F'**munu
```

are gauge invariant for `q_Phi = 1`. The scalar quartic is the only dark-sector tree-level potential term, consistent with the stated classically scale-invariant dark sector.

The optional terms

```text
lambda_HP * |H|**2 * |Phi|**2
(epsilon / 2) * F'_munu * F**munu
```

are gauge invariant and dimension four. They are acceptable as phenomenological portals if treated as negligible for the FOPT potential. Their actual sizes must be specified later for laboratory, BBN, CMB, dark-photon, and late-decay constraints.

## Coleman-Weinberg Parameter Basis

The correct branch parameter basis is:

- Independent FOPT scan parameters: `v`, `g_D`.
- Dependent parameters: `lambda_Phi`, `beta_lambda`, `m_Aprime`, `m_rho`.
- Fixed assumptions for the minimal FOPT backend: `q_Phi = 1`, no fermions, negligible portal/kinetic-mixing effects on the effective potential, and `xi = T_dark / T_visible = 1`.

For the gauge-only minimal model,

```text
beta_lambda = 3 * g_D**4 / (8 * pi**2)
m_rho**2 = beta_lambda * v**2
```

Since `g_D > 0`, `beta_lambda > 0`, so the Coleman-Weinberg radiative-symmetry-breaking condition used by the backend is satisfied. `lambda_Phi` must not be scanned independently.

## SSB and Mass Conventions

The prompt convention

```text
Phi = (chi + rho + i * G) / sqrt(2)
```

is consistent with full breaking of `U(1)_D`. Expanding `|D_mu Phi|**2` around the background gives

```text
|D_mu Phi|**2 contains (1/2) * g_D**2 * chi**2 * A'_mu * A'**mu
```

and because a real massive vector has mass term `(1/2) * m_Aprime**2 * A'_mu * A'**mu`,

```text
m_Aprime**2(chi) = g_D**2 * chi**2
```

This matches the prompt and the charge-one convention used in arXiv:2502.19478. It must not be mixed directly with arXiv:2105.01007 benchmarks using `m_ZD = 2 * g_D * M` without an explicit convention translation.

The tree-level scalar masses along the background direction are, from `V_tree = lambda_Phi * chi**4 / 4`,

```text
m_rho,tree**2(chi) = 3 * lambda_Phi * chi**2
m_G,tree**2(chi) = lambda_Phi * chi**2
```

At the Coleman-Weinberg minimum the physical radial mass is instead set by the one-loop curvature relation stated in the prompt,

```text
m_rho**2 = beta_lambda * v**2
```

The Goldstone is eaten by `A'` after symmetry breaking.

## Thermal Masses and FOPT Backend

The prompt does not specify full Debye/thermal masses for scalar, Goldstone, or longitudinal gauge modes. This is not a blocker for `backend/semianalytic_pipeline.py`, because that backend uses mass-over-vev ratios and degrees of freedom for conformal single-field models and does not require explicit Daisy-resummed thermal masses as inputs.

It is a warning for any later full one-loop finite-temperature implementation. A full Landau-gauge/Arnold-Espinosa or Parwani implementation would need a precise thermal-mass prescription, gauge choice, and resummation scheme.

## Backend Compatibility

The model matches the selection rule for `backend/semianalytic_pipeline.py`:

- classically scale-invariant;
- single scalar background field `chi`;
- no explicit tree-level scalar mass term;
- all relevant masses proportional to the same vev;
- CW-fixed quartic treated as dependent;
- backend input can use `boson_gbs = {"Aprime": g_D}`, `boson_dofs = {"Aprime": 3}`, `fermion_gfs = {}`, `fermion_dofs = {}`.

The backend already assumes `xi = 1`, matching the prompt.

## Literature Convention Caveats

The preliminary literature handoff identifies two especially relevant convention issues:

- arXiv:2105.01007 is the closest minimal dark `U(1)_D` PTA-scale benchmark, but it uses `m_ZD = 2 * g_D * M`. Its mass/vev benchmarks require translation before use with this prompt's `m_Aprime = g_D * v`.
- arXiv:2502.19478 uses the same charge-one mass convention `m_Aprime = g * v` and is directly useful for PTA/PTArcade priors, but it includes anomaly-cancelling fermions and dark-matter dynamics absent from the target model. Its fermion and thermal-mass effects must not be imported into the minimal no-fermion model without explicitly extending the model.

Across the literature, Landau-gauge finite-temperature potentials, Arnold-Espinosa Daisy resummation, supercooling/percolation failure modes, and `Delta N_eff`/BBN constraints are recurring theory and cosmology caveats.

## Warnings for Downstream Agents

1. Do not scan `lambda_Phi`; compute it from the CW/backend relation.
2. Do not use arXiv:2105.01007 masses without translating the charge/vev convention.
3. Treat the missing full thermal masses as a warning for full finite-temperature potentials, not as a blocker for the semi-analytic backend.
4. Portal and kinetic-mixing parameters are not specified quantitatively. They are negligible for FOPT by assumption, but the constraint agent will need values or ranges to evaluate laboratory and cosmological constraints.
5. The assumptions "small portals" and "xi = 1 thermalization" may be phenomenologically compatible only in part of parameter space; this must be checked downstream.
