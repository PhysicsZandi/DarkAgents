# Proposer Handoff Schema (Model Specification)

Write either:

- `output/<model-name>/handoff_proposed_model.json` from `proposer-agent`.
- `output/<model-name>/handoff_model.json` from `critic-agent` after validation
  or deterministic fixes.

In addition to the common envelope fields defined in
[HANDOFF_SCHEMAS.md](HANDOFF_SCHEMAS.md) (`model`, `agent`, `run_status`,
provenance arrays), include the following agent-specific fields:

```json
{
  "model": "<model-name>",
  "agent": "proposer-agent | critic-agent",
  "run_status": "ok | warning | failed | blocked",
  "gauge_groups": [],
  "global_symmetries": [],
  "particle_content": [],
  "lagrangian_terms": [],
  "free_parameters": [],
  "parameter_basis": {
    "independent": {},
    "dependent": {},
    "fixed": {}
  },
  "assumptions": [],
  "backend_compatibility": []
}
```

For FOPT-capable models, also include:

```json
{
  "ssb_pattern": [],
  "vev_convention": [],
  "tree_level_potential": [],
  "field_dependent_masses": [],
  "thermal_masses": [],
  "expression_symbols": []
}
```

Rules:

- `particle_content` entries must include at least `name`, `type`, `spin`,
  gauge representations or charges, statistics, and degrees of freedom when
  known.
- `lagrangian_terms` entries must include a symbolic `expression` and enough
  notes to verify gauge invariance.
- `free_parameters` entries must include `name` and either `range`, `value`, or
  `determination`.
- `parameter_basis.independent` defines parameters that may be scanned or
  assigned PTArcade priors. `parameter_basis.dependent` defines parameters
  computed from model relations and must not be scanned or assigned priors.
  `parameter_basis.fixed` defines externally fixed constants or assumptions.
- For classically scale-invariant / Coleman-Weinberg models, the quartic coupling
  fixed by the Coleman-Weinberg minimization condition must appear under
  `parameter_basis.dependent`, not `parameter_basis.independent`.
- For Higgs-like potentials, the quadratic mass parameter `mu^2` must appear
  under `parameter_basis.dependent` when it is fixed by the minimization
  condition in terms of the vev and quartic coupling.
- `field_dependent_masses` entries must include `particle`, `m2_of_chi` or the
  relevant background-field expression, `dof`, `statistics`, and notes on the
  derivation.
- `tree_level_potential`, `field_dependent_masses`, `thermal_masses`, and
  dependent-parameter relations must use analytical Python/SymPy-compatible
  expression strings when consumed downstream. Do not use LaTeX-only expressions,
  implicit multiplication, Unicode Greek symbols, or prose expressions in
  machine-readable expression fields. For example use `3 * g2 * chi**2`, not
  `3g^2\chi^2`.
- Every symbol appearing in machine-readable expression strings must be declared
  in `expression_symbols`, `parameter_basis`, or the relevant background-field
  convention. Validation must fail if an expression is non-parseable or contains
  undeclared symbols.
- `backend_compatibility` should state whether `semianalytic_pipeline`, 
  or another backend can be used, and why.

Recommended structure for `backend_compatibility` items:

```json
{
  "backend": "semianalytic_pipeline |  other",
  "status": "compatible | compatible_with_warnings | incompatible",
  "mapping": {},
  "notes": ""
}
```
