# PTA Handoff Schema

Write `output/<model-name>/handoff_pta.json`.

Required fields:
```json
{
  "model": "<model-name>",
  "agent": "pta-agent",
  "run_status": "ok | warning | failed | blocked",
  "created_at": "YYYY-MM-DD",
  "branch": "pta | ptarcade_campaign | other",
  "created_from": [],
  "commands": [],
  "files_read": [],
  "files_written": [],
  "warnings": [],
  "errors": [],
  "approximations": [],
  "analysis_mode": "benchmark_only | benchmark_plus_ptarcade | not_run",
  "pta_parameter_basis": {
    "independent": {},
    "dependent": {},
    "fixed": {}
  },
  "spectrum_template": "higgsless | sw | dbf | bf | bf_konstandin | other",
  "template_validity": {
    "status": "ok | warning | failed",
    "reason": ""
  },
  "benchmark_analysis": {
    "scan_summary": {
      "total_points": 0,
      "viable_points": 0,
      "boundary_expansions": []
    },
    "prior_ranges": {},
    "template_comparison": {},
    "best_fit_points": [
      {
        "rank": 1,
        "name": "",
        "parameters": {},
        "alpha": null,
        "beta_H": null,
        "T_star": null,
        "score": null,
        "inside_bins": null,
        "total_bins": null,
        "peak_frequency_Hz": null,
        "peak_h2OmegaGW": null,
        "spectrum": {
          "frequency_Hz": [],
          "h2OmegaGW": []
        },
        "spectrum_file_ref": {
          "file": "output/<model-name>/pta_benchmark_scan.csv",
          "spectrum_id": ""
        }
      }
    ]
  },
  "ptarcade_analysis": {
    "run_status": "ok | warning | failed | blocked | not_run",
    "campaign": {
      "pta_data": "",
      "mode": "",
      "out_dir": "",
      "config_file": "",
      "model_file": "",
      "plot_file": ""
    },
    "prior_parameter_basis": {
      "independent": {},
      "dependent": {},
      "fixed": {}
    },
    "priors": {},
    "chain_validation": {
      "chains_found": false,
      "finite_samples": false,
      "notes": ""
    },
    "bayes_estimates": {
      "bayes_est": {},
      "credible_regions": {
        "sigma_1": {
          "description": "68% credible region",
          "bounds": {}
        },
        "sigma_2": {
          "description": "95% credible region",
          "bounds": {}
        },
        "sigma_3": {
          "description": "99.7% credible region",
          "bounds": {}
        }
      },
      "evidence": null,
      "evidence_error": null
    },
    "map_estimates": {
      "map_est": {},
      "map_value": null
    }
  },
  "constraint_summary": []
}
```

Recommended provenance rules:

- `created_from` should list upstream FOPT handoffs and benchmark region definitions.
- `commands` should capture the PTA scan commands and PTArcade campaign invocation if present.
- `files_read` should include upstream FOPT JSON, model files, and PTA configuration.
- `files_written` should include the benchmark scan CSV, PDF plots, and PTArcade artifacts.
- `analysis_mode` must be `benchmark_plus_ptarcade`. `ptarcade_analysis` MUST be present and populated.
  If PTArcade could not be executed due to missing dependencies or blockers, set
  `ptarcade_analysis.run_status = "blocked"`, set the top-level `run_status` to
  `blocked` (or `failed` as appropriate), and explain the reason in `errors`.

Benchmark analysis structure:

- `best_fit_points` must be a list ordered by rank, with the top-scoring point at rank 1.
- All best-fit entries must use model parameters, not only derived FOPT parameters.
- `prior_ranges` must be on model parameters, not directly on `alpha`, `beta_H`, or temperature.
- `template_comparison` is optional but recommended; record the best score and validity for each template checked.
- Benchmark-only results must not use Bayesian terms such as posterior, MAP, evidence, or credible interval.

PTArcade analysis structure:

- `sigma_1`, `sigma_2`, `sigma_3` should be explicitly structured credible regions (68%, 95%, 99.7%).
- Each sigma region should include parameter bounds or full posterior samples if available.
- `bayes_est` and `map_est` must be on model parameters only, not on `alpha`, `beta_H`, or temperature.
- PTArcade priors must reference independent model parameters only; dependent parameters must appear in `prior_parameter_basis.dependent`.
- `chain_validation` must confirm that chains were found and contain finite samples before claiming Bayesian estimates are usable.

Rules:

- If no best-fit points exist, set `best_fit_points` to `[]` and explain in `warnings` or `errors`.
- If FOPT ran successfully but no viable FOPT points are available, PTA should
  use `run_status: "ok"` or `run_status: "warning"` with no PTA-compatible
  region, not `blocked`, provided the upstream FOPT handoff is valid.
- If plotting fails after numerical PTA outputs are generated, keep the PTA
  handoff usable and record the plotting failure in `warnings` or `errors`; do
  not mark the full PTA benchmark as failed solely because plotting failed.
- Do not call a point viable if the selected spectrum template is outside its
  validity domain.
- PTA benchmark scans and PTArcade priors must use only
  `pta_parameter_basis.independent`. Dependent parameters fixed by
  Coleman-Weinberg relations or minimization conditions must be computed inside
  the model implementation and may be reported as diagnostics, but must not be
  used as PTA scan axes or PTArcade priors (record them in
  `prior_parameter_basis.dependent`).
- PTArcade is mandatory for PTA handoffs. If the campaign cannot be run,
  represent this explicitly in `ptarcade_analysis.run_status` and `errors`; do not
  omit `ptarcade_analysis`.
- If the best benchmark point touches a scan boundary, record the expansion
  attempt in `scan_summary.boundary_expansions` before accepting the point.
- `pta_benchmark_scan.csv` and `handoff_pta.json` must use the
  same frequency grid, ordering, units, and spectrum column/key names. The
  best-fit spectra in JSON must map unambiguously to rows in `pta_benchmark_scan.csv`.
- Use `blocked` if dependencies or expected chain outputs are unavailable.
- Include enough file paths for the report agent to locate the generated model,
  config, chain, and plot artifacts.
