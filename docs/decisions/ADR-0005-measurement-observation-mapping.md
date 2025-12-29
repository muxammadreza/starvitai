# ADR-0005: Measurement Observations and derived metrics mapping

## Status
Accepted (2025-12-29)

## Context
We need a canonical, auditable representation of patient-submitted glucose, ketone (BHB), and weight measurements, along with derived metrics such as GKI. These values are PHI and must remain in Medplum. The backend must compute derived metrics server-side and preserve provenance.

## Decision
1) **Store each raw measurement as a separate Observation** rather than a multi-component panel.
2) **Store derived metrics (GKI) as separate Observations**, linked via:
   - `derivedFrom` references to source Observations, and
   - a shared `identifier` (`urn:starvit:measurement-group|{measurementId}`) across the measurement set.
3) **Use a single internal code system** for consistency: `urn:starvit:observation-code`, with UCUM units.
4) **Require explicit timestamps with timezone**; reject ambiguous inputs.
5) **Emit a Provenance** record for each derived metric Observation to capture sources and the backend agent.

## Consequences
- Measurements are queryable and composable without parsing panel components.
- Derived metrics are fully auditable and linked to source Observations.
- Clients must send canonical units (mmol/L, kg) and explicit timestamps.

## Alternatives considered
1) **Single Observation with components** (panel-style): rejected because it complicates per-metric searches and derived-from provenance.
2) **Store GKI as a component on the glucose Observation**: rejected because it obscures provenance and derivedFrom linkage.
3) **Accept mg/dL and convert**: rejected to avoid ambiguous payloads and unit drift during MVP.
4) **Use only LOINC codes**: deferred until an explicit terminology mapping effort (tracked separately) to avoid incorrect or partial code mapping.

## Links
- Mapping spec: `docs/backend/MEASUREMENT_MAPPING.md`

## Rollout plan
1) Deploy backend changes and update OpenAPI.
2) Verify measurement writes and GKI trends in staging using synthetic data.
