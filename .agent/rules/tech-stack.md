---
trigger: manual
---

The Tech Stack (Immutable Constraints)

You must strictly adhere to the following technology choices. Do not suggest alternatives.

### **Backend (The Research Engine)**

* **Language:** Python 3.11+
* **Framework:** **FastAPI** (Async, Pydantic v2).
* **Dependency Manager:** Poetry.
* **Key Libraries:** `neo4j` (driver), `pandas` (data), `scikit-learn` (ML).

### **Frontend (The Protocol Designer)**

* **Framework:** **Next.js 16+** (App Router).
* **Language:** TypeScript (Strict Mode).
* **State Logic:** **XState** (For clinical protocol safety).
* **Visualization:** **React Flow** (For drawing metabolic pathways).
* **UI Component System:** **Tamagui** (Universal UI, For future React Native mobile portability).

### **Data Layer (The Truth)**

* **EHR/Identity:** **Medplum** (Headless FHIR Server).
* **Graph Database:** **Neo4j** (Enterprise/Community Docker). *Must include APOC and GDS plugins.*
* **Relational/Vector:** **PostgreSQL** (Docker image: `pgvector/pgvector:pg16`).
* **Caching:** Redis.