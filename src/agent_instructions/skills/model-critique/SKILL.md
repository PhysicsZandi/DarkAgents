---
name: model-critique
description: Critique the proposed model after reading the preliminary report. Find physical inconsistencies such as gauge anomalies, inconsistent Lagrangian terms, violations of basic QFT principles or branch-specific issues. Apply minimal fixes only when the model was proposed by the proposer-agent and ask for clarification when the model was supplied by the user.
---

# Model Critique Skill

## Overview

This skill is used by the critic agent to critique the proposed model after reading the preliminary report. The goal is to find physical inconsistencies and either apply minimal fixes or request clarification, depending on whether the model was produced by the proposer-agent or supplied directly by the user.
You should answer the following questions:
- Is the model consistent? Are there any red flags or warnings in the Lagrangian, the field content, the symmetries?
- Are the branch-specific assumptions and ingredients internally consistent?

For the FOPT-PTA branch, check also:
- Is the vev convention compatible with the SSB pattern?
- Are the field-dependent masses consistent with the Lagrangian, the SSB pattern and the vev convention?
- Are the thermal masses specified for the relevant bosonic degrees of freedom?

## Task Workflow

1. Examine the model for physical inconsistencies at the level of Lagrangian, symmetries, field content and branch-specific assumptions. Use this focused checklist:
   - field content: identify all fields and verify spin, gauge representations, charges and reality/complexity assumptions;
   - Lagrangian structure: check that every kinetic, mass, Yukawa, portal and scalar-potential term is gauge invariant and compatible with the stated symmetries;
   - Yukawa and mass-spectrum consistency: after assigning vevs, derive the fermion mass matrix for all Yukawa-coupled fermions and verify which components become massive, which remain massless and whether the degrees of freedom match the spectrum assumed downstream;
   - anomalies: check gauge and mixed anomalies only when the model contains new chiral fermions or new gauge symmetries;
   - parameter consistency: check signs, dimensions, allowed ranges, vev definitions, dependent-parameter relations and whether free parameters are overconstrained or incorrectly scanned;
   - branch requirements: check only the branch-specific ingredients needed by the downstream pipeline.
2. For each issue, decide whether it is fixable without introducing a new physics choice. If the model was supplied by the user, do not repair it silently: write the blocking question or ambiguity in the critique output. If the model was proposed by the `proposer-agent`, apply the minimal fix that preserves the initial proposal as much as possible. Classify each issue as red flag or warning, based on whether it is a physical blocker that cannot be ignored and would invalidate downstream results, or a non-blocking assumption, convention, approximation or model-building choice that downstream agents must keep in mind.

In case a FOPT-PTA is requested, check also:
   - Trace the symmetry-breaking pattern from the initial to final gauge group and confirm that it is consistent with the vev assignments. In order to do so, simply take the proposed spontaneous symmetry breaking pattern and verifiy that the vev convention is consistent with it, i.e. that the new vacuum state after SSB is correctly identified by the vev convention and that the unbroken gauge symmetries are consistent with the SSB pattern.
   - Check field-dependent masses by substituting scalar background fields or vevs into the Lagrangian for the fields that enter the scalar potential and the Yukawa interactions. In order to do so, identify the scalar background direction and the fields that get a mass from it, substitute the background field into the Lagrangian, derive the field-dependent mass matrices for scalars, fermions and gauge bosons, diagonalize the mass matrices if needed, and check that the resulting field-dependent masses are consistent with the proposed Lagrangian, SSB pattern and vev convention. Pay attention to the convention used and be sure about the possible presence of factors of 2 or sqrt(2). Recall that real fields (like real gauge bosons or real scalars) have a 1/2 in the mass term while complex fields do not.
   - Check whether the required thermal mass terms are specified for the relevant bosonic degrees of freedom.
   - Check that field-dependent masses and thermal masses are analytical Python/SymPy-compatible strings in the JSON handoff, not numerical guesses.
   - Verify the number of physical degrees of freedom before and after symmetry breaking, including Goldstone modes.

## Rules

- Check every aspect in a quantitative way, do not use vague statements such as "looks consistent" or "seems fine" without a thorough examination. 
- Try the minimal fix that preserves the initial proposal as much as possible. Try not to change the gauge group or the field content, unless it is the only way to fix a critical inconsistency. 
- If you find an issue to a model that has been proposed by the user, ask for clarification to the user. Do not try to fix it by yourself.
- If you find an issue to a model that has been proposed by the `proposer-agent`, try to fix it by yourself with the minimal change possible to the initial proposal.

For the `fopt-pta` branch, pay attention to the dependent and independent parameter classification: in classically scale-invariant / Coleman-Weinberg models, the CW-fixed quartic coupling is dependent; in Higgs-like potentials, the quadratic mass parameter `mu^2` is dependent when fixed by the minimization condition. 

For classically scale-invariant / Coleman-Weinberg models analysed with `backend/semianalytic_pipeline.py`, check that the CW relation is expressed in the model-independent form `beta_lambda = 1/(8 pi^2) * (sum_B n_B gb^4 - sum_F n_F gf^4)` with the dependent quantities `m_chi^2 = beta_lambda * vev^2` and flag any hand-derived quartic that disagrees with it. Require `beta_lambda > 0` (bosons dominating fermions) for radiative symmetry breaking.