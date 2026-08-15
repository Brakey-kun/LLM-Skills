#!/usr/bin/env python3
"""
Zips a finished handoff export folder (handoff.md, handoff.json, assets/)
into a single <folder-name>-handoff.zip next to it.

Usage:
    python package_handoff.py /path/to/export-folder [output_dir]
"""
import sys
import zipfile
from pathlib import Path


def package_handoff(folder: str, output_dir: str | None = None) -> str:
    src = Path(folder).resolve()
    if not src.is_dir():
        raise FileNotFoundError(f"Not a directory: {src}")

    expected = ["handoff.md", "handoff.json"]
    missing = [f for f in expected if not (src / f).exists()]
    if missing:
        print(f"Warning: missing expected file(s): {', '.join(missing)}", file=sys.stderr)

    out_dir = Path(output_dir).resolve() if output_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"{src.name}-handoff.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(src.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(src))

    print(f"Packaged: {zip_path}")
    return str(zip_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    folder_arg = sys.argv[1]
    out_arg = sys.argv[2] if len(sys.argv) > 2 else None
    package_handoff(folder_arg, out_arg)
