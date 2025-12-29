from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from app.modules.deid.bq_stub import DeidBQStubSink
from app.modules.deid.job_runner import DeidJobSpec, DeidStubRunner
from app.modules.deid.transformer import DEFAULT_DEID_POLICY


def _synthetic_observation(idx: int) -> Dict[str, Any]:
    return {
        "resourceType": "Observation",
        "id": f"obs-{idx}",
        "subject": {"reference": f"Patient/p-{idx}"},
        "effectiveDateTime": datetime.now(tz=timezone.utc).isoformat(),
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "15074-8" if idx % 2 == 0 else "104816-4",
                }
            ]
        },
        "valueQuantity": {"value": 3.5 + idx, "unit": "mmol/L"},
    }


def _build_synthetic_payload(count: int, run_id: str) -> Dict[str, Any]:
    runner = DeidStubRunner()
    job = DeidJobSpec(
        source_kind="synthetic",
        records=[_synthetic_observation(i + 1) for i in range(count)],
        run_id=run_id,
        policy=DEFAULT_DEID_POLICY,
    )
    result = runner.run(job)

    sink = DeidBQStubSink()
    payload = sink.build_payload(result)

    return {
        "deid_observations": payload.observation_rows,
        "deid_run_metadata": payload.run_metadata,
    }


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic de-id payloads (stub only).")
    parser.add_argument("--count", type=int, default=3, help="Number of synthetic observations to generate.")
    parser.add_argument("--run-id", type=str, default="run-synthetic", help="Run identifier for the stub.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")

    args = parser.parse_args(argv)
    if args.count < 1:
        raise SystemExit("count must be >= 1")

    payload = _build_synthetic_payload(count=args.count, run_id=args.run_id)
    payload_json = json.dumps(payload, indent=2)

    if args.output:
        args.output.write_text(payload_json, encoding="utf-8")
    else:
        sys.stdout.write(payload_json + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
