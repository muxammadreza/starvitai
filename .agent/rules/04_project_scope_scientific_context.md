---
trigger: always_on
---

## Starvit scope and scientific context (quick orientation)

Starvit is a **clinician‑supervised metabolic‑therapy support platform** (oncology first; diabetes/metabolic disease later) with strict PHI controls and a **de‑identified research/ML layer**.

Starvit’s “scientific spine” is metabolic‑oncology viewed through an evolutionary lens:
- Insulin/IGF‑1 → PI3K/AKT/mTOR growth signaling
- Aerobic glycolysis (Warburg effect) vs oxidative metabolism
- Ketogenic metabolic therapy (KMT) and derived metrics like **GKI**
- Stress-response pathways (AMPK/FOXO), inflammation, circadian regulation
- Antagonistic pleiotropy and mismatch theory as the framing for tradeoffs

This is not a “diet app.” It is an auditable decision‑support + research platform.

### Architecture invariants (do not violate)
- PHI system of record: **GCP Healthcare API (FHIR R4)**.
- De‑identified zone: **BigQuery** + **TigerGraph** only; **no PHI**.
- Graph DB (TigerGraph) is **de‑identified zone only** and **never** accessed directly by UIs.
- One backend for MVP (modular monolith). Multiple UIs may exist.

### Bio‑Digital Mirror method (how we work)
For any feature, protocol logic, or ML idea:
1) **Biology**: define the mechanism and the measurable signals.
2) **Evolutionary logic**: state the adaptation/tradeoff that makes the mechanism plausible.
3) **Data model**: map signals to FHIR/BigQuery tables and (if needed) graph entities.
4) **Protocol workflow**: encode as a versioned state machine; “clinician approval required.”
5) **Audit trail**: inputs → transforms → outputs → model/protocol versions.

### Research/ML principles
- Prefer measurable endpoints and derived metrics with explicit units/conversions.
- Make time explicit (windows, cadence, pre/post intervention).
- Use TigerGraph for:
  - cohort discovery,
  - relationship mining,
  - embeddings and link prediction candidates.
- Use Vertex AI for training/serving with full lineage.

### Canonical docs (must consult when relevant)
- Agent guidance: `docs/AGENTS.md`
- Architecture: `docs/ARCHITECTURE.md`
- Decisions/ADRs: `docs/DECISIONS.md`
- Backend engineering: `docs/backend/**`
- Graph engineering: `docs/graph/**`
- ML engineering: `docs/ml/**`
- Scientific references: `docs/research/**`

If a request conflicts with any of the above, stop and escalate to the principal-architect critic workflow.


## Clinical + research context docs (must use)

- `docs/clinical/METABOLIC_ONCOLOGY_KB.md` (conceptual primitives, press–pulse, biomarker framing)
- `docs/clinical/SAFETY_RED_FLAGS.md` (non-bypassable safety gates)
- `docs/clinical/EVIDENCE_METHODS.md` (PRISMA/SPIRIT/CONSORT-AI/GMLP)
- `docs/clinical/REGULATORY_SAMD_CDS.md` (CDS/SaMD framing; transparency requirements)
- `docs/research/sources/*` (NotebookLM ledger + brainstorming + source notes)