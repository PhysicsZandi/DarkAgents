# FOPT Handoff Schema

Write `output/<model-name>/handoff_fopt.json`. If detailed scan output is also
written, mirror the same data in `output/<model-name>/fopt_results.json`. The
single schema below is the canonical contract for both artifacts.

```json
{
    "model": "<model-name>",
    "agent": "fopt-agent",
    "run_status": "ok | warning | failed | blocked",
    "created_at": "YYYY-MM-DD",
    "branch": "fopt | other",
    "created_from": [],
    "commands": [],
    "files_read": [],
    "files_written": [],
    "warnings": [],
    "errors": [],
    "approximations": [],
    "backend_choice": {
      "selected_backend": "semianalytic_pipeline | other | null",
      "executed": false,
      "reason": ""
    },
    "backend": "semianalytic_pipeline | other",
    "backend_executed": false,
    "expected_upstream_inputs": [],
    "missing_upstream_inputs": [],
    "model_parameter_ranges": {},
    "parameter_basis": {
      "independent": {},
      "dependent": {},
      "fixed": {}
    },
    "temperature_key": "Treh | T_star | Tp | Tn",
    "scan_status_labels": ["viable", "physical_failure", "numerical_failure", "not_fopt"],
    "benchmark_summary": {
      "total_points": 0,
      "viable_points": 0,
      "failed_points": 0,
      "excluded_points": 0
    },
    "scan_summary": {
      "total_points": 0,
      "viable_points": 0,
      "failed_points": 0,
      "excluded_points": 0
    },
    "csv_json_alignment": {
      "csv_file": "output/<model-name>/fopt_benchmarks.csv",
      "independent_parameter_columns": [],
      "required_result_columns": [],
      "status_column": "status"
    },
    "model_parameters": [],
    "benchmarks": [],
    "best_points": [],
    "prior_ranges": {},
    "validation": {
      "finite_values": true,
      "percolation_checked": true,
      "eternal_inflation_checked": true,
      "perturbativity_checked": false
    },
    "output_files": []
}
```

Each `benchmarks` item must include:

  ```json
  {
    "name": "",
    "parameters": {},
    "alpha": null,
    "beta_H": null,
    "Tn": null,
    "Tp": null,
    "Treh": null,
    "f_peak_est": null,
    "_comment_f_peak_est": "template-independent, order-of-magnitude redshifted peak frequency in Hz; anchors the vev/temperature scale for the PTA agent and must not be treated as the true spectral peak",
    "status": "viable | failed | excluded | warning",
    "failure_reason": ""
  }
  ```

Rules:

- Use `blocked` when required upstream files are missing.
- Use `failed` when the backend was attempted and no trustworthy FOPT result was produced.
- If the backend runs successfully but no viable FOPT point is found, use `run_status: "ok"` or `"warning"` with `best_points: []`, not `blocked` or `failed`.
- Do not report failed numerical points as viable.
- `parameter_basis.independent` defines the FOPT scan axes.
- `parameter_basis.dependent` records internally computed quantities such as CW-fixed quartics or minimization-fixed `mu^2`.
- Scan and sample only independent model parameters. Dependent parameters fixed by Coleman-Weinberg relations or minimization conditions must be computed internally and reported as diagnostics, but must not be used as scan axes.
- Each row in `fopt_benchmarks.csv` must include a status compatible with `scan_status_labels`.
- The independent parameter columns in `fopt_benchmarks.csv` must exactly match the key strings in `parameter_basis.independent`; record them in `csv_json_alignment.independent_parameter_columns`.
- `fopt_benchmarks.csv`, `handoff_fopt.json`, and any detailed FOPT result JSON must use identical parameter names, units, and status labels.
- If no viable points are found, `best_points` must be an empty array and `warnings` or `errors` must summarize the diagnostics.
- `output_files` should include `fopt_model.py`, `fopt_model_scan.py`, `fopt_benchmarks.csv`, `fopt_report.md`, `handoff_fopt.json`, and any detailed result JSON that was written.
- If `status` is not `viable`, explain why in `failure_reason`.
- If `backend_executed` is false, `benchmarks` must be empty and `errors` must say why no backend run occurred.
- Use the temperature name actually consumed by PTA in `temperature_key`.
- `f_peak_est` is the template-independent, order-of-magnitude redshifted peak frequency in Hz; it anchors the vev/temperature scale for the PTA agent and must not be treated as the true spectral peak.
- `parameter_basis.independent` must match the independent scan axes used in the FOPT scan.
- Dependent parameters such as CW-fixed quartics or minimization-fixed `mu^2` may be included in benchmark diagnostics, but they must not be listed as independent model parameters.
