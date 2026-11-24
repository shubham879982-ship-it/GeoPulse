import csv
from pathlib import Path

STORE_COLUMNS = {"store_id", "store_name", "category", "latitude", "longitude"}
VISIT_COLUMNS = {"visit_id", "timestamp", "latitude", "longitude", "activity_type"}

def validate_csv(path: Path, required_columns: set[str]) -> tuple[bool, list[str]]:
    errors = []
    if not path.exists():
        return False, [f"File not found: {path}"]

    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                return False, ["CSV file is empty or has no header."]
            missing = required_columns - set(reader.fieldnames)
            if missing:
                errors.append("Missing columns: " + ", ".join(sorted(missing)))
                return False, errors

            for row_number, row in enumerate(reader, start=2):
                for key in ("latitude", "longitude"):
                    try:
                        value = float(row[key])
                    except (TypeError, ValueError):
                        errors.append(f"Row {row_number}: {key} must be numeric.")
                        continue
                    if key == "latitude" and not -90 <= value <= 90:
                        errors.append(f"Row {row_number}: latitude is outside [-90, 90].")
                    if key == "longitude" and not -180 <= value <= 180:
                        errors.append(f"Row {row_number}: longitude is outside [-180, 180].")
    except OSError as exc:
        return False, [str(exc)]

    return not errors, errors

def validate_inputs(stores_file: Path, visits_file: Path) -> None:
    checks = [
        (stores_file, STORE_COLUMNS),
        (visits_file, VISIT_COLUMNS),
    ]
    all_errors = []
    for path, columns in checks:
        valid, errors = validate_csv(path, columns)
        if not valid:
            all_errors.extend(errors)
    if all_errors:
        raise ValueError("\n".join(all_errors))
