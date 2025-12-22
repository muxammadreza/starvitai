# Novelty seeking and hypothesis generation (Starvit)

## What novelty is (and is not)
Novelty is **not** free-form speculation.
Novelty is a candidate relationship that is:
- under-represented in the internal evidence graph,
- supported by cohort data,
- and mechanistically plausible.

## Scoring components
- graph novelty (rarity / low prior)
- cohort robustness (sensitivity checks)
- plausibility (pathway coherence)
- actionability (testability)

## Safeguards
- LLMs do not create evidence. They may summarize retrieved sources with citations.
- Reject candidates with:
  - no supporting paths/subgraphs,
  - unstable signals,
  - biologically implausible constraints violations.

## Triage tiers
Tier 0: known/expected
Tier 1: plausible + supported (prioritize)
Tier 2: interesting but weak (needs more data)
Tier 3: implausible/noisy (discard)
