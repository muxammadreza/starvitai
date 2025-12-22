# Regulatory framing (SaMD / CDS) for Starvit

This is a product-engineering *risk framing* document. It is not legal advice.

## Why we treat this seriously

Even if Starvit positions itself as clinician-supervised, any feature that:
- recommends protocol changes,
- triages safety risks,
- or influences clinical decisions

can move the product toward **Clinical Decision Support (CDS)** or **Software as a Medical Device (SaMD)** expectations.

## US framing: FDA CDS guidance (high level)

The FDA’s CDS guidance discusses when software functions may be considered non-device CDS vs device functions, with emphasis on whether a healthcare professional can **independently review the basis** for the recommendation.

Starvit implications:
- Prefer “show your work” outputs: evidence cards, links to sources, and transparent feature contributions.
- Separate **monitoring and visualization** from **recommendations**.
- Require explicit clinician sign-off for any suggested protocol changes.

## Global framing: IMDRF SaMD

IMDRF provides:
- SaMD risk categorization (based on significance of info + healthcare situation)
- clinical evaluation principles

Starvit implications:
- Keep a clean distinction between:
  1) valid clinical association
  2) analytical validation
  3) clinical validation
- Maintain versioned model cards and change control.

## ML-specific expectations

Use the GMLP guiding principles as the baseline for ML lifecycle design:
- data quality and representativeness
- model performance characterization (including subgroup analysis)
- human factors and real-world monitoring

## References

- FDA. **Clinical Decision Support Software** guidance (September 2022).
- IMDRF. **SaMD risk categorization** (N12:2014).
- IMDRF. **SaMD clinical evaluation** (N41:2017).
- FDA/Health Canada/MHRA. **GMLP guiding principles** (2021).
