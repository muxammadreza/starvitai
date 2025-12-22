# BigQuery governance (de-identified zone)

## Goals
- Prevent accidental over-sharing of sensitive quasi-identifiers.
- Make access decisions auditable and reviewable.
- Keep query costs predictable.

## Layers of control
1) Dataset/table IAM (baseline)
2) Row-level security (cohort isolation when needed)
3) Column-level access control (policy tags) for sensitive columns
4) Data masking policies for fields that remain sensitive post de-ID

## Required practices
- Dataset ownership is restricted to a small admin group.
- Writes are restricted to pipeline service accounts.
- Reads are granted via groups and views where possible.
- For any table that can re-identify or isolate individuals:
  - apply RLS and/or policy tags
  - validate with “unauthorized user” test queries
