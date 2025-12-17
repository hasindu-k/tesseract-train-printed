import cv2
from PIL import Image
import os

img_path = "pages/page_0001.tif"
output_folder = "lines/"
os.makedirs(output_folder, exist_ok=True)

img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
_, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i, c in enumerate(sorted(contours, key=lambda x: cv2.boundingRect(x)[1])):
    x, y, w, h = cv2.boundingRect(c)
    line_img = img[y:y+h, x:x+w]
    Image.fromarray(line_img).save(f"{output_folder}line_{i+1:04d}.tif")
