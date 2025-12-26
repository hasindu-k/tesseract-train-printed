#!/usr/bin/env python3
"""
Generate Tesseract LSTM training files (.lstmf) from line images
using existing ground truth (.gt.txt) files.

Folder structure expected:

lines/
└── history 10 S/
    ├── page_0001/
    │   ├── line_0001.tif
    │   ├── line_0001.gt.txt
    │   ├── line_0002.tif
    │   ├── line_0002.gt.txt
    │   └── ...
    ├── page_0002/
    └── ...

Usage:
    python generate_lstmf.py
"""

import os
import subprocess
import sys

# ================= CONFIG =================
LINES_DIR = r"lines/history-10-S"
IMAGE_EXTENSIONS = (".tif", ".tiff", ".png")
GT_EXT = ".gt.txt"
LSTMF_EXT = ".lstmf"
PSM_MODE = "7"   # Single text line
# ==========================================


def check_tesseract():
    """Ensure Tesseract is installed and accessible."""
    try:
        subprocess.run(
            ["tesseract", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return "tesseract"
    except Exception:
        print("❌ ERROR: Tesseract not found in PATH")
        print("Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        sys.exit(1)


def generate_lstmf(image_path, gt_path, tesseract_cmd):
    """
    Generate a .lstmf file for a single line image.
    Tesseract automatically reads <output>.gt.txt
    """

    output_prefix = os.path.splitext(image_path)[0]
    lstmf_path = output_prefix + LSTMF_EXT

    # Skip if already exists
    if os.path.exists(lstmf_path):
        return "exists"

    cmd = [
        tesseract_cmd,
        image_path,
        output_prefix,
        "--oem", "1",
        "--psm", PSM_MODE,
        "lstm.train"
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        return f"error: {result.stderr.strip()}"

    if not os.path.exists(lstmf_path):
        return "failed"

    return "ok"


def main():
    tesseract_cmd = check_tesseract()
    print(f"✔ Found Tesseract: {tesseract_cmd}")

    if not os.path.isdir(LINES_DIR):
        print(f"❌ ERROR: Directory not found: {LINES_DIR}")
        sys.exit(1)

    total = 0
    generated = 0
    skipped = 0
    errors = 0

    for page in sorted(os.listdir(LINES_DIR)):
        page_path = os.path.join(LINES_DIR, page)

        if not os.path.isdir(page_path):
            continue

        print(f"\nProcessing: {page}")

        for file in sorted(os.listdir(page_path)):
            if not file.lower().endswith(IMAGE_EXTENSIONS):
                continue

            total += 1

            image_path = os.path.join(page_path, file)
            base = os.path.splitext(file)[0]
            gt_path = os.path.join(page_path, base + GT_EXT)

            if not os.path.exists(gt_path):
                print(f"  SKIP (no GT): {file}")
                skipped += 1
                continue

            print(f"  GENERATING: {file}...", end=" ")

            result = generate_lstmf(image_path, gt_path, tesseract_cmd)

            if result == "ok":
                print("OK")
                generated += 1
            elif result == "exists":
                print("EXISTS")
                skipped += 1
            else:
                print("FAILED")
                print(f"    ↳ {result}")
                errors += 1

    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"  Total images:     {total}")
    print(f"  Generated:        {generated}")
    print(f"  Skipped:          {skipped}")
    print(f"  Errors:           {errors}")
    print("=" * 60)


if __name__ == "__main__":
    main()
