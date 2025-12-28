#!/usr/bin/env bash
set -euo pipefail

# Generate a sha256 manifest for .codex (excluding .codex/archive)
# Usage: .codex/tools/gen_manifest.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$ROOT"

python3 - <<'PY'
import hashlib
from pathlib import Path

root = Path.cwd()
agent = root / ".codex"

if not agent.exists():
    raise SystemExit(".codex directory not found. Run from repo root.")

def sha256_file(p: Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

files=[]
for p in sorted(agent.rglob("*")):
    # Exclude archive and the manifest itself (avoid self-referential hash mismatch)
    if p.is_file() and "archive" not in p.parts and p.name != "manifest.sha256":
        files.append(p)

lines=[f"{sha256_file(p)}  {p.relative_to(root).as_posix()}" for p in files]
(agent/"manifest.sha256").write_text("\n".join(lines)+"\n", encoding="utf-8")
print(f"Wrote {len(lines)} entries to .codex/manifest.sha256")
PY
