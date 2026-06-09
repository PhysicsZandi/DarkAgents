---
name: prior-audit
description: Extract, classify and rank assumptions, priors, approximations, uncertainties, validity domains, caveats or limitations across the whole workflow that could affect the interpretation of the final result.
---

# Prior Audit Skill

## Overview

Use this skill to find and audit any assumption, prior, approximation, uncertainty, validity domain, caveat or limitation across the whole workflow that could affect the interpretation of the final result. 

## Task Workflow

1. Collect assumptions, priors, approximations, uncertainties, validity domains, caveats, limitations and warnings from all upstream handoffs. 
2. Make an exhaustive list of all possible audit items.  Check also for some possible solution or propose new possible computations that could resolve the issue, if applicable. Together with all other possible items, check for any unresolved critic warnings from the `critic-agent` and for any constraint raised by the `constraint-agent`, if they are applicable to the model or if there are other not found. 
3. Do a thorough examination using the `WebSearch` and `WebFetch` tools to answer the question: "What could still be missing?". This helps you find implicit items and is necessary to provide novel insights and uncaught assumptions.
4. Classify each item by category and severity. Build a prior audit table with the entries present in the `assumptions` part in the `docs/HANDOFF_PRIOR_AUDIT_SCHEMA.md` template. 

## Rules

- Do not introduce compute new physics calculations or scans. Only audit the existing pipeline assumptions.
- Do not edit upstream files. Only write `prior_audit_report.md`, `prior_audit_table.csv` and `handoff_prior_audit.json` inside `output/<model-name>/`.
