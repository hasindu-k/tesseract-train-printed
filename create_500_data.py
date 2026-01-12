import os
import shutil
from glob import glob

dataset_dir = r"C:\github\tesseract-train-printed\lines\dataset"
target_count = 500

# get existing tif files (sorted for consistency)
images = sorted(glob(os.path.join(dataset_dir, "*.tif")))

if not images:
    raise ValueError("No .tif files found in dataset folder")

current_pairs = len(images)
print(f"Currently found {current_pairs} line pairs")

if current_pairs >= target_count:
    print("Already have at least 500 lines. Nothing to do.")
else:
    i = 1
    pair_index = 0  # loop through existing files repeatedly

    while i <= target_count:
        new_name = f"line_{i:04d}"

        new_img = os.path.join(dataset_dir, new_name + ".tif")
        new_txt = os.path.join(dataset_dir, new_name + ".txt")

        # skip if already exists
        if os.path.exists(new_img) and os.path.exists(new_txt):
            i += 1
            continue

        # source files
        src_img = images[pair_index % current_pairs]
        src_txt = src_img.replace(".tif", ".txt")

        shutil.copy(src_img, new_img)

        if os.path.exists(src_txt):
            shutil.copy(src_txt, new_txt)
        else:
            open(new_txt, "w").write("")  # create empty fallback

        pair_index += 1
        i += 1

    print(f"Dataset expanded to {target_count} lines.")
