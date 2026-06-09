# Final Report Handoff Schema

Write `output/<model-name>/handoff_report.json` from `report-agent`.

Required fields:

```json
{
  "model": "<model-name>",
  "agent": "report-agent",
  "run_status": "ok | warning | failed | blocked",
  "created_at": "YYYY-MM-DD",
  "branch": "report | other",
  "created_from": [],
  "commands": [],
  "files_read": [],
  "files_written": [],
  "warnings": [],
  "errors": [],
  "approximations": [],
  "included_sections": [],
  "figures_included": [],
  "tables_included": [],
  "cited_sources": [],
  "compiled_pdf": false,
  "compile_errors": []
}
```

Recommended provenance rules:

- `created_from` should list the upstream handoffs and reports that were actually used in the final report.
- `commands` should capture the LaTeX compile or validation commands used to produce the report artifacts.
- `files_read` should include the upstream JSON handoffs, the LaTeX sources, and any auxiliary files that were needed to write the report.
- `files_written` should include the `.tex`, `.pdf` if present, and any compile error log or generated artifacts.
- `warnings`, `errors`, and `approximations` should carry any nonfatal caveats that matter for interpretation.

Each item in `included_sections` should include:

```json
{
  "name": "",
  "status": "included | partial | omitted",
  "source": "",
  "notes": []
}
```

Each item in `figures_included` should include:

```json
{
  "label": "",
  "file": "",
  "caption": "",
  "source": "",
  "notes": []
}
```

Each item in `tables_included` should include:

```json
{
  "label": "",
  "file": "",
  "caption": "",
  "source": "",
  "notes": []
}
```

Each item in `cited_sources` should include:

```json
{
  "title": "",
  "arxiv_id": "",
  "source_file": "",
  "source_type": "handoff_json | report_md | paper | other",
  "citation_verified": false
}
```

Recommended validation rules:

- `compiled_pdf` should be `true` only when the PDF was actually produced and is readable.
- `compile_errors` should be empty unless the LaTeX build failed or produced warnings that materially affect the output.
- `cited_sources` should prefer upstream handoff JSONs over duplicated narrative summaries when both exist.
- `included_sections`, `figures_included`, and `tables_included` should reflect the actual final report content, not the intended outline.
