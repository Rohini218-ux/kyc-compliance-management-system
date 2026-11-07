
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EXPORT_DIRS = [
    PROJECT_ROOT / "backend" / "exports" / "anomaly_injected",
    PROJECT_ROOT / "backend" / "exports" / "sql",
]

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def generate_checksums():
    files = []

    for directory in EXPORT_DIRS:
        if not directory.exists():
            print(f"Directory not found: {directory}")
            continue

        for file_path in sorted(directory.rglob("*")):
            if file_path.is_file():
                files.append({
                    "file": str(file_path.relative_to(PROJECT_ROOT)),
                    "size_bytes": file_path.stat().st_size,
                    "sha256": calculate_sha256(file_path)
                })

    manifest = {
        "algorithm": "SHA-256",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files
    }

    output_path = PROJECT_ROOT / "docs" / "checksums.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(manifest, indent=4),
        encoding="utf-8"
    )

    print(f"Checksum manifest created: {output_path}")
    print(f"Files hashed: {len(files)}")


if __name__ == "__main__":
    generate_checksums()
