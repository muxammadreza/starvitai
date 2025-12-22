#!/usr/bin/env bash
set -euo pipefail

# Verify the sha256 manifest for .agent
# Usage: .agent/tools/verify_manifest.sh

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

if [[ ! -f ".agent/manifest.sha256" ]]; then
  echo "Missing .agent/manifest.sha256. Run .agent/tools/gen_manifest.sh first."
  exit 2
fi

python3 - <<'PY'
import hashlib
from pathlib import Path

manifest = Path(".agent/manifest.sha256").read_text(encoding="utf-8").splitlines()

def sha256_file(p: Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

bad=[]
missing=[]
for line in manifest:
    if not line.strip():
        continue
    expected, path = line.split(maxsplit=1)
    path = path.strip()
    p = Path(path)
    if not p.exists():
        missing.append(path)
        continue
    actual = sha256_file(p)
    if actual != expected:
        bad.append((path, expected, actual))

if missing or bad:
    print("MANIFEST VERIFICATION FAILED")
    if missing:
        print("\nMissing files:")
        for m in missing: print("  -", m)
    if bad:
        print("\nHash mismatches:")
        for path, exp, act in bad:
            print(f"  - {path}\n    expected: {exp}\n    actual:   {act}")
    raise SystemExit(1)

print("Manifest OK")
PY
