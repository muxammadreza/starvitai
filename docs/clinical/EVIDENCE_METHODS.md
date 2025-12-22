# Evidence methods (living reviews + trial design)

This is Starvit’s house style for building a research layer that is clinically credible and audit-able.

## Systematic review / evidence synthesis

- Use **PRISMA 2020** for reporting systematic reviews.
- When feasible, pre-register or document a review protocol, inclusion/exclusion, and risk-of-bias approach.
- Maintain a “living review” update cadence for fast-moving topics.

Minimum artifacts:
- search strategy (queries, databases, dates)
- inclusion/exclusion criteria
- extraction template
- risk-of-bias method (e.g., ROB2, ROBINS-I, QUADAS-2 as appropriate)
- evidence tables and a plain-language summary

## Trial protocol design

- Use **SPIRIT 2013** for clinical trial protocol items.
- If AI is part of the intervention or decision support, add **SPIRIT-AI** items.

## Reporting and evaluation of AI/ML

- For clinical trials evaluating AI interventions: **CONSORT-AI**.
- For prediction models: prefer TRIPOD-style rigor (and TRIPOD-AI when applicable).
- Align evaluation practices with **Good Machine Learning Practice (GMLP)** guiding principles.

## Outputs Starvit produces

- **Evidence cards** (claim → evidence → confidence grade → applicability constraints → engineering implications).
- **Endpoint definitions** (primary/secondary endpoints, measurement windows, missingness handling).
- **Safety gate definitions** (red-flag triggers, escalation steps, clinician override requirements).

## References

- Page MJ et al. **PRISMA 2020 statement.** *BMJ.* 2021.
- Chan A-W et al. **SPIRIT 2013 statement.** 2013.
- Liu X et al. **CONSORT-AI extension.** *BMJ.* 2020.
- Rivera SC et al. **SPIRIT-AI extension.** *BMJ.* 2020.
- FDA/Health Canada/MHRA. **Good Machine Learning Practice (GMLP) guiding principles.** 2021.
