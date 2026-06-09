# Handoff Schemas

This is the index for the per-agent handoff contracts. Each agent writes a
canonical `handoff_*.json` plus human-readable reports; the detailed field
contract for each JSON lives in the linked schema document.

## Pipeline order

`proposer-agent` → `preliminary-librarian-agent` → `critic-agent` → `fopt-agent` → `pta-agent` → `constraint-agent` → `prior-agent` → `report-agent`.

## Agent outputs and schema docs

| Agent | Schema doc | Canonical JSON / report outputs |
| --- | --- | --- |
| `proposer-agent` | [HANDOFF_PROPOSER_SCHEMA.md](HANDOFF_PROPOSER_SCHEMA.md) | `output/<model-name>/proposed_model.md`, `output/<model-name>/handoff_proposed_model.json` |
| `critic-agent` | [HANDOFF_CRITIC_SCHEMA.md](HANDOFF_CRITIC_SCHEMA.md) | `output/<model-name>/critique.md`, `output/<model-name>/model.md`, `output/<model-name>/handoff_critique.json`, `output/<model-name>/handoff_model.json` |
| `preliminary-librarian-agent` | [HANDOFF_LIBRARIAN_PRELIMINARY_SCHEMA.md](HANDOFF_LIBRARIAN_PRELIMINARY_SCHEMA.md) | `output/<model-name>/librarian_preliminary_report.md`, `output/<model-name>/handoff_librarian_preliminary.json` |
| `fopt-agent` | [HANDOFF_FOPT_SCHEMA.md](HANDOFF_FOPT_SCHEMA.md) | `output/<model-name>/fopt_model.py`, `output/<model-name>/fopt_model_scan.py`, `output/<model-name>/fopt_benchmarks.csv`, `output/<model-name>/fopt_report.md`, `output/<model-name>/handoff_fopt.json`, `output/<model-name>/fopt_results.json` |
| `pta-agent` | [HANDOFF_PTA_SCHEMA.md](HANDOFF_PTA_SCHEMA.md) | `output/<model-name>/pta_benchmark_scan.csv`, `output/<model-name>/pta_benchmark_spectrum.pdf`, `output/<model-name>/pta_posteriors.pdf`, `output/<model-name>/pta_ptarcade_spectrum.pdf`, `output/<model-name>/ptarcade_bayes.json`, `output/<model-name>/pta_report.md`, `output/<model-name>/handoff_pta.json` |
| `constraint-agent` | [HANDOFF_CONSTRAINTS_SCHEMA.md](HANDOFF_CONSTRAINTS_SCHEMA.md) | `output/<model-name>/constraints_report.md`, `output/<model-name>/constraints_table.csv`, `output/<model-name>/handoff_constraints.json` |
| `prior-agent` | [HANDOFF_PRIOR_AUDIT_SCHEMA.md](HANDOFF_PRIOR_AUDIT_SCHEMA.md) | `output/<model-name>/prior_audit_report.md`, `output/<model-name>/prior_audit_table.csv`, `output/<model-name>/handoff_prior_audit.json` |
| `report-agent` | [HANDOFF_REPORT_SCHEMA.md](HANDOFF_REPORT_SCHEMA.md) | `output/<model-name>/final_report.tex`, `output/<model-name>/handoff_report.json` |

## Common envelope fields

Unless a schema explicitly states otherwise, every `handoff_*.json` shares the
following envelope. Per-agent schema docs list only the fields that are specific
to that agent and do not repeat these.

```json
{
  "model": "<model-name>",
  "agent": "<agent-name>",
  "run_status": "ok | warning | failed | blocked",
  "created_at": "YYYY-MM-DD",
  "branch": "<branch> | other",
  "created_from": [],
  "commands": [],
  "files_read": [],
  "files_written": [],
  "warnings": [],
  "errors": [],
  "approximations": []
}
```

The `agent` value must match the agent's canonical name exactly (e.g.
`preliminary-librarian-agent`, not `librarian-agent`).

Common `run_status` convention across all agents:

- `ok` / `warning` — the agent ran and produced a usable (possibly empty) result.
- `failed` — the agent ran but produced no trustworthy result.
- `blocked` — required upstream inputs or dependencies were missing.
