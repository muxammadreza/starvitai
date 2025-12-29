# Measurement mapping (FHIR Observations)

## Purpose
Define the canonical mapping for patient-submitted glucose, ketone (BHB), and weight readings and derived metrics (e.g., GKI) into Medplum FHIR R4 Observations.

## Audience
Backend engineers, clinical informatics reviewers, and data governance reviewers.

## Coding strategy (canonical)
- Use a **single internal code system** for all measurement Observations: `urn:starvit:observation-code`.
- Add **secondary LOINC codings** for interoperability where applicable.
- Use **UCUM** for `valueQuantity.system` (`http://unitsofmeasure.org`).
- Do **not** convert units server-side; reject non-canonical units.

## Shared Observation fields (all measurement Observations)
- `resourceType`: `Observation`
- `status`: `final`
- `category.coding.system`: `http://terminology.hl7.org/CodeSystem/observation-category`
- `subject.reference`: `Patient/{patientId}`
- `performer.reference`: `Patient/{patientId}` (self-reported)
- `effectiveDateTime`: ISO-8601 with timezone (server stores UTC)
- `valueQuantity.system`: `http://unitsofmeasure.org`
- `identifier`:
  - `system`: `urn:starvit:measurement-group`
  - `value`: `measurementId` (UUID shared across raw + derived Observations)

## Measurement types

### Blood glucose
- `code.coding.system`: `urn:starvit:observation-code`
- `code.coding.code`: `glucose-blood-mmol`
- `code.coding.display`: `Blood glucose (mmol/L)`
- LOINC: `http://loinc.org|15074-8` `Glucose [Moles/volume] in Blood`
- `category`: `laboratory`
- `valueQuantity.unit`: `mmol/L`
- `valueQuantity.code`: `mmol/L`

### Blood beta-hydroxybutyrate (BHB)
- `code.coding.system`: `urn:starvit:observation-code`
- `code.coding.code`: `bhb-blood-mmol`
- `code.coding.display`: `Blood beta-hydroxybutyrate (mmol/L)`
- LOINC: `http://loinc.org|104816-4` `Beta hydroxybutyrate [Moles/volume] in Blood`
- `category`: `laboratory`
- `valueQuantity.unit`: `mmol/L`
- `valueQuantity.code`: `mmol/L`

### Body weight
- `code.coding.system`: `urn:starvit:observation-code`
- `code.coding.code`: `body-weight-kg`
- `code.coding.display`: `Body weight (kg)`
- LOINC: `http://loinc.org|29463-7` `Body weight`
- `category`: `vital-signs`
- `valueQuantity.unit`: `kg`
- `valueQuantity.code`: `kg`

### Derived: Glucose Ketone Index (GKI)
- `code.coding.system`: `urn:starvit:observation-code`
- `code.coding.code`: `gki`
- `code.coding.display`: `Glucose Ketone Index`
- `category`: `laboratory`
- `valueQuantity.unit`: `1` (unitless)
- `valueQuantity.code`: `1`
- `derivedFrom`: references glucose + ketone Observations

## Provenance for derived metrics
For every derived metric Observation, write a `Provenance` resource:
- `target`: `Observation/{gkiObservationId}`
- `entity`: source Observations (glucose + ketone)
- `activity`: `urn:starvit:activity|derived-metric`
- `agent`: `urn:starvit:agent|starvit-backend`
- `identifier`: `urn:starvit:measurement-group|{measurementId}`

## Validation rules (reject ambiguous payloads)
- `measuredAt` **must include a timezone offset**.
- `glucose.unit` **must** be `mmol/L`.
- `ketones.unit` **must** be `mmol/L`.
- `weight.unit` (if provided) **must** be `kg`.
- `glucose.value`, `ketones.value`, `weight.value` (if provided) must be > 0.

## Derived metric formula
- `GKI = glucose (mmol/L) / ketones (mmol/L)`
- Server computes and rounds to 2 decimals.

## Search conventions
- Recent measurements:
  - `Observation?patient=Patient/{id}&code=urn:starvit:observation-code|glucose-blood-mmol,urn:starvit:observation-code|bhb-blood-mmol,urn:starvit:observation-code|body-weight-kg&date=ge{iso}`
- Derived metrics trend:
  - `Observation?patient=Patient/{id}&code=urn:starvit:observation-code|gki&date=ge{iso}`

## How to operate (failure modes + checks)
- If derived metric creation fails, verify the two source Observations exist and have `measurementId`.
- If searches return empty, verify the `code` token matches the `urn:starvit:observation-code` system and the correct `patient` reference.
- If unit validation fails, confirm the client is sending canonical units (no mg/dL).
