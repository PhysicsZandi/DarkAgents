# Critique: conformal_u1_dark_fopt

Branch: `fopt-pta`

## Verdict

The model is usable for downstream FOPT/PTA scans with warnings. No unresolved red flags remain after minimal repairs to the model description.

The validated downstream model is written to `output/conformal_u1_dark_fopt/model.md` and `output/conformal_u1_dark_fopt/handoff_model.json`.

## Core Checks

### Gauge and Gravitational Anomalies

The only new chiral fermions charged under `U(1)_D` are two left-handed Weyl fermions:

- `psi_plus` with `q_D = +1`
- `psi_minus` with `q_D = -1`

The cubic Abelian anomaly is proportional to

```text
sum q_D^3 = (+1)^3 + (-1)^3 = 0
```

The mixed gravitational anomaly is proportional to

```text
sum q_D = +1 - 1 = 0
```

All new fermions are Standard Model singlets, so there are no new mixed Standard Model gauge anomalies.

### Yukawa Gauge Invariance

With `q_Phi = 2`, the proposed Majorana-type Weyl Yukawa terms are gauge invariant:

```text
Phi_dagger psi_plus psi_plus:  -2 + 1 + 1 = 0
Phi psi_minus psi_minus:       +2 - 1 - 1 = 0
```

A Dirac bilinear `psi_plus psi_minus` would also be gauge invariant but would be an explicit dimension-three fermion mass term, so classical scale invariance forbids it at tree level. The proposed Yukawa structure is therefore consistent with the conformal setup.

### Fermion Degrees of Freedom and Mass Basis

After `Phi = chi / sqrt(2)` and `chi = v_D`, the two Weyl fields obtain equal Majorana masses:

```text
m_psi_plus = m_psi_minus = y_D v_D / sqrt(2)
```

The semianalytic backend may treat them as one degenerate fermion entry with `gf_psi = y_D / sqrt(2)` and total `dof = 4`. This is a bookkeeping compression, not a single Dirac mass eigenstate. Downstream reports should avoid calling this a Dirac fermion unless an additional field-basis choice and mass term structure are introduced.

### Coleman-Weinberg Consistency

The tree-level potential has no explicit scalar mass term:

```text
V0 = lambda_D chi**4 / 4
```

The quartic `lambda_D` is correctly dependent rather than scanned independently. The backend-compatible Coleman-Weinberg coefficient is

```text
beta_lambda = (1/(8*pi**2))*(3*(2*g_D)**4 - 4*(y_D/sqrt(2))**4)
```

The downstream scan must enforce `beta_lambda > 0`; equivalently, the vector contribution must dominate the fermion contribution. Perturbativity of `g_D` and `y_D` is also an assumption, not a numerical result from this critique.

### Field-Dependent Masses and Backend Mapping

The validated backend mass-over-vev mapping is:

```text
gb_X = 2*g_D
gf_psi = y_D/sqrt(2)
boson_dofs["X_mu"] = 3
fermion_dofs["psi_degenerate_majorana_pair"] = 4
```

The scalar radial mode is the Coleman-Weinberg pseudo-dilaton at the broken minimum:

```text
m_chi_squared = beta_lambda * v_D**2
```

It should not be double-counted as an independent bosonic Coleman-Weinberg driver in `backend/semianalytic_pipeline.py`, which already adds a subleading scalar placeholder internally.

### Thermal Masses

The proposer thermal masses are placeholders. They are analytic and parseable, but `backend/semianalytic_pipeline.py` does not consume explicit Debye masses; it consumes mass-over-vev couplings and degrees of freedom, then constructs the small-field/high-temperature polynomial coefficients internally. This is a warning rather than a blocker.

### Literature Benchmark Mapping

The librarian benchmark mappings are compatible as starting points, not as exact parameter translations. The closest sources use different charge normalizations, kinetic mixing, portals, or Yukawa assumptions. Downstream FOPT/PTA scans may use the quoted MeV-scale `v_D`, `g_D`, and `y_D` regions as priors or seeds only after applying the validated `m_X/v_D = 2*g_D` convention and enforcing `beta_lambda > 0`.

## Minimal Repairs Applied

1. Clarified that the two Weyl fermions become two degenerate Majorana fermions, represented in the backend as one `dof = 4` degenerate fermion entry.
2. Clarified the field-dependent vector mass convention as the backend mapping `m_X(chi) = gb_X * chi` with `gb_X = 2*g_D`.
3. Marked explicit thermal masses as placeholders because the selected semianalytic backend does not directly consume them.
4. Preserved `lambda_D` as a dependent Coleman-Weinberg quantity and made `beta_lambda > 0` an explicit downstream validity condition.

## Downstream Permission

Downstream `fopt-agent` and `pta-agent` work is allowed, with warnings. The FOPT scan must enforce the validated parameter basis and should not scan `lambda_D` independently.
