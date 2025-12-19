---
trigger: manual
---

## Coding Standards & Patterns

**5.1 Graph Modeling (Neo4j)**

* Do not use SQL-style logic for complex data.
* **Pattern:** `(:Patient)-[:HAS_METABOLIC_STATE]->(:GKI_Log)-[:LINKED_TO]->(:Tumorresponse)`
* Use Cypher queries optimized for traversal depth (finding hidden links).

**5.2 Clinical Safety (XState)**

* All treatment protocols must be modeled as **State Machines**.
* **Forbidden:** `if/else` spaghetti code for patient logic.
* **Required:** Defined states (e.g., `State: Ketosis_Induction`, `State: Maintenance`, `State: Toxicity_Alert`).

**5.3 Code Generation Style**

* **Backend:** Use Pydantic models for all API inputs/outputs to ensure data validation (Medical grade safety).
* **Frontend:** Mobile-first design using Tamagui stacks for patient facing app, and desktop-first design using Tamagui stacks for clinician faced app.
* **Comments:** Explain the *biological reason* for the code, not just what the code does.
* *Good:* `// Calculate GKI to assess fermentation fuel availability.`
* *Bad:* `// Divide glucose by ketones.`