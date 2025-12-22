---
description: Add a secure Pub/Sub push handler (OIDC-verified) with idempotency and tests
---

1) Define the event contract:
   - message `type`, `version`, and required `payload` schema
   - `correlation_id` and `occurred_at`
2) Decide where the handler lives:
   - if it touches PHI -> keep minimal and call the FHIR adapter
   - if it is de-identified pipeline -> ensure payload is de-identified
3) Implement the HTTP endpoint:
   - verify Pub/Sub OIDC token (audience, issuer, signature) and reject if invalid
   - validate payload with Pydantic
   - enforce idempotency (dedupe key)
   - ack only after side effects succeed; route poison messages to DLQ
4) Add structured logs with correlation_id; do not log payloads containing PHI.
5) Add tests:
   - token verification unit test
   - handler idempotency test
   - happy-path integration test
6) Quality gates:
   // turbo
   - Run `poetry run pytest -q`

Deliver: handler code + message schema + tests + example Pub/Sub message.
