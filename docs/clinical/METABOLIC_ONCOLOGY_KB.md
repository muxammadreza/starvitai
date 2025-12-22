# Metabolic oncology knowledge base (working)

This is a *modeling reference* for Starvit’s research layer and clinician dashboard. It is not patient advice and must never be used to generate patient-specific instructions without clinician approval.

## Conceptual frame used in Starvit

### Cancer as an energetics problem (operational framing)
Starvit’s research layer treats tumor progression as constrained by energy and redox management in the tumor microenvironment and host organism. This informs a “metabolic management” framing where we:

- measure host metabolic state longitudinally
- stratify tumor/host contexts where metabolic therapy is plausible
- treat any intervention logic as clinician-supervised

### Press–Pulse (why this matters)
Seyfried et al. propose a **Press–Pulse** strategy: sustained “press” stressors coupled to intermittent “pulse” stressors that restrict fermentable fuels (notably glucose and glutamine) and/or raise tumor-selective oxidative stress, while protecting normal cells via availability of non-fermentable fuels (ketones). This is explicitly positioned as a *clinical trial design framework*, not a turnkey patient protocol. (Primary source: Seyfried et al., 2017.)

## Canonical primitives for the platform

### Measurements (MVP)
- **Glucose (mmol/L)**
- **β-hydroxybutyrate / BHB (mmol/L)**
- **Weight trend** (and when available: appetite, functional status)

### Derived metrics
- **Glucose–Ketone Index (GKI)** = glucose (mmol/L) / BHB (mmol/L).
  - The “GKI calculator” concept is described as a pragmatic monitoring tool for metabolic management contexts. (Primary source: Seyfried et al., 2015.)

### Protocol primitives (server-side)
- **Gates**: safety/contraindication checks, clinician-approval checkpoints.
- **State**: metabolic therapy “phase” (baseline → press → pulse cycles → maintenance) with explicit logging.
- **Audit**: inputs → derived metrics → gate outcomes → clinician decision.

## Risk contexts and counterexamples (must be modeled)

### Cachexia / host fragility
Preclinical work shows that ketogenic diets can delay tumor growth in some settings while **worsening host outcomes** (e.g., accelerated cachexia) unless host support is addressed. This is a key design constraint: the platform must treat cachexia risk as a red-flag gate and never “optimize GKI” blindly. (Primary source: Ferrer et al., 2023.)

### Tumor metabolic plasticity
The platform must assume **tumor metabolic heterogeneity**. Some tumors/subtypes may use ketone bodies or engage “backup routes.” This creates a stratification problem (feature engineering + knowledge graph + tumor subtype context) rather than a one-size-fits-all rule.

## How we use the in-repo research notes

- `docs/research/sources/notebooklm resources summary.md` is the **resource ledger**.
- `docs/research/sources/research brainstorming.md` defines the **evolutionary/oncology hypothesis program**.
- Other `docs/research/sources/*` files are source notes and summaries.

## What is safe to productize now vs later

### Safe-ish (monitoring + documentation)
- Unit-safe logging of glucose/BHB + derived GKI.
- Trend displays; adherence tracking.
- Clinician-facing evidence cards.

### Requires clinician-supervised protocol logic
- Any decision thresholds (including GKI targets).
- Contraindication screening and escalation.
- Interaction with chemotherapy/radiation/steroids.

### Research-only (until validated)
- Automated “protocol suggestions” beyond monitoring and data display.
- ML-driven pathway discovery outputs shown to clinicians without an evidence card + uncertainty.

## Primary references

- Seyfried TN, Yu G, Maroon JC, D’Agostino DP. **Press-pulse: a novel therapeutic strategy for the metabolic management of cancer.** *Nutr Metab (Lond).* 2017. (Open access.)
- Seyfried TN et al. **The glucose ketone index calculator: a simple tool to monitor therapeutic efficacy for metabolic management of brain cancer.** 2015. (Open access.)
- Ferrer et al. **Ketogenic diet–associated tumor delay with host-risk tradeoffs (cachexia / endocrine axis context).** *Cell Metabolism.* 2023. (Open access.)
