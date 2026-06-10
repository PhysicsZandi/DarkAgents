# Validated Model: u1conformal

Date: 2026-06-10  
Agent: critic-agent  
Branch: fopt-pta

## Model

The validated model is a classically scale-invariant dark Abelian Higgs sector with gauge group

```text
U(1)_D
```

and one complex scalar `Phi` of charge `q_Phi = 1`. The dark covariant derivative is

```text
D_mu = partial_mu - i * g_D * A'_mu
```

The dark-sector Lagrangian is

```text
L_D = |D_mu Phi|**2 - lambda_Phi * |Phi|**4 - (1/4) * F'_munu * F'**munu
```

The optional phenomenological interactions are

```text
lambda_HP * |H|**2 * |Phi|**2
(epsilon / 2) * F'_munu * F**munu
```

For the FOPT calculation these optional couplings are assumed small enough not to modify the effective potential.

## Background and Symmetry Breaking

The background convention is

```text
Phi = (chi + rho + i * G) / sqrt(2)
```

with `v = <chi>`. The symmetry-breaking pattern is

```text
U(1)_D -> nothing
```

The Goldstone `G` is eaten by the dark gauge boson.

## Potential and Coleman-Weinberg Relations

The tree-level potential along the background is

```text
V_tree(chi) = lambda_Phi * chi**4 / 4
```

The independent FOPT parameters are

```text
v
g_D
```

The CW-fixed quartic `lambda_Phi` is dependent and must not be scanned independently. In the minimal gauge-only model,

```text
beta_lambda = 3 * g_D**4 / (8 * pi**2)
m_rho**2 = beta_lambda * v**2
```

with `beta_lambda > 0` for `g_D > 0`.

## Field-Dependent Masses

Using the prompt convention and real-field mass-term normalization,

```text
m_Aprime**2(chi) = g_D**2 * chi**2
```

The tree-level scalar curvature masses along the same background are

```text
m_rho,tree**2(chi) = 3 * lambda_Phi * chi**2
m_G,tree**2(chi) = lambda_Phi * chi**2
```

The physical radial mass at the CW minimum is

```text
m_rho**2 = beta_lambda * v**2
```

## Backend Mapping

For `backend/semianalytic_pipeline.py`, use

```text
chi0 = v
boson_gbs = {"Aprime": g_D}
boson_dofs = {"Aprime": 3}
fermion_gfs = {}
fermion_dofs = {}
```

Do not pass `lambda_Phi`, `rho`, or `G` as independent scan inputs. The semi-analytic backend computes the CW-fixed scalar contribution internally at subleading order.

## Caveats

The model is validated with warnings:

- full Daisy-resummed thermal masses are not specified in the prompt and would be required for a full finite-temperature effective-potential implementation;
- `lambda_HP` and `epsilon` are unspecified and must be supplied later for quantitative constraints;
- benchmarks using `m_ZD = 2 * g_D * M` conventions require translation before comparison;
- gauge dependence and supercooling/percolation reliability must be tracked in downstream FOPT/PTA analysis.
