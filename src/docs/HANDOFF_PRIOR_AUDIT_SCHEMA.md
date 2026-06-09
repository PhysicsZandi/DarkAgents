# Prior Audit Handoff Schema

Write `output/<model-name>/handoff_prior_audit.json`.

Required fields:

```json
{
  "model": "<model-name>",
  "agent": "prior-agent",
  "run_status": "ok | warning | failed | blocked",
  "created_at": "YYYY-MM-DD",
  "branch": "prior_audit | other",
  "created_from": [],
  "commands": [],
  "files_read": [],
  "files_written": [],
  "warnings": [],
  "errors": [],
  "approximations": [],
  "uncertainty_summary": {
    "total_items": 0,
    "severity_distribution": {
      "1": 0,
      "2": 0,
      "3": 0,
      "4": 0,
      "5": 0,
      "6": 0,
      "7": 0,
      "8": 0,
      "9": 0,
      "10": 0
    },
    "controlled_distribution": {
      "1": 0,
      "2": 0,
      "3": 0,
      "4": 0,
      "5": 0,
      "6": 0,
      "7": 0,
      "8": 0,
      "9": 0,
      "10": 0
    }
  },
  "upstream_statuses": [],
  "assumptions": [],
  "required_followups": []
}
```

Recommended provenance rules:

- `created_from` should list the upstream handoffs, reports, and benchmark files that were actually inspected.
- `files_read` should include upstream JSONs and any Markdown report that supplied caveats not serialized in JSON.
- `upstream_statuses` should summarize each inspected handoff as `ok`, `warning`, `failed`, `blocked`, `missing`, or `not_applicable`.
- `files_written` should include every artifact produced by the agent.

Each item in `assumptions` should include:

```json
{
  "id": "",
  "kind": "assumption | prior | approximation | uncertainty | caveat | limitation | warning",
  "category": "",
  "description": "",
  "severity": 1,
  "controlled": false,
  "affected_outputs": [],
  "required_solution": "",
  "source": {
    "file": "",
    "section": "",
    "note": ""
  }
}
```

Each item in `required_followups` should include:

```json
{
  "id": "",
  "priority": "high | medium | low",
  "description": "",
  "blocked_by": [],
  "suggested_action": ""
}
```

Recommended validation rules:

- `severity` should be a numeric scale from 1 to 10, where 10 is the most serious uncontrolled issue.
- `controlled` should be a boolean, not a free-text label.
- `kind` should distinguish model assumptions from downstream approximations, uncertainties, caveats, and warnings.
- `required_followups` should only contain unresolved items that would materially reduce uncertainty or unblock a downstream interpretation.