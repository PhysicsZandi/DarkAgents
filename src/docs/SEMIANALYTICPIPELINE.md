# SemiAnalyticPipeline

This class only works for classically scale-invariant models with a single scalar field. It exploits the fact that in such models, masses of all particles are proportional to the vev of the scalar field, so a high-temperature expansion of the effective potential leads to a polynomial in the scalar field, with temperature-dependent coefficients. This allows analytical expressions for the bounce action, nucleation temperature and percolation temperature. The percolation temperature is computed by approximating the false vacuum decay rate as a Gaussian function and integrating it analytically. All you need are the value of the vev, the masses of the particles, and their degrees of freedom. In particular, it takes as input the masses over the vev defined by 
- gb_gauge = mgauge / vev for gauge bosons
- gb_fermion = mfermion / vev for fermions

Furthermore, the lambda quartic coupling of the scalar field is computed by the code with the requirement that the effective potential has a minimum at the vev. This means that the user does not need to specify the value of lambda, but only the masses of the particles and their degrees of freedom. In practice, the contribution of scalar and Goldstone bosons is negligible, so you can only consider the gauge bosons and the fermions, which are the ones that give the dominant contribution to the effective potential. 

The CW-fixed scalar quartic must be treated as a dependent parameter in all handoff JSONs. It must not be scanned independently and must not appear under `parameter_basis.independent`.

The current implementation works with a renormalisation scale equal to the vev, and does not include RG running or Daisy resummation. For more details on the implementation and the underlying assumptions, see arXiv:2602.02829 (Pascoli, Rosauro-Alcaraz, Zandi).

This code has been tested against the full numerical calculation of the effective potential and bounce action, and it reproduces the results with high accuracy, while being much faster to evaluate. This makes it a useful tool for scanning large parameter spaces of classically scale-invariant models and identifying viable points for gravitational wave production.

## Model skeleton

To define a model, instantiate `SemiAnalyticPipeline` with the vev, mass-over-vev ratios, and degrees of freedom:
```python
from semianalytic_pipeline import SemiAnalyticPipeline

vev = VEV_VALUE

# for bosons
g = GAUGE_COUPLING_VALUE
mgauge = GAUGE_BOSON_MASS_VALUE
gb_gauge = mgauge / vev

# for fermions
y = YUKAWA_COUPLING_VALUE
mfermion = FERMION_MASS_VALUE
gb_fermion = mfermion / vev


boson_gbs = {
    "name_gauge": gb_gauge,
}
boson_dofs = {
    "name_gauge": DOFS_GAUGE,
}
fermion_gfs = {
    "name_fermion": gb_fermion,
}
fermion_dofs = {
    "name_fermion": DOFS_FERMION,
}

model = SemiAnalyticPipeline(
    chi0=vev,
    boson_gbs=boson_gbs,
    boson_dofs=boson_dofs,
    fermion_gfs=fermion_gfs,
    fermion_dofs=fermion_dofs,
    verbose=False,
)
```

The code computes automatically the CW-fixed quartic coupling and the mass of the scalar field, which are not independent parameters but are fixed by the gauge and fermion content of the model. Do not include the scalar field in the input, the code will automatically compute its contribution.


## Methods

```python
Tnucl = model.get_Tn()
Tperc = model.get_Tp()
alpha = model.get_alpha()
beta_H = model.get_beta_H()
Treh = model.get_Tr()
eternal_inflation = model.get_check_eternal_inflation()
```
Pay attention that the method `get_check_eternal_inflation` returns `True` if eternal inflation is present, and `False` if it is not. Eternal inflation occurs when the false vacuum decay rate is smaller than the Hubble rate, which means that the phase transition never completes and the universe keeps inflating forever. This is a failure mode for gravitational wave production, and points that suffer from eternal inflation should not be reported as viable, even if they have finite and positive values for the other observables.

Pay also attention that the vev must be given in GeV to the code. 

## Validation and output conventions

Generated model code should keep all model-specific logic in `output/<model-name>/fopt_model.py` and scan code in `output/<model-name>/fopt_model_scan.py`. The scan should write `output/<model-name>/fopt_benchmarks.csv`, `output/<model-name>/fopt_report.md`, and `output/<model-name>/handoff_fopt.json`.

A viable point must have finite positive values for the relevant transition observables, especially `alpha`, `beta_H`, `Tp`, `T`. Failed numerical points must be recorded separately and must not be reported as viable.

Check also that eternal inflation is avoided, i.e. that the false vacuum decay rate is always larger than the Hubble rate. If eternal inflation occurs, report it as a failure mode and do not report the point as viable, even if the other observables are finite and positive.

## Generated Scan Requirements

Generated scan code must wrap each backend evaluation in per-point error handling and a per-point timeout. Backend exceptions, non-convergence, timeouts and non-finite intermediate outputs must be recorded as `numerical_failure`, not silently discarded.

The independent parameter columns in `fopt_benchmarks.csv` must exactly match the key strings in `parameter_basis.independent`. Status labels and units must match those used in `handoff_fopt.json`.

If the backend runs successfully but no viable FOPT point is found, the handoff should use `run_status: "ok"` or `run_status: "warning"` with an empty viable-point list, not `blocked` or `failed`.
