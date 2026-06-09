# PTA Analysis Summary: SU2_conformal Model

## Completed Tasks

### ✅ 1. Template Selection
- **Selected:** `dbf` (dissipative bulk flow) template from arXiv:2511.15687
- **Rationale:** SU2_conformal produces α >> 0.5 (up to 10^16), making higgsless template invalid
- **Validation:** dbf template is validated for strongly supercooled FOPT with large α

### ✅ 2. Implemented pta_spectrum.py
- Location: `output/SU2_conformal/pta_spectrum.py`
- Features:
  - Computes GW spectrum for SU2_conformal model
  - Uses dbf template from backend/spectrum.py
  - Handles FOPT parameter computation via semianalytic_pipeline
  - Validates inputs and handles edge cases

### ✅ 3. Benchmark Scan Against PTA Violins
- **Input:** 50 viable points from fopt_benchmarks.csv
- **Output:** pta_benchmark_scan.csv, pta_benchmark_scan.json
- **Results:** Identified top 10 best-fit points
- **Scoring:** Combined frequency match + amplitude match

**Top 3 Points:**
| Rank | g_D | v (GeV) | α | β_H | T* (GeV) | Score |
|------|-----|---------|----|------|-----------|-------|
| 1 | 1.0632 | 0.0428 | 2.22×10⁶ | 32.43 | 0.0042 | 0.99998 |
| 2 | 1.1683 | 0.0428 | 7.08×10³ | 47.23 | 0.0042 | 0.99992 |
| 3 | 0.9675 | 0.0428 | 8.49×10⁹ | 21.78 | 0.0039 | 0.99991 |

**Observation:** All spectra peak at lowest PTA frequency bin, suggesting true peak is below PTA range.

### ✅ 4. PTArcade Campaign Setup
Created all required files for PTArcade inference with N_samples = 100,000:

- **ptarcade_model.py:** Model definition with log10 priors on (g_D, v)
  - Prior ranges: g_D ∈ [0.5, 3.0], v ∈ [0.01, 10.0] GeV (log-uniform)
  - Uses dbf template, dynamically selects based on α
  - Full error handling and validation

- **ptarcade_config.py:** Configuration file
  - PTA data: NG15
  - Mode: ceffyl
  - N_samples: 100,000
  - Output: output/SU2_conformal/chains

- **ptarcade_plot.py:** Posterior plotting script
  - Generates posterior plots and saves Bayesian estimates
  - Outputs: ptarcade_bayes.json, ptarcade_summary.txt

### ✅ 5. Handoff Documentation
- **handoff_pta.json:** Complete PTA handoff following HANDOFF_PTA_SCHEMA.md
- **pta_report.md:** Detailed PTA agent report
- **pta_benchmark_scan.json:** Benchmark results in JSON format

## Files Created/Modified

```
output/SU2_conformal/
├── pta_spectrum.py              # ✅ Spectrum computation
├── pta_benchmark_scan.py        # ✅ Benchmark scan script
├── pta_benchmark_scan.csv       # ✅ Benchmark results (50 points)
├── pta_benchmark_scan.json      # ✅ Benchmark results JSON
├── ptarcade_model.py            # ✅ PTArcade model
├── ptarcade_config.py           # ✅ PTArcade config
├── ptarcade_plot.py             # ✅ PTArcade plotting
├── handoff_pta.json             # ✅ PTA handoff
├── pta_report.md                # ✅ PTA report
└── chains/                      # 📂 Directory for PTArcade output
```

## Next Step: Run PTArcade

To complete the PTArcade campaign:

```bash
cd /Users/mattezandi/Desktop/code/DarkAgents/vibe_workspace

# Activate ptarcade environment
conda activate ptarcade

# Run PTArcade (N_samples = 100,000)
ptarcade -m output/SU2_conformal/ptarcade_model.py \
         -c output/SU2_conformal/ptarcade_config.py

# After completion (~1-2 hours), generate plots
python output/SU2_conformal/ptarcade_plot.py

# This will create:
# - output/SU2_conformal/chains/ (MCMC chains)
# - output/SU2_conformal/ptarcade_bayes.json (Bayesian estimates)
# - output/SU2_conformal/ptarcade_summary.txt (text summary)
# - output/SU2_conformal/SU2_conformal_posteriors.pdf (posterior plots)
```

## Key Findings

1. **Template:** dbf (dissipative bulk flow) is the correct choice for SU2_conformal
2. **Parameter Space:** v ≈ 0.0428 GeV, g_D ≈ 0.97-1.17 produces best PTA matches
3. **Alpha Values:** Extremely large (10^6 - 10^16) due to Coleman-Weinberg mechanism
4. **GW Amplitude:** h²Ω_GW ~ 10⁻¹⁰ - 10⁻⁹ in PTA range (within violin bounds)
5. **Frequency:** Spectra peak at or below lowest PTA frequency bin

## References

- **dbf Template:** arXiv:2511.15687 (Lewicki & Vaskonen, 2025) - Impact of cosmic expansion on GW spectra from strongly supercooled FOPT
- **higgsless Template:** arXiv:2209.04369 (Jinno et al., 2022) - Higgsless simulations of cosmological phase transitions
- **Model:** 2109.11558, 2210.07075
- **Backend:** arXiv:2602.02829

## Notes

- The FOPT scan used v ∈ [0.01, 10] GeV (instead of [100, 1e6] GeV) to obtain signals in PTA band
- All spectra peak at the lowest PTA frequency bin, suggesting the true GW peak may be at lower frequencies
- The dbf template properly handles the strong supercooling regime of SU2_conformal
- PTArcade configuration uses conservative defaults and N_samples = 100,000 as requested

---

*Last updated: 2026-06-07*
