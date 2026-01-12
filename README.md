# Tesseract Training for Printed Text

## Reference

[ChatGPT Conversation](https://chatgpt.com/share/6942ab02-523c-8001-925e-83c2b6cf4dc0)

## Setup Steps

1. Create TIF images from PDF: `pdf_to_tif.py`
2. Create ground truth text files: `create_gt_text_files.py`
3. Update data folder with new ground-truth files

## Training Command

```bash
cd /c/github/tesseract-train-printed/tesstrain

make training \
    MODEL_NAME=sin_eng_custom \
    START_MODEL=sin \
    TESSDATA=../tessdata/ \
    DATA_DIR=../data/ \
    MAX_ITERATIONS=10000 \
    LEARNING_RATE=0.0001 \
    LANG_TYPE=Indic
```

## Testing

Run from `C:\github\tesseract-train-printed\tesstrain`:

```bash
tesseract "C:\github\train-printed\api\lines\history 10 S first-lesson\page_0008\line_0001.tif" output_result -l sin_eng_custom --tessdata-dir ../data
```

## Comparison: Old vs New Model

**Old model:**

```bash
tesseract "C:\github\train-printed\api\lines\20242025-OL-History-Past-Paper-Sinhala-Medium\page_0001\line_8.tif" result_old -l sin --tessdata-dir ../tessdata
```

**New model:**

```bash
tesseract "C:\github\train-printed\api\lines\20242025-OL-History-Past-Paper-Sinhala-Medium\page_0001\line_8.tif" result_new -l sin_eng_custom --tessdata-dir ../data
```

Both estimate resolution as 397.
