---
name: fopt-implementation
description: Convert a model undergoing a cosmological first-order phase transition into a working code implementation able to compute the necessary parameters. 
---

# FOPT Implementation Skill

## Overview

This skill is used by the `fopt-agent` to convert a proposed model undergoing a first-order phase transition into a code implementation able to compute the necessary first-order phase transition parameters.

## Task Workflow

1. Write the model implementation in `output/<model-name>/fopt_model.py`. The code must compute the first-order phase transition parameters (strength, characteristic timescale, transition temperature) from the model independent parameters (vev, couplings, masses) using the backend selected from `docs/BACKEND_COMPATIBILITY.md`. Compute dependent parameters from their defining relations at each point. Use validated analytical expressions for field-dependent masses, thermal masses, potentials and dependent parameters when provided. Add a simple smoke-test function at the end and run it on one benchmark point to verify that the implementation executes and returns finite, physically interpretable outputs.
2. Write the scan code in `output/<model-name>/fopt_model_scan.py`. Scan only the model independent parameters, starting from literature or model benchmarks in `output/<model-name>/librarian_preliminary_report.md` and `output/<model-name>/model.md`. Use a bounded coarse-to-fine strategy: first test a modest broad grid to locate viable regions, then refine only around successful or near-successful points. You should be able to find a region where the model produces a first-order phase transition, compute the relevant parameters, and prefer points whose estimated redshifted peak frequency falls in the PTA band. Test at least 100 points when computationally feasible. Save all scan results in `output/<model-name>/fopt_benchmarks.csv`, and mirror the structured per-point and best-point results in `output/<model-name>/fopt_results.json` as required by `docs/HANDOFF_FOPT_SCHEMA.md`. If the first scan finds no viable first-order phase transition, or no viable point lands in the PTA band, enlarge the scan ranges and increase the number of points, then rerun. The two cases call for different enlargements: extend towards lower scales (scanning logarithmically) when viable points exist but their estimated peak is above the PTA band, and broaden or densify the grid in all independent directions when no viable transition is found at all. Repeat this enlarge-and-rerun loop a few times, and only report that no FOPT or PTA-compatible region exists if it still fails once the scan is broad enough that the physical bounds, not the grid, are the limiting factor.

## Rules

- Choose logarithmic steps if the parameters span several orders of magnitude. Choose linear steps if the parameters span a small range. DO NOT choose exponential steps.
- Explore all independent free-parameter directions, including vevs and couplings. Do not scan dependent parameters. Do not fixed parameters. 
- Enforce physical scan bounds before calling the backend, including positive quantities or perturbative couplings.
- A viable point must have finite outputs, positive physical temperatures, finite positive strength, characteristic timescale, transition temperature.
- Do not invent FOPT observables, viable points, scan ranges, backend outputs, or benchmark values. Every reported number must come from executed code.
- Do not treat an empty or boundary-touching scan as a final result, enlarge the scan ranges and increase the number of points and rerun first.
- Do not edit upstream files or modify `backend` files. Only write code fiels and outputs inside `output/<model-name>/`.

For the `fopt-pta` branch, keep in mind that the target signal is gravitational waves from a first-order phase transition in the PTA frequency range. All other frequency ranges will give different benchmark points that are not relevant. A rule of thumb is that the vev and then the transition temperature should be around MeV-GeV scale to give a signal in the PTA range, but this depends on the details of the model and the phase transition. To anchor the scan to the PTA band without committing to a spectrum template, estimate the redshifted peak frequency from the FOPT parameters alone as $f_{\rm peak}\approx 1.6\times10^{-5}\,\mathrm{Hz}\,(\beta/H)\,(T_{\rm reh}/100\,\mathrm{GeV})\,(g_*/100)^{1/6}$, reading $g_*$ from `backend/T_vs_g_gs_GeV.csv`. This is an order-of-magnitude estimate only, the pta-agent owns the exact peak through the selected template. Steer the scan toward the region whose estimated peak falls in the PTA band $f_{\rm peak}\sim 10^{-9}$–$10^{-7}$ Hz. 