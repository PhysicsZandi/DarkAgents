---
name: model-proposal
description: Propose a locally novel BSM particle-physics model candidate that has not already been studied in the local output directory, compatible with the user's request and the available backend code.
---

# Model Proposal Skill

## Overview

This skill is used by the proposer agent to generate a locally novel BSM particle-physics model candidate that has not already been studied in the local output directory, compatible with the user's request and the available backend code. The model must be: 
- locally novel: it cannot be a model that has already been implemented and tested in the `output/<other-model-name>/handoff_model.json`.
- consistent: it must be free of obvious physical inconsistencies and follow the principles of QFT, such as Lagrangian issues or gauge anomalies;
- compatible: it must be compatible with the available backend code.

A model is specified by its field content, symmetries, Lagrangian terms, independent parameters and dependent parameters (if a relation among parameters is present, e.g. CW relation or a vev relation, it must be clearly indicated). Furthermore, according to the user's request, the model must also include branch-specific ingredients:
- if `fopt-pta` is requested, a spontaneous symmetry breaking pattern, scalar background direction, vev convention, tree-level potential, field-dependent masses and thermal/Debye masses of particles getting a mass from the scalar field to compute the one-loop finite-temperature effective potential. Field-dependent and thermal/Debye masses must be analytical expressions, not numerical guesses.

## Task Workflow

1. Inspect the existing model specifications in `output/<other-model-name>/handoff_model.json` when present to rule out duplicates. Compare field content, symmetries, Lagrangian terms and free parameters rather than names. 
2. Propose a minimal locally novel model candidate that satisfies the user's requirements, is compatible with the backend code and is physically consistent. For the candidate, check anomaly cancellation when new chiral fermions or chiral gauge symmetries are introduced and gauge consistency of all Lagrangian terms.
3. Write a self-contained description of the model: field content with representations under all gauge symmetries, symmetries including global and discrete ones, full Lagrangian including kinetic, mass, Yukawa and potential terms, specification of all independent parameters with physical ranges and motivations, specification of all dependent parameters with their defining relations, e.g. CW relation of the quartic coupling or vev relation between quartic coupling, tree-level mass terms and vev, and any additional specifications directly relevant to the user's request and branch requirements.

## Rules

- Same model with different parameter names or a different naming convention is not a novel model. Check the field content, symmetries and Lagrangian terms rather than names to rule out duplicates.
- Do not propose a model that cannot be represented by the available backend.
- Do not propose a model that has already been implemented and studied in the `output/<other-model-name>/handoff_model.json` file, even if it has a different name or a different parameter name choice.
- Do not propose a model that is obviously inconsistent, such as a model with gauge anomalies or a model that violates basic principles of QFT.
- When proposing a model, try to be as minimal as possible in terms of field content, symmetries and Lagrangian terms, while still satisfying the user's request and being compatible with the backend code. Avoid unnecessary complications or extensions that are not directly relevant to the user's request or the target physical signature.
- Only write outputs inside `output/<model-name>/` and do not edit any existing files.
- Document any assumptions, limitations, caveats and approximations that are made in the process.


For the `fopt-pta` branch, pay attention to the dependent and independent parameter classification: in classically scale-invariant / Coleman-Weinberg models, the CW-fixed quartic coupling is dependent; in Higgs-like potentials, the quadratic mass parameter `mu^2` is dependent when fixed by the minimization condition. 

For classically scale-invariant / Coleman-Weinberg models analysed with `backend/semianalytic_pipeline.py`, express the CW relation in the model-independent form in terms of the mass-over-vev ratios `gb`/`gf` and the dof `n`, rather than re-deriving a model-specific quartic:
- `beta_lambda = 1/(8 pi^2) * (sum_B n_B gb^4 - sum_F n_F gf^4)`, with radiative symmetry breaking requiring `beta_lambda > 0` (bosons must dominate over fermions);
- the CW pseudo-dilaton (radial scalar) mass `m_chi^2 = beta_lambda * vev^2`, reported as a dependent quantity;
The scalar `gb` is then not independent but fixed by the gauge and fermion content as `gb_scalar = sqrt(beta_lambda)`, with negligible back-reaction on `beta_lambda`, so do not treat it as a free input or double-count its dof. The quartic `lambda` is renormalisation-scale dependent, is not needed by the backend, and must never be scanned or used as a viability filter.