#!/usr/bin/env python3
import shutil
from pathlib import Path


def copy_ground_truth_files(source_dir, dest_dir):
    source = Path(source_dir)
    dest = Path(dest_dir)

    # Make sure destination exists
    dest.mkdir(parents=True, exist_ok=True)

    # Patterns to search
    patterns = ["*.tif", "*.gt.txt"]

    for pattern in patterns:
        for file_path in source.rglob(pattern):
            if not file_path.is_file():
                continue

            page = file_path.parent.name
            name = file_path.name

            new_name = f"{page}_{name}"
            dest_path = dest / new_name

            # Copy (overwrite if already exists — like cp)
            shutil.copy2(file_path, dest_path)
            print(f"Copied: {file_path} -> {dest_path}")


if __name__ == "__main__":
    copy_ground_truth_files(
        "lines/history 10 S",
        "data/sin_eng_custom-ground-truth"
    )
