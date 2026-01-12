import os
import subprocess
import shutil
from jiwer import cer

# SETTINGS
TEST_FOLDER = "./data/sin_eng_custom-ground-truth"
MODEL_NAME = "sin_eng_custom"
TESSDATA_DIR = "./data"
ERROR_FOLDER = "./error_100_images"

os.makedirs(ERROR_FOLDER, exist_ok=True)

def run_tesseract(tif_path, psm=None):
    psm_arg = f"--psm {psm}" if psm else ""
    cmd = (
        f'tesseract "{tif_path}" stdout '
        f'-l {MODEL_NAME} --tessdata-dir {TESSDATA_DIR} {psm_arg}'
    )
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return ""

def run_test():
    files = [f for f in os.listdir(TEST_FOLDER) if f.endswith(".tif")]

    total_cer = 0
    count = 0
    initial_failures = 0
    recovered_with_psm7 = 0
    final_failures = 0

    print(f"\n--- Testing Model: {MODEL_NAME} ---\n")

    for tif in files:
        base_name = tif.replace(".tif", "")
        tif_path = os.path.join(TEST_FOLDER, tif)
        gt_path = os.path.join(TEST_FOLDER, f"{base_name}.gt.txt")

        if not os.path.exists(gt_path):
            continue

        with open(gt_path, "r", encoding="utf-8") as f:
            reference = f.read().strip()

        # 1️⃣ Normal OCR
        ocr_normal = run_tesseract(tif_path)
        cer_normal = cer(reference, ocr_normal)

        total_cer += cer_normal
        count += 1

        print(f"Image: {tif} | CER: {cer_normal:.4f}")

        # 2️⃣ Retry only if totally failed
        if cer_normal == 1.0:
            initial_failures += 1
            ocr_psm7 = run_tesseract(tif_path, psm=7)
            cer_psm7 = cer(reference, ocr_psm7)

            # ✅ Recovered case
            if cer_psm7 < 1.0:
                recovered_with_psm7 += 1
                print("  ✅ Recovered with PSM 7")
                continue

            # ❌ Still failed → save
            final_failures += 1
            print("  ❌ Failed even with PSM 7")

            shutil.copy(tif_path, os.path.join(ERROR_FOLDER, tif))
            shutil.copy(gt_path, os.path.join(ERROR_FOLDER, f"{base_name}.gt.txt"))

            with open(
                os.path.join(ERROR_FOLDER, f"{base_name}.ocr_normal.txt"),
                "w", encoding="utf-8"
            ) as f:
                f.write(ocr_normal if ocr_normal else "[EMPTY OCR OUTPUT]")

            with open(
                os.path.join(ERROR_FOLDER, f"{base_name}.ocr_psm7.txt"),
                "w", encoding="utf-8"
            ) as f:
                f.write(ocr_psm7 if ocr_psm7 else "[EMPTY OCR OUTPUT - PSM 7]")

    avg_cer = (total_cer / count) * 100 if count else 0

    print("\n--- FINAL RESULTS ---")
    print(f"Images Tested            : {count}")
    print(f"Initial 100% CER         : {initial_failures}")
    print(f"Recovered with PSM 7     : {recovered_with_psm7}")
    print(f"Final Failed Images      : {final_failures}")
    print(f"Average CER (initial)    : {avg_cer:.2f}%")
    print(f"Estimated Accuracy       : {100 - avg_cer:.2f}%")

    if final_failures > 0:
        print(f"\n📂 Truly failed samples saved in: {ERROR_FOLDER}")
    else:
        print("\n🎉 No unrecoverable OCR failures found!")

if __name__ == "__main__":
    run_test()
