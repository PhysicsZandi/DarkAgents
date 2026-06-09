## Constraint Handoff

Write `output/<model-name>/handoff_constraints.json`.

Required fields:

```json
{
  "model": "<model-name>",
  "agent": "constraint-agent",
  "run_status": "ok | warning | failed | blocked",
  "created_at": "YYYY-MM-DD",
  "branch": "constraints | other",
  "created_from": [],
  "commands": [],
  "files_read": [],
  "files_written": [],
  "warnings": [],
  "errors": [],
  "approximations": [],
  "analysis_mode": "ptarcade_1sigma | benchmark_region | benchmark_point | unavailable",
  "input_region": {
    "source": "ptarcade_1sigma | benchmark_region | benchmark_point | unavailable",
    "parameters": {},
    "derived_masses": {},
    "notes": []
  },
  "constraint_summary": {
    "total_constraints_considered": 0,
    "directly_testable": 0,
    "approximately_testable": 0,
    "requires_recast": 0,
    "requires_new_backend": 0,
    "not_applicable": 0
  },
  "constraints": [],
  "missing_calculations": []
}
```

Recommended provenance rules:

- `analysis_mode` should match `input_region.source` unless multiple sources are mixed and explained in `input_region.notes`.
- `created_from` should name the upstream handoffs or benchmark files used to define the audited region.
- `commands` should capture the actual search, fetch, and validation commands used to build the handoff.
- `files_read` should include upstream JSON files and any literature sources that directly informed the constraint classification.
- `files_written` should include every artifact produced by the agent.

Each item in `constraints` should include:

```json
{
  "id": "",
  "name": "",
  "category": "collider | beam_dump | fixed_target | flavor | direct_detection | indirect_detection | stellar | supernova | CMB | BBN | Neff | structure_formation | thermalization | theory | other",
  "description": "",
  "applicability_class": "direct | approximate | recast_needed | requires_new_backend | not_applicable",
  "constraint_applied": false,
  "affected_particles": [],
  "mass_range": {},
  "coupling_range": {},
  "observable": "",
  "required_inputs": [],
  "required_observables": [],
  "available_observables": [],
  "missing_observables": [],
  "units": {},
  "conventions": {},
  "applicability": "",
  "tested_subregion": {},
  "applicability_notes": [],
  "source": {
    "title": "",
    "arxiv_id": "",
    "authors": "",
    "citation_verified": false
  }
}
```

Each item in `missing_calculations` should include:

```json
{
  "observable": "",
  "needed_for_constraints": [],
  "required_inputs": [],
  "suggested_backend_module": "",
  "validation_checks": [],
  "priority": "high | medium | low"
}
```

Recommended validation rules:

- `constraint_applied` should be `true` only when the preferred region is directly mapped to a published bound or a trustworthy recast.
- `applicability_class` should distinguish between direct results, approximate results, recast-needed limits, missing backend calculations, and genuinely non-applicable constraints.
- `tested_subregion` should record the specific mass, coupling, lifetime, branching-ratio, or temperature slice that overlaps the preferred region.
- `missing_calculations` should only list observables that are not already present in the upstream handoffs or backend outputs and are required to test at least one constraint.