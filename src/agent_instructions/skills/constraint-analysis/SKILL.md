---
name: constraint-analysis
description: Search the literature for constraints applicable to BSM particles in the PTA-preferred region, classify their applicability, and identify missing observables or backend calculations.
---

# Constraint Analysis Skill

## Overview

Use this skill to explicitly search the literature for constraints relevant to the new particles in the preferred pipelines parameter space region.

Common contrained quantities include masses, couplings, decay channels, production modes, lifetimes and thermal-history assumptions in the pipeline preferred region. Common constraint categories include collider constraints, beam-dump and fixed-target constraints, flavor constraints, direct-detection constraints, indirect-detection constraints, stellar-cooling constraints, supernova constraints, CMB constraints, BBN constraints, dark-radiation constraints, structure-formation constraints, thermalization constraints and theory constraints. Common missing calculations include mediator decay widths and lifetimes, scalar decay widths and lifetimes, branching ratios, thermalization rate versus Hubble rate, decoupling temperature, BBN lifetime and abundance test, CMB energy-injection rate, annihilation cross section, self-interaction cross section, direct-detection scattering cross section, Higgs exotic or invisible branching ratio, dark photon visible or invisible decay rates, kinetic-mixing production rates, stellar energy-loss rate, supernova trapping or free-streaming regime, relic abundance or freeze-in yield, dark-sector temperature ratio and `N_eff`. 

## Task Workflow

1. Extract from all the upstream handoff JSONs the relevant particles and the parameter space region. Include masses and all relevant information about the particles. 

For the `fopt-pta` branch:
- If PTArcade was run, use the 1 sigma posterior region of the model parameters. 
- If only benchmark PTA exists, use the best benchmark point and the local benchmark scan region.

2. Make an exhaustive list of all possible constraints that could apply to these particles. 
3. Build targeted `WebSearch` queries for each particle and coupling. Pay attention to the specific mass range, coupling range, decay channels, production modes, lifetimes and thermal-history assumptions. After the search, use `WebFetch` to read the most relevant sources before including them in the report.
4. For each relevant paper or experimental result, extract the constrained observable, constrained mass range, constrained coupling or mixing range, units, coupling conventions, assumptions, decay channels, production mode, lifetime regime if relevant and whether the bound is direct, approximate, recast-needed or not applicable. Do not compare or apply bounds unless units and normalization conventions are matched or the conversion is explicit.
5. Keep only constraints that overlap the pipeline-preferred region. For every constraint, record the tested subregion and do not state that the full region is excluded unless the bound applies to the full region. For each candidate constraint, identify the required model-specific observable and check whether it is already available from the upstream handoff JSONs or existing backend code. If not, suggest what is the required physical quantity to compute.
6. Classify each constraint by applicability and missing computations. Build a constraint table with the entries present in the `constraints` part in the `docs/HANDOFF_CONSTRAINTS_SCHEMA.md` template.

## Rules

- Prefer high-level community summaries, PDG reviews, Cosmic Vision reports, official experimental results, experimental-combination papers, review papers and recent specialized compilation preprints when available. Fetch large individual papers only when they are needed for a specific limit, assumption, mass range, decay mode or likelihood detail.
- Do not claim that a parameter point is excluded unless the required observable has been computed or directly mapped to a published bound. Do not apply a bound outside its stated mass, coupling, lifetime, branching-ratio or decay-channel regime. Do not apply collider, beam-dump or direct-detection constraints from mass alone, because production and decay assumptions matter. Do not apply cosmological constraints from lifetime alone, because abundance, temperature ratio and branching fractions may matter.
- Prefer high-level community summaries, PDG reviews, Cosmic Vision reports, official experimental results, experimental-combination papers, review papers and recent specialized compilation preprints when available. Do not fetch large individual papers.
- If only abstract or metadata are accessible, do not infer quantitative conclusions.
- For every constraint, pay attention to conventions, such as units and couplings. Do not compare or apply bounds unless units and normalization conventions are matched or the conversion is explicit. When a constraint applies to only part of the PTA-preferred region, record the affected subregion and do not state that the full region is excluded.
- Do not edit upstream files. Only write `constraints_report.md`, `constraints_table.csv` and `handoff_constraints.json` inside `output/<model-name>/`.
