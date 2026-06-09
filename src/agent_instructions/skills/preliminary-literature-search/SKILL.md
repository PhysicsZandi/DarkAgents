---
name: preliminary-literature-search
description: Search the literature (arXiv and INSPIRE-HEP) for papers that already studied the model or similar models, and benchmark points of the model parameter space (couplings, vevs, masses) to match the target signal.
---

# Literature Search Skill

## Overview

This skill is used to search the literature (arXiv and INSPIRE-HEP) for papers that already studied the model or similar models, and benchmark points of the model parameter space (couplings, vevs, masses) to match the target signal. The goal is to determine whether the model, structurally similar models, or benchmark points relevant to the requested target signal have already appeared in the literature. The primary sources are arXiv and INSPIRE-HEP.

## Task Workflow

1. Discover potential relevant papers by querying arXiv and INSPIRE-HEP using the `WebSearch` tool. For each candidate paper, record: title, authors, publication date, arXiv ID, abstract, source link and a preliminary relevance score (0-10) based on relevance to the model and target signal.
2. Select the most relevant papers based on the preliminary relevance score, then read them in detail using the `WebFetch` tool to extract: a brief summary, the model studied in the paper including Lagrangian, particle content, symmetries, the target signal(s), benchmark or best-fit model parameter points relevant for the target signal, and an updated relevance score (0-10).
3. Before finalizing the report, verify each kept paper by checking that it exists and that the title, authors and arXiv ID match the citation. Do not include unverified papers as kept papers. 

For the `fopt-pta` branch, check also
- the vev convention, the SSB pattern, the field-dependent masses, the thermal masses, the effective potential, the renormalisation scheme, the FOPT parameter definitions, the spectrum template and the GW target signal. Record convention mismatches. 

## Rules

- Stop when you have a clear picture of the literature landscape, and you have identified whether the model, structurally similar models, or benchmark points relevant to the requested target signal have already appeared in the literature.
- Double-check always if a paper actually exists and whether the title and authors match the citations. Do NOT rely on memory for citations.
- If only abstract or metadata are accessible, do not infer Lagrangians, benchmark points or formulas. Mark the paper as metadata-only and lower the relevance/confidence accordingly.
- Document any assumptions, limitations, caveats and approximations that are made in the process. 
- Pay attention to the benchmark points and parameter space regions studied in the papers, you need to get the details right to be able to compare with the target signal. Use your memory only if you do not find any paper with the relevant benchmark points.
- Pay attention to the target signal, it is possible that the same model has been studied in the literature but not for the target signal of interest. In this case, the paper is still relevant to understand the model structure, but NOT to get benchmark points.
- It is useful to put the target signal in the literature search query to find papers that studied the same model for the same target signal. 


For the `fopt-pta` branch, keep in mind that the target signal is gravitational waves from a first-order phase transition in the PTA frequency range. All other frequency ranges will give different benchmark points that are not relevant. A rule of thumb is that the vev and then the transition temperature should be around MeV-GeV scale to give a signal in the PTA range, but this depends on the details of the model and the phase transition. 