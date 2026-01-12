import os
import shutil

root_dir = r"C:\Users\Hasindu\Desktop\create-dataset"
output_dir = os.path.join(root_dir, "dataset")

os.makedirs(output_dir, exist_ok=True)

for subdir, dirs, files in os.walk(root_dir):
    folder = os.path.basename(subdir)

    # only process page_* folders
    if not folder.startswith("page_"):
        continue

    for file in files:
        if file.endswith(".tif"):
            line_name = file.replace(".tif", "")
            page = folder
            new_base = f"{page}_{line_name}"

            image_src = os.path.join(subdir, file)
            txt_src = os.path.join(subdir, line_name + ".gt.txt")

            image_dst = os.path.join(output_dir, new_base + ".tif")
            txt_dst = os.path.join(output_dir, new_base + ".txt")

            shutil.copy(image_src, image_dst)

            if os.path.exists(txt_src):
                shutil.copy(txt_src, txt_dst)
            else:
                print(f"Missing text file for {image_src}")

print("Dataset created at:", output_dir)
