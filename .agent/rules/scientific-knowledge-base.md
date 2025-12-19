---
trigger: manual
---

## Scientific Knowledge Base (The "Why")

When writing logic, you must understand the biological context. Refer to these axioms:

1. **The Warburg Effect:** Tumors are glucose-dependent.
* *Code implication:* We track **GKI** (Glucose-Ketone Index).
* *Logic:* If GKI > 3.0, trigger "Metabolic Warning" in XState.


2. **Evolutionary Mismatch:** Modern diet (high carb) vs. Ancient Genes (Tumor Suppressors).
* *Code implication:* The app must link "Carbohydrate Intake" events to "Tumor Growth Velocity" predictions in Neo4j.


3. **Press-Pulse Strategy (Seyfried):**
* *Press:* Chronic metabolic stress (Ketogenic diet).
* *Pulse:* Acute stress (Hyperbaric Oxygen, Glycolytic Inhibitors).
* *Code implication:* Protocols are defined as a series of "Press" states and "Pulse" events in the database.