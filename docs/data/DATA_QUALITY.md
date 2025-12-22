# Data quality and testing

## Minimum checks (per dataset)
- freshness SLA
- completeness (row counts, null thresholds)
- validity (ranges/units/enums)
- uniqueness/relationships
- schema drift detection

## ML/feature datasets
- point-in-time correctness tests
- missingness drift
- distribution drift (quantiles/PSI baselines)

## Tooling
- dbt schema tests + custom tests are preferred for BigQuery tables/views
- Dataform assertions are acceptable for Dataform-managed assets
- streaming pipelines must include DLQ + error metrics
