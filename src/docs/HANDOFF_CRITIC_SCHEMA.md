# Critic Handoff Schema

Write `output/<model-name>/handoff_critique.json`.

Canonical field names are `validation_*`. Legacy `valutation_*` keys are
deprecated. If a legacy handoff contains `valutation_*` keys, the orchestrator
or validation layer must normalize them immediately to the canonical
`validation_*` spelling before any downstream agent consumes the handoff.
Downstream agents must not depend on mixed `validation_*` and `valutation_*`
naming.

In addition to the common envelope fields defined in
[HANDOFF_SCHEMAS.md](HANDOFF_SCHEMAS.md) (`model`, `agent`, `run_status`,
provenance arrays), include the following agent-specific fields:

```json
{
  "model": "<model-name>",
  "agent": "critic-agent",
  "run_status": "ok | warning | failed | blocked",
  "validation_gauge_groups": [],
  "validation_global_symmetries": [],
  "validation_particle_content": [],
  "validation_lagrangian_terms": [],
  "validation_free_parameters": [],
  "parameter_basis": {
    "independent": {},
    "dependent": {},
    "fixed": {}
  },
  "validation_assumptions": [],
  "authoritative_model_file": "output/<model-name>/model.md",
  "repair_records": [],
  "red_flags": [],
  "warnings": []
}
```

For FOPT requests, also include:

```json
{
  "validation_ssb_pattern": [],
  "validation_vev_convention": [],
  "validation_tree_level_potential": [],
  "validation_field_dependent_masses": [],
  "validation_thermal_masses": [],
  "validation_backend_compatibility": []
}
```

Rules:

- Each item in a `validation_*` array must include `item`, `status`, and
  `notes`.
- Allowed item statuses are `ok`, `warning`, `fixed`, `red_flag`, and
  `blocked`.
- If a red flag is fixed, include `original`, `fix`, and `severity`.
- If the critic generates `model.md`, `authoritative_model_file` must identify
  it as the validated model for downstream stages.
- If the critic repairs a proposer-generated model, each repair must be recorded
  in `repair_records` with the original issue, applied fix, justification, and
  whether the fix was minimal.
- The critic must not return `ok` while unresolved red flags remain.
- The critic must check that dependent parameters have not been incorrectly
  classified as independent scan parameters.
- In Coleman-Weinberg models, CW-fixed quartics must be dependent parameters. In
  Higgs-like models, minimization-fixed `mu^2` parameters must be dependent
  parameters.