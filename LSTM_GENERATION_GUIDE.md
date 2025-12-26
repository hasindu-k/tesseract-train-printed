# Step 4: Generate LSTM Training Files (.lstmf)

## Overview

LSTM training files (.lstmf) are the required format for training Tesseract's LSTM neural network model. Each `.lstmf` file contains training data for one line image paired with its ground truth text.

## Prerequisites

### 1. **Install Tesseract with LSTM Support**

**Windows:**

```powershell
# Option A: Using Chocolatey
choco install tesseract

# Option B: Download installer
# https://github.com/UB-Mannheim/tesseract/wiki
# Download "tesseract-ocr-w64-setup-v5.x.exe" or newer
```

**Verify Installation:**

```powershell
tesseract --version
```

Should output something like:

```
tesseract 5.x.x
...
```

### 2. **Prepare Ground Truth Files**

You should have `.gt.txt` files in each page directory with the correct text for each line:

```
lines/history 10 S/
├── page_0001/
│   ├── line_0001.tif
│   ├── line_0001.gt.txt    # Contains: "The text from line 0001"
│   ├── line_0002.tif
│   ├── line_0002.gt.txt    # Contains: "The text from line 0002"
```

## Generate LSTM Training Files

### **Method 1: Automated Python Script (Recommended)**

Use the provided `generate_lstmf.py`:

```powershell
python .\generate_lstmf.py
```

This script will:

- ✅ Find Tesseract in your PATH
- ✅ Scan all page directories in `lines/history 10 S/`
- ✅ For each line image + ground truth pair:
  - Generate corresponding `.lstmf` file
  - Skip if `.lstmf` already exists
  - Report errors with details
- ✅ Print summary statistics

### **Method 2: Manual Command-Line**

For a single line image:

```powershell
tesseract lines/history\ 10\ S/page_0001/line_0001.tif lines/history\ 10\ S/page_0001/line_0001 lstmf
```

For all lines in a page (batch):

```powershell
# Navigate to page directory
cd "lines/history 10 S/page_0001"

# Process all TIF files
foreach ($file in Get-ChildItem *.tif) {
    $basename = [io.path]::GetFileNameWithoutExtension($file)
    tesseract $file $basename lstmf
    Write-Host "Generated: $basename.lstmf"
}
```

## Expected Output Structure

After generation, your directories should look like:

```
lines/history 10 S/
├── page_0001/
│   ├── line_0001.tif
│   ├── line_0001.gt.txt
│   ├── line_0001.lstmf      ← Generated!
│   ├── line_0002.tif
│   ├── line_0002.gt.txt
│   ├── line_0002.lstmf      ← Generated!
```

## Troubleshooting

### **"tesseract: command not found"**

- Tesseract is not installed or not in PATH
- Install from: https://github.com/UB-Mannheim/tesseract/wiki
- Restart terminal after installation

### **No .lstmf files generated**

- Check that `.gt.txt` files are not empty
- Verify image files (.tif/.png) are valid
- Check Tesseract output for error messages

### **Empty .gt.txt files**

Use the `create_gt_text_files.py` script to create placeholder files, then populate them with correct text

## Important Notes

⚠️ **Ground Truth Accuracy**: The quality of `.lstmf` files depends entirely on the accuracy of your `.gt.txt` files. Make sure they contain the EXACT text from each line image.

⚠️ **File Format**: Tesseract expects specific image formats:

- TIF/TIFF (recommended for training)
- PNG
- BMP
- JPEG (less recommended for training)

⚠️ **Character Set**: Make sure your `.gt.txt` files use UTF-8 encoding and contain only characters that Tesseract should learn.

## Next Steps

Once you have `.lstmf` files:

1. Collect training data (typically 20,000-50,000+ lines for good results)
2. Combine all `.lstmf` files for training
3. Train Tesseract LSTM model using `tesstrain` toolkit
4. Fine-tune on your specific document type

## Additional Resources

- [Tesseract Training Documentation](https://github.com/tesseract-ocr/tesseract/wiki/Training-Tesseract)
- [Tesstrain (Training Toolkit)](https://github.com/tesseract-ocr/tesstrain)
- [LSTM Training Guide](https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00)
