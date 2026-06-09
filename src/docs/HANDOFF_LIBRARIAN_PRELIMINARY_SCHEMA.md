# Librarian Preliminary Handoff Schema

Write `output/<model-name>/handoff_librarian_preliminary.json`.

Required fields:

```json
{
  "model": "<model-name>",
  "agent": "preliminary-librarian-agent",
  "run_status": "ok | warning | failed | blocked",
  "scan_mode": "preliminary_scan",
  "papers": [],
  "searched_sources": [],
  "novelty_verdict": "",
  "novelty_notes": "",
  "benchmark_hints": {},
  "constraint_summary": [],
  "theory_uncertainties": [],
  "recommended_next_steps": []
}
```

Each `papers` item must include:

```json
{
  "arxiv_id": "",
  "title": "",
  "authors": [],
  "year": null,
  "journal": "",
  "relevance_score": null,
  "brief_description": "",
  "model_studied": "",
  "similarity_to_target": "",
  "paper_classification": "same_model | structurally_similar_model | same_target_signal_different_model | benchmark_only_relevance | background_context_only",
  "metadata_only": false,
  "experimental_constraints": [],
  "observables": [],
  "benchmark_points": [],
  "assumptions": [],
  "citation_verified": true
}
```

Rules:

- Preliminary scans may leave `constraint_summary` and `theory_uncertainties`
  empty because they focus on novelty and benchmark hints.
- Kept citations must be verified against the actual source metadata.
- Each kept paper must be structurally classified using `paper_classification`.
- Benchmark hints must label confidence as `direct`, `adaptable`,
  `qualitative`, or `unusable`, and must include any relevant convention notes.
- Metadata-only papers must not be used as sources for formulas, benchmark
  points, or exclusions.

Recommended structure for benchmark hints:

```json
{
  "benchmark_hints": [
    {
      "source": "",
      "parameters": {},
      "confidence": "direct | adaptable | qualitative | unusable",
      "conventions": {},
      "notes": ""
    }
  ]
}
```
