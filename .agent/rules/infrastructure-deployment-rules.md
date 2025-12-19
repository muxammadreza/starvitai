---
trigger: manual
---

## Infrastructure & Deployment Rules (Coolify Protocol)

We deploy on a single **Hetzner VPS** using **Coolify**. You must write code and configuration that respects this environment.

**Rule 3.1: Docker is the Standard**

* All services must be defined in `docker-compose.yml`.
* Do not rely on Vercel/AWS specific APIs.

**Rule 3.2: Medplum Configuration**

* **NEVER** generate a `medplum.config.json` file.
* **ALWAYS** configure Medplum via Environment Variables in Docker Compose.
* **Mandatory Pattern:** Use `MEDPLUM_BASE_URL`, `MEDPLUM_DATABASE_URL`, and `MEDPLUM_REDIS_URL`.

**Rule 3.3: Neo4j Constraints**

* You must configure Neo4j memory limits to prevent crashing the VPS.
* **Mandatory Env Vars:**
* `NEO4J_server_memory_heap_max__size=2G` (Strict limit).
* `NEO4J_PLUGINS=["apoc", "graph-data-science"]`.



**Rule 3.4: Networking**

* Services communicate internally via Docker Service Names (e.g., `neo4j`, `medplum-server`), NOT localhost.
* Public access is only via the Next.js frontend or Medplum API domain.